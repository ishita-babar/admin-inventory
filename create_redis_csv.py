import redis
import pandas as pd

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Load your products (or any source of SKUs)
df = pd.read_csv('backend/src/main/resources/products.csv')  # Adjust path as needed

# Prepare your output data
output_rows = []

for _, row in df.iterrows():
    sku_id = row['product_id']
    # Fetch wishlist and cart from Redis
    wishlist = r.get(f'wishlist:{sku_id}')
    cart = r.get(f'cart:{sku_id}')
    wishlist = int(wishlist) if wishlist else 0
    cart = int(cart) if cart else 0

    # Fill in other fields as needed (use real data or mock for now)
    avg_rating = row.get('rating_avg', 4.0)
    units_sold = 20  # Replace with real or mock data
    returns = 2      # Replace with real or mock data
    in_stock = row.get('units_in_stock', 10)
    label_action = "ORDER STOCK"  # Replace with your logic

    output_rows.append({
        'sku_id': sku_id,
        'wishlist': wishlist,
        'cart': cart,
        'avg_rating': avg_rating,
        'units_sold': units_sold,
        'returns': returns,
        'in_stock': in_stock,
        'label_action': label_action
    })

# Create DataFrame and save to CSV
out_df = pd.DataFrame(output_rows)
out_df.to_csv('output_with_redis.csv', index=False)
print("CSV file created: output_with_redis.csv") 