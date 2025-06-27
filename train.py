import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load training data
data = pd.DataFrame([
    {"sku_id": "ELE-001", "date": "2024-06-01", "wishlist": 30, "cart": 15, "avg_rating": 4.2, "units_sold": 20, "returns": 2, "in_stock": 12, "label_action": "RESTOCK"},
    {"sku_id": "ELE-001", "date": "2024-06-02", "wishlist": 10, "cart": 5, "avg_rating": 2.5, "units_sold": 2, "returns": 5, "in_stock": 10, "label_action": "DISCOUNT"},
    {"sku_id": "APP-001", "date": "2024-06-01", "wishlist": 25, "cart": 10, "avg_rating": 4.5, "units_sold": 15, "returns": 1, "in_stock": 8, "label_action": "RESTOCK"},
    {"sku_id": "APP-001", "date": "2024-06-02", "wishlist": 5, "cart": 2, "avg_rating": 2.8, "units_sold": 3, "returns": 2, "in_stock": 20, "label_action": "DISCOUNT"},
    {"sku_id": "HOM-001", "date": "2024-06-01", "wishlist": 12, "cart": 7, "avg_rating": 4.0, "units_sold": 8, "returns": 0, "in_stock": 5, "label_action": "RESTOCK"},
    {"sku_id": "HOM-001", "date": "2024-06-02", "wishlist": 3, "cart": 1, "avg_rating": 3.0, "units_sold": 1, "returns": 1, "in_stock": 15, "label_action": "DISCOUNT"},
    {"sku_id": "SPO-001", "date": "2024-06-01", "wishlist": 20, "cart": 12, "avg_rating": 4.7, "units_sold": 18, "returns": 0, "in_stock": 10, "label_action": "RESTOCK"},
    {"sku_id": "SPO-001", "date": "2024-06-02", "wishlist": 2, "cart": 1, "avg_rating": 2.0, "units_sold": 2, "returns": 2, "in_stock": 25, "label_action": "DISCOUNT"},
])

# Features and label
features = ["wishlist", "cart", "avg_rating", "units_sold", "returns", "in_stock"]
X = data[features]
y = data["label_action"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Simple classifier
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X_train, y_train)

# Predict and explain
preds = clf.predict(X_test)
print(classification_report(y_test, preds))

def explain_prediction(row):
    if row["wishlist"] > 15 and row["in_stock"] < 15:
        return "High wishlist and low stock → RESTOCK"
    if row["avg_rating"] < 3.0 and row["cart"] < 5:
        return "Low rating and low cart → DISCOUNT"
    if row["units_sold"] > 10 and row["in_stock"] < 10:
        return "High sales and low stock → RESTOCK"
    if row["returns"] > 3:
        return "High returns → DISCOUNT"
    return "Default business logic applied"

# Example explanations
for i, row in X_test.iterrows():
    print(f"Prediction: {clf.predict([row])[0]}, Reason: {explain_prediction(row)}")

# Placeholder for future social media trend matching

def match_social_media_trends(product_catalog, hashtags):
    """
    Placeholder for semantic similarity logic between product catalog and trending hashtags.
    To be implemented: Use NLP models to match product descriptions with trending topics.
    """
    pass 