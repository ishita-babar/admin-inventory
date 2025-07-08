#!/usr/bin/env python3
"""
ML Forecasting Script for Inventory Management
Analyzes PostgreSQL and Redis data to predict demand and provide recommendations
Also merges in predictions from redis_data_with_predictions.csv and trends_prediction.csv for dashboard display.
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
        self.pg_conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            database=pg_db,
            user=pg_user,
            password=pg_password
        )
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        self.confidence_thresholds = {
            'HIGH': 0.8,
            'MEDIUM': 0.6,
            'LOW': 0.4
        }

    def get_product_data(self) -> pd.DataFrame:
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
            print('DEBUG: Running main product analytics query...')
            df = pd.read_sql_query(query, self.pg_conn)
            print('DEBUG: Main query successful, shape:', df.shape)
            logger.info(f"Fetched data for {len(df)} products")
            return df
        except Exception as e:
            print('ERROR: Main query failed:', e)
            import traceback
            traceback.print_exc()
            logger.error(f"Error fetching product data: {e}")
            return pd.DataFrame()

    def get_redis_intent_data(self, sku: str) -> Dict[str, int]:
        cart_key = f"cart:{sku}"
        wishlist_key = f"wishlist:{sku}"
        cart_count = int(self.redis_client.get(cart_key) or 0)
        wishlist_count = int(self.redis_client.get(wishlist_key) or 0)
        return {
            'cart_count_7d': cart_count,
            'wishlist_count_30d': wishlist_count
        }

    def calculate_sales_velocity(self, sales_30d: int) -> float:
        return sales_30d / 30.0 if sales_30d > 0 else 0.0

    def calculate_return_rate(self, returns_30d: int, sales_30d: int) -> float:
        if sales_30d == 0:
            return 0.0
        return (returns_30d / sales_30d) * 100

    def predict_demand(self, product_data: Dict[str, Any]) -> int:
        sales_velocity = product_data['sales_velocity']
        base_demand = sales_velocity * 30
        cart_multiplier = 1 + (product_data['cart_count_7d'] * 0.1)
        wishlist_multiplier = 1 + (product_data['wishlist_count_30d'] * 0.05)
        rating_multiplier = 1 + (product_data['avg_rating_60d'] - 3) * 0.1
        return_rate = product_data['return_rate']
        return_multiplier = 1 - (return_rate / 100) * 0.2
        predicted_demand = base_demand * cart_multiplier * wishlist_multiplier * rating_multiplier * return_multiplier
        return max(0, int(predicted_demand))

    def determine_action(self, product_data: Dict[str, Any], predicted_demand: int) -> str:
        current_stock = product_data['inventory_count']
        min_stock = product_data['min_stock_level']
        max_stock = product_data['max_stock_level']
        if predicted_demand > 0:
            stock_coverage = current_stock / (predicted_demand / 30)
        else:
            stock_coverage = float('inf')
        if stock_coverage < 7:
            return "RESTOCK"
        elif stock_coverage > 90:
            if product_data['return_rate'] > 15:
                return "DEPRECATE"
            else:
                return "DISCOUNT"
        elif stock_coverage > 60:
            return "DISCOUNT"
        else:
            return "NO ACTION"

    def calculate_confidence(self, product_data: Dict[str, Any]) -> str:
        confidence_score = 0.0
        if product_data['sales_30d'] > 0:
            confidence_score += 0.3
        if product_data['cart_count_7d'] > 0 or product_data['wishlist_count_30d'] > 0:
            confidence_score += 0.2
        if product_data['review_count_60d'] > 0:
            confidence_score += 0.2
        if product_data['sales_velocity'] > 0:
            confidence_score += 0.2
        if product_data['returns_30d'] > 0:
            confidence_score += 0.1
        if confidence_score >= self.confidence_thresholds['HIGH']:
            return "HIGH"
        elif confidence_score >= self.confidence_thresholds['MEDIUM']:
            return "MEDIUM"
        else:
            return "LOW"

    def generate_reason(self, product_data: Dict[str, Any], action: str, predicted_demand: int) -> str:
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
        else:
            return "Optimal inventory levels maintained"

    def generate_forecast(self) -> List[Dict[str, Any]]:
        logger.info("Starting forecast generation...")
        df = self.get_product_data()
        if df.empty:
            logger.error("No product data available")
            return []
        forecasts = []
        for _, row in df.iterrows():
            try:
                intent_data = self.get_redis_intent_data(row['sku'])
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
                product_data['sales_velocity'] = self.calculate_sales_velocity(product_data['sales_30d'])
                product_data['return_rate'] = self.calculate_return_rate(product_data['returns_30d'], product_data['sales_30d'])
                predicted_demand = self.predict_demand(product_data)
                action = self.determine_action(product_data, predicted_demand)
                confidence = self.calculate_confidence(product_data)
                reason = self.generate_reason(product_data, action, predicted_demand)
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
        if self.pg_conn:
            self.pg_conn.close()
        if self.redis_client:
            self.redis_client.close()

#!/usr/bin/env python3
import pandas as pd
import json
import sys

def main():
    forecasts = []
    try:
        products_df = pd.read_csv('backend/src/main/resources/products.csv')
        if 'product_id' in products_df.columns:
            id_col = 'product_id'
        elif 'id' in products_df.columns:
            id_col = 'id'
        else:
            print('ERROR: products.csv missing product_id or id column', file=sys.stderr)
            sys.exit(1)
        name_lookup = dict(zip(products_df[id_col].astype(str), products_df['name']))
        category_lookup = dict(zip(products_df[id_col].astype(str), products_df['category']))
        stock_lookup = dict(zip(products_df[id_col].astype(str), products_df['units_in_stock']))
    except Exception as e:
        print(f'ERROR: Failed to load products.csv: {e}', file=sys.stderr)
        sys.exit(1)

    # Process redis_data_with_predictions.csv
    try:
        redis_df = pd.read_csv('ml/redis_data_with_predictions.csv')
        for _, row in redis_df.iterrows():
            sku_id = str(row['sku_id'])
            label = row['label']
            product_name = name_lookup.get(sku_id, 'Unknown Product')
            category = category_lookup.get(sku_id, '-')
            current_stock = stock_lookup.get(sku_id, '-')
            description = 'Predicted by ML model using wishlist, add to cart, return rate, rating, units sold.'
            if label == 'RESTOCK':
                predicted_demand = int(current_stock) + 500 if current_stock != '-' else 500
            else:
                predicted_demand = '-'
            forecasts.append({
                'sku_id': sku_id,
                'product_name': product_name,
                'category': category,
                'current_stock': current_stock,
                'predicted_demand': predicted_demand,
                'action': label,
                'reason': description
            })
    except Exception as e:
        print(f'ERROR: Failed to load or process redis_data_with_predictions.csv: {e}', file=sys.stderr)

    # Process trends_prediction.csv
    try:
        trends_df = pd.read_csv('ml/trends_prediction.csv')
        for _, row in trends_df.iterrows():
            sku_id = str(row['product_id'])
            product_name = row['product_name']
            category = category_lookup.get(sku_id, '-')
            current_stock = stock_lookup.get(sku_id, '-')
            predicted_demand = int(current_stock) + 500 if current_stock != '-' else 500
            forecasts.append({
                'sku_id': sku_id,
                'product_name': product_name,
                'category': category,
                'current_stock': current_stock,
                'predicted_demand': predicted_demand,
                'action': 'RESTOCK',
                'reason': 'Instagram trend'
            })
    except Exception as e:
        print(f'ERROR: Failed to load or process trends_prediction.csv: {e}', file=sys.stderr)

    with open('ml/forecast_output.json', 'w') as f:
        json.dump(forecasts, f, indent=2)

if __name__ == "__main__":
    main() 