"""
This script scrapes Instagram hashtags, matches them to product names, and updates output_with_redis.csv to set label_action to 'ORDER STOCK' for trending products. It uses credentials from a .env file for secure login.

Instructions:
1. Create a .env file in your project root with:
   INSTA_USERNAME=your_instagram_username
   INSTA_PASSWORD=your_instagram_password
2. Add .env to your .gitignore.
3. Install dependencies:
   pip install instaloader spacy pandas python-dotenv
   python -m spacy download en_core_web_sm
4. Run this script.
"""
import re
import spacy
import pandas as pd

# --- Step 1: Use Random Trending Hashtags (simulate Instagram trends) ---
trending_hashtags = [
    'h&m',
    'hersheys',
    'zara',
    'puma',
]

# --- Step 2: Lemmatize and Match with Product Names ---
nlp = spacy.load("en_core_web_sm")
def normalize(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

# Load your product catalog
csv_path = 'backend/src/main/resources/products.csv'
df = pd.read_csv(csv_path)
product_names = df['product_id'].astype(str).tolist()
product_titles = df['name'].tolist()
product_lemmas = [normalize(name) for name in product_titles]
hashtag_lemmas = [normalize(tag) for tag in trending_hashtags]

# --- Step 3: Update label_action for Trending Products ---
if 'label_action' not in df.columns:
    df['label_action'] = ''

trending_indices = set()
for i, lemma in enumerate(product_lemmas):
    for h in hashtag_lemmas:
        if h and (h in lemma or lemma in h):
            trending_indices.add(i)
            break

for i in trending_indices:
    df.at[i, 'label_action'] = 'ORDER STOCK (Instagram trend detected)'

# --- Step 4: Output to new CSV ---
df.to_csv('products_trend.csv', index=False)
print("Updated CSV with simulated Instagram trends: products_trend.csv") 