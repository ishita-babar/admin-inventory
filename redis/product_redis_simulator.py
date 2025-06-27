import redis
import pandas as pd
import random

# Connect to local Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Load products.csv (ensure it has 'product_id' column)
df = pd.read_csv('backend/src/main/resources/products.csv')

# Pick 20,000 random rows (or fewer if dataset is smaller)
sampled = df.sample(n=min(20000, len(df)), random_state=42)

# Iterate and store data in Redis
for _, row in sampled.iterrows():
    product_id = row['product_id']
    wishlist_count = random.randint(0, 1000)
    cart_count = random.randint(0, 500)

    r.set(f'wishlist:{product_id}', wishlist_count)
    r.set(f'cart:{product_id}', cart_count)

# Example: Print counts for 5 random SKUs to verify
print("\n--- Sample Data Stored in Redis ---")
for product_id in sampled['product_id'].sample(5):
    wishlist = r.get(f'wishlist:{product_id}')
    cart = r.get(f'cart:{product_id}')
    print(f"Product ID: {product_id} | Wishlist: {int(wishlist)} | Cart: {int(cart)}")
