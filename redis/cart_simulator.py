#!/usr/bin/env python3
"""
Redis Cart & Wishlist Simulator
Simulates user intent data for ML forecasting
"""

import redis
import random
import time
import json
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CartSimulator:
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        
        # Product SKUs from our database
        self.product_skus = [
            'ELE-001', 'ELE-002', 'ELE-003',  # Electronics
            'CLO-001', 'CLO-002', 'CLO-003',  # Clothing
            'HOM-001', 'HOM-002', 'HOM-003',  # Home & Garden
            'SPO-001', 'SPO-002', 'SPO-003',  # Sports
            'BOO-001', 'BOO-002', 'BOO-003'   # Books
        ]
        
        # Product popularity weights (higher = more popular)
        self.product_weights = {
            'ELE-001': 0.15,  # Wireless Headphones - very popular
            'ELE-002': 0.12,  # Smartphone - popular
            'ELE-003': 0.08,  # Laptop - moderate
            'CLO-001': 0.20,  # Cotton T-Shirt - very popular
            'CLO-002': 0.10,  # Denim Jeans - popular
            'CLO-003': 0.08,  # Running Shoes - moderate
            'HOM-001': 0.06,  # Garden Hose - low
            'HOM-002': 0.05,  # Kitchen Blender - low
            'HOM-003': 0.12,  # LED Light Bulbs - popular
            'SPO-001': 0.08,  # Yoga Mat - moderate
            'SPO-002': 0.04,  # Basketball - low
            'SPO-003': 0.02,  # Tennis Racket - very low
            'BOO-001': 0.08,  # Programming Guide - moderate
            'BOO-002': 0.06,  # Cookbook - low
            'BOO-003': 0.04   # Fitness Manual - low
        }
        
        # Time-based patterns (hour of day affects activity)
        self.hour_weights = {
            0: 0.1,   # Midnight - low activity
            1: 0.05,  # 1 AM - very low
            2: 0.02,  # 2 AM - minimal
            3: 0.01,  # 3 AM - minimal
            4: 0.01,  # 4 AM - minimal
            5: 0.02,  # 5 AM - minimal
            6: 0.05,  # 6 AM - low
            7: 0.1,   # 7 AM - low
            8: 0.15,  # 8 AM - moderate
            9: 0.2,   # 9 AM - moderate
            10: 0.25, # 10 AM - high
            11: 0.3,  # 11 AM - high
            12: 0.35, # Noon - very high
            13: 0.3,  # 1 PM - high
            14: 0.25, # 2 PM - high
            15: 0.3,  # 3 PM - high
            16: 0.35, # 4 PM - very high
            17: 0.4,  # 5 PM - very high
            18: 0.45, # 6 PM - peak
            19: 0.5,  # 7 PM - peak
            20: 0.45, # 8 PM - peak
            21: 0.4,  # 9 PM - very high
            22: 0.3,  # 10 PM - high
            23: 0.2   # 11 PM - moderate
        }
        
        # Day of week patterns
        self.day_weights = {
            0: 0.8,   # Monday - moderate
            1: 0.9,   # Tuesday - high
            2: 1.0,   # Wednesday - peak
            3: 0.95,  # Thursday - high
            4: 1.1,   # Friday - peak
            5: 1.2,   # Saturday - peak
            6: 0.7    # Sunday - moderate
        }

    def get_current_activity_multiplier(self):
        """Calculate activity multiplier based on current time"""
        now = datetime.now()
        hour_weight = self.hour_weights.get(now.hour, 0.2)
        day_weight = self.day_weights.get(now.weekday(), 1.0)
        return hour_weight * day_weight

    def simulate_cart_activity(self):
        """Simulate add-to-cart activity"""
        activity_multiplier = self.get_current_activity_multiplier()
        
        # Number of cart activities based on time
        base_activities = random.randint(1, 5)
        total_activities = int(base_activities * activity_multiplier)
        
        for _ in range(total_activities):
            # Select product based on popularity weights
            sku = random.choices(
                self.product_skus,
                weights=[self.product_weights[sku] for sku in self.product_skus]
            )[0]
            
            # Increment cart count
            cart_key = f"cart:{sku}"
            current_count = self.redis_client.get(cart_key)
            new_count = int(current_count or 0) + 1
            
            # Set with expiration (7 days)
            self.redis_client.setex(cart_key, 7 * 24 * 3600, new_count)
            
            logger.info(f"Cart activity: {sku} -> {new_count}")

    def simulate_wishlist_activity(self):
        """Simulate wishlist activity"""
        activity_multiplier = self.get_current_activity_multiplier()
        
        # Wishlist activities are less frequent than cart
        base_activities = random.randint(0, 2)
        total_activities = int(base_activities * activity_multiplier)
        
        for _ in range(total_activities):
            # Select product based on popularity weights
            sku = random.choices(
                self.product_skus,
                weights=[self.product_weights[sku] for sku in self.product_skus]
            )[0]
            
            # Increment wishlist count
            wishlist_key = f"wishlist:{sku}"
            current_count = self.redis_client.get(wishlist_key)
            new_count = int(current_count or 0) + 1
            
            # Set with expiration (30 days)
            self.redis_client.setex(wishlist_key, 30 * 24 * 3600, new_count)
            
            logger.info(f"Wishlist activity: {sku} -> {new_count}")

    def cleanup_expired_keys(self):
        """Clean up expired keys (Redis handles this automatically with TTL)"""
        # This is handled automatically by Redis TTL
        pass

    def get_current_stats(self):
        """Get current Redis statistics"""
        cart_keys = self.redis_client.keys("cart:*")
        wishlist_keys = self.redis_client.keys("wishlist:*")
        
        stats = {
            'cart_products': len(cart_keys),
            'wishlist_products': len(wishlist_keys),
            'total_cart_count': sum(int(self.redis_client.get(key) or 0) for key in cart_keys),
            'total_wishlist_count': sum(int(self.redis_client.get(key) or 0) for key in wishlist_keys)
        }
        
        return stats

    def run_simulation(self, duration_minutes=60, interval_seconds=30):
        """Run the simulation for specified duration"""
        logger.info(f"Starting cart/wishlist simulation for {duration_minutes} minutes")
        logger.info(f"Interval: {interval_seconds} seconds")
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        try:
            while datetime.now() < end_time:
                # Simulate activities
                self.simulate_cart_activity()
                self.simulate_wishlist_activity()
                
                # Log current stats every 5 minutes
                if datetime.now().minute % 5 == 0 and datetime.now().second < 30:
                    stats = self.get_current_stats()
                    logger.info(f"Current stats: {stats}")
                
                # Wait for next interval
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            logger.info("Simulation stopped by user")
        
        # Final stats
        final_stats = self.get_current_stats()
        logger.info(f"Simulation completed. Final stats: {final_stats}")

def main():
    """Main function to run the simulator"""
    simulator = CartSimulator()
    
    # Run for 1 hour with 30-second intervals
    simulator.run_simulation(duration_minutes=60, interval_seconds=30)

if __name__ == "__main__":
    main() 