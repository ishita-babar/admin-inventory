#!/usr/bin/env python3
"""
ML Forecasting Script for Inventory Management
Analyzes PostgreSQL and Redis data to predict demand and provide recommendations
"""

import psycopg2
import redis
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InventoryForecaster:
    def __init__(self, 
                 pg_host='localhost', pg_port=5432, pg_db='inventory_dashboard', 
                 pg_user='postgres', pg_password='password',
                 redis_host='localhost', redis_port=6379, redis_db=0):
        
        # PostgreSQL connection
        self.pg_conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            database=pg_db,
            user=pg_user,
            password=pg_password
        )
        
        # Redis connection
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        
        # ML model parameters (placeholder for future ARIMA/Prophet implementation)
        self.confidence_thresholds = {
            'HIGH': 0.8,
            'MEDIUM': 0.6,
            'LOW': 0.4
        }

    def get_product_data(self) -> pd.DataFrame:
        """Fetch product analytics data from PostgreSQL"""
        query = """
        SELECT 
            p.id,
            p.sku,
            p.name,
            p.category_id,
            c.name as category_name,
            p.price,
            p.inventory_count,
            p.min_stock_level,
            p.max_stock_level,
            COALESCE(SUM(s.quantity), 0) as sales_30d,
            COALESCE(SUM(s.revenue), 0) as revenue_30d,
            COALESCE(AVG(r.rating), 0) as avg_rating_60d,
            COALESCE(COUNT(r.id), 0) as review_count_60d,
            COALESCE(SUM(ret.quantity), 0) as returns_30d,
            CASE 
                WHEN p.inventory_count <= p.min_stock_level THEN 'Low Stock'
                WHEN p.inventory_count >= p.max_stock_level THEN 'Overstock'
                ELSE 'In Stock'
            END as inventory_status
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN sales s ON p.id = s.product_id 
            AND s.sale_date >= CURRENT_DATE - INTERVAL '30 days'
        LEFT JOIN reviews r ON p.id = r.product_id 
            AND r.review_date >= CURRENT_DATE - INTERVAL '60 days'
        LEFT JOIN returns ret ON p.id = ret.product_id 
            AND ret.return_date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY p.id, p.sku, p.name, p.category_id, c.name, p.price, 
                 p.inventory_count, p.min_stock_level, p.max_stock_level
        ORDER BY p.sku
        """
        
        try:
            df = pd.read_sql_query(query, self.pg_conn)
            logger.info(f"Fetched data for {len(df)} products")
            return df
        except Exception as e:
            logger.error(f"Error fetching product data: {e}")
            return pd.DataFrame()

    def get_redis_intent_data(self, sku: str) -> Dict[str, int]:
        """Get cart and wishlist data from Redis for a specific SKU"""
        cart_key = f"cart:{sku}"
        wishlist_key = f"wishlist:{sku}"
        
        cart_count = int(self.redis_client.get(cart_key) or 0)
        wishlist_count = int(self.redis_client.get(wishlist_key) or 0)
        
        return {
            'cart_count_7d': cart_count,
            'wishlist_count_30d': wishlist_count
        }

    def calculate_sales_velocity(self, sales_30d: int) -> float:
        """Calculate daily sales velocity"""
        return sales_30d / 30.0 if sales_30d > 0 else 0.0

    def calculate_return_rate(self, returns_30d: int, sales_30d: int) -> float:
        """Calculate return rate percentage"""
        if sales_30d == 0:
            return 0.0
        return (returns_30d / sales_30d) * 100

    def predict_demand(self, product_data: Dict[str, Any]) -> int:
        """
        Predict future demand using multiple signals
        This is a simplified algorithm - replace with ARIMA/Prophet later
        """
        # Base demand from sales velocity
        sales_velocity = product_data['sales_velocity']
        base_demand = sales_velocity * 30  # 30-day prediction
        
        # Adjust based on user intent signals
        cart_multiplier = 1 + (product_data['cart_count_7d'] * 0.1)
        wishlist_multiplier = 1 + (product_data['wishlist_count_30d'] * 0.05)
        
        # Adjust based on rating (higher rating = higher demand)
        rating_multiplier = 1 + (product_data['avg_rating_60d'] - 3) * 0.1
        
        # Adjust based on return rate (higher returns = lower demand)
        return_rate = product_data['return_rate']
        return_multiplier = 1 - (return_rate / 100) * 0.2
        
        # Calculate final prediction
        predicted_demand = base_demand * cart_multiplier * wishlist_multiplier * rating_multiplier * return_multiplier
        
        # Ensure positive value
        return max(0, int(predicted_demand))

    def determine_action(self, product_data: Dict[str, Any], predicted_demand: int) -> str:
        """Determine recommended action based on inventory and predicted demand"""
        current_stock = product_data['inventory_count']
        min_stock = product_data['min_stock_level']
        max_stock = product_data['max_stock_level']
        
        # Calculate stock coverage (days of inventory based on predicted demand)
        if predicted_demand > 0:
            stock_coverage = current_stock / (predicted_demand / 30)  # days
        else:
            stock_coverage = float('inf')
        
        # Decision logic
        if stock_coverage < 7:  # Less than 1 week of stock
            return "RESTOCK"
        elif stock_coverage > 90:  # More than 3 months of stock
            if product_data['return_rate'] > 15:  # High return rate
                return "DEPRECATE"
            else:
                return "DISCOUNT"
        elif stock_coverage > 60:  # More than 2 months of stock
            return "DISCOUNT"
        else:
            return "NO ACTION"

    def calculate_confidence(self, product_data: Dict[str, Any]) -> str:
        """Calculate confidence level based on data quality and consistency"""
        # Factors that increase confidence
        confidence_score = 0.0
        
        # Sales data availability
        if product_data['sales_30d'] > 0:
            confidence_score += 0.3
        
        # User intent data availability
        if product_data['cart_count_7d'] > 0 or product_data['wishlist_count_30d'] > 0:
            confidence_score += 0.2
        
        # Review data availability
        if product_data['review_count_60d'] > 0:
            confidence_score += 0.2
        
        # Sales velocity stability (simplified)
        if product_data['sales_velocity'] > 0:
            confidence_score += 0.2
        
        # Return rate data
        if product_data['returns_30d'] > 0:
            confidence_score += 0.1
        
        # Determine confidence level
        if confidence_score >= self.confidence_thresholds['HIGH']:
            return "HIGH"
        elif confidence_score >= self.confidence_thresholds['MEDIUM']:
            return "MEDIUM"
        else:
            return "LOW"

    def generate_reason(self, product_data: Dict[str, Any], action: str, predicted_demand: int) -> str:
        """Generate human-readable reason for the recommendation"""
        current_stock = product_data['inventory_count']
        
        if action == "RESTOCK":
            if current_stock <= product_data['min_stock_level']:
                return "Low inventory and high predicted demand"
            else:
                return "High cart/wishlist activity and low inventory"
        
        elif action == "DISCOUNT":
            if product_data['return_rate'] > 10:
                return "High inventory and moderate return rate"
            else:
                return "High inventory with good product performance"
        
        elif action == "DEPRECATE":
            return "High inventory and high return rate"
        
        else:  # NO ACTION
            return "Optimal inventory levels maintained"

    def generate_forecast(self) -> List[Dict[str, Any]]:
        """Generate comprehensive forecast for all products"""
        logger.info("Starting forecast generation...")
        
        # Get product data from PostgreSQL
        df = self.get_product_data()
        if df.empty:
            logger.error("No product data available")
            return []
        
        forecasts = []
        
        for _, row in df.iterrows():
            try:
                # Get Redis intent data
                intent_data = self.get_redis_intent_data(row['sku'])
                
                # Prepare product data dictionary
                product_data = {
                    'id': row['id'],
                    'sku': row['sku'],
                    'name': row['name'],
                    'category_name': row['category_name'],
                    'price': float(row['price']),
                    'inventory_count': int(row['inventory_count']),
                    'min_stock_level': int(row['min_stock_level']),
                    'max_stock_level': int(row['max_stock_level']),
                    'sales_30d': int(row['sales_30d']),
                    'revenue_30d': float(row['revenue_30d']),
                    'avg_rating_60d': float(row['avg_rating_60d']),
                    'review_count_60d': int(row['review_count_60d']),
                    'returns_30d': int(row['returns_30d']),
                    'inventory_status': row['inventory_status'],
                    'cart_count_7d': intent_data['cart_count_7d'],
                    'wishlist_count_30d': intent_data['wishlist_count_30d']
                }
                
                # Calculate derived metrics
                product_data['sales_velocity'] = self.calculate_sales_velocity(product_data['sales_30d'])
                product_data['return_rate'] = self.calculate_return_rate(product_data['returns_30d'], product_data['sales_30d'])
                
                # Generate prediction
                predicted_demand = self.predict_demand(product_data)
                action = self.determine_action(product_data, predicted_demand)
                confidence = self.calculate_confidence(product_data)
                reason = self.generate_reason(product_data, action, predicted_demand)
                
                # Create forecast result
                forecast = {
                    'sku_id': product_data['sku'],
                    'product_name': product_data['name'],
                    'category': product_data['category_name'],
                    'predicted_demand': predicted_demand,
                    'current_stock': product_data['inventory_count'],
                    'action': action,
                    'confidence': confidence,
                    'reason': reason,
                    'metrics': {
                        'sales_velocity': round(product_data['sales_velocity'], 2),
                        'return_rate': round(product_data['return_rate'], 2),
                        'avg_rating': round(product_data['avg_rating_60d'], 2),
                        'cart_activity': product_data['cart_count_7d'],
                        'wishlist_activity': product_data['wishlist_count_30d']
                    }
                }
                
                forecasts.append(forecast)
                logger.info(f"Generated forecast for {product_data['sku']}: {action}")
                
            except Exception as e:
                logger.error(f"Error processing {row['sku']}: {e}")
                continue
        
        logger.info(f"Forecast generation completed. Processed {len(forecasts)} products.")
        return forecasts

    def close_connections(self):
        """Close database connections"""
        if self.pg_conn:
            self.pg_conn.close()
        if self.redis_client:
            self.redis_client.close()

def main():
    """Main function to run forecasting"""
    try:
        # Initialize forecaster
        forecaster = InventoryForecaster()
        
        # Generate forecast
        forecasts = forecaster.generate_forecast()
        
        # Output results
        if forecasts:
            print(json.dumps(forecasts, indent=2))
        else:
            print("No forecasts generated")
            
    except Exception as e:
        logger.error(f"Forecast generation failed: {e}")
        sys.exit(1)
    finally:
        forecaster.close_connections()

if __name__ == "__main__":
    main() 