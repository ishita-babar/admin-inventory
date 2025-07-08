import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')

def train_logistic_regression_model():
    """Train and save a Logistic Regression model"""
    print("=== LOGISTIC REGRESSION MODEL TRAINING ===")
    
    # Load data
    df = pd.read_csv('ml/output_with_redis.csv')
    
    # Features and target
    X = df[['wishlist', 'cart', 'avg_rating', 'units_sold', 'returns', 'in_stock']]
    y = df['label']
    
    print(f"Dataset shape: {X.shape}")
    print("Class distribution:")
    print(y.value_counts())
    print(f"Class ratios: {y.value_counts(normalize=True).round(3)}")
    
    # Feature engineering - same as your original code
    X_enhanced = X.copy()
    X_enhanced['return_rate'] = X['returns'] / (X['units_sold'] + 1)
    X_enhanced['demand_signal'] = X['wishlist'] + X['cart']
    X_enhanced['popularity'] = X['avg_rating'] * np.log1p(X['units_sold'])
    
    print(f"Enhanced features: {X_enhanced.columns.tolist()}")
    
    # Encode target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X_enhanced, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")
    
    # Initialize Logistic Regression model
    model = LogisticRegression(
        random_state=42, 
        max_iter=1000,
        class_weight='balanced'
    )
    
    print("\n--- Training Logistic Regression ---")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='f1_weighted')
    print(f"CV F1 Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    # Train on full training set
    model.fit(X_train_scaled, y_train)
    
    # Test predictions
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)
    
    # Calculate metrics
    f1 = f1_score(y_test, y_pred, average='weighted')
    accuracy = accuracy_score(y_test, y_pred)
    
    # Confidence analysis
    max_proba = np.max(y_pred_proba, axis=1)
    high_confidence_pct = (max_proba > 0.8).mean() * 100
    
    print(f"Test F1 Score: {f1:.3f}")
    print(f"Test Accuracy: {accuracy:.3f}")
    print(f"Mean Confidence: {max_proba.mean():.3f}")
    print(f"High Confidence (>0.8): {high_confidence_pct:.1f}%")
    
    # Final evaluation
    print(f"\n=== FINAL EVALUATION ===")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Detailed confidence analysis
    print(f"\nDetailed Confidence Analysis:")
    print(f"Mean confidence: {max_proba.mean():.3f}")
    print(f"Median confidence: {np.median(max_proba):.3f}")
    print(f"Min confidence: {max_proba.min():.3f}")
    print(f"Max confidence: {max_proba.max():.3f}")
    
    for threshold in [0.7, 0.8, 0.9, 0.95]:
        pct = (max_proba > threshold).mean() * 100
        print(f"Predictions with confidence > {threshold}: {pct:.1f}%")
    
    # Feature importance analysis
    print(f"\n=== FEATURE IMPORTANCE ===")
    feature_names = X_enhanced.columns.tolist()
    
    # For multiclass logistic regression, we get coefficients for each class
    print("Feature coefficients by class:")
    for i, class_name in enumerate(le.classes_):
        print(f"\n{class_name}:")
        coef_df = pd.DataFrame({
            'feature': feature_names,
            'coefficient': model.coef_[i]
        })
        coef_df['abs_coefficient'] = np.abs(coef_df['coefficient'])
        coef_df = coef_df.sort_values('abs_coefficient', ascending=False)
        for _, row in coef_df.head(5).iterrows():
            print(f"  {row['feature']}: {row['coefficient']:.3f}")
    
    # Save all components
    joblib.dump(model, 'logistic_regression_model.pkl')
    joblib.dump(le, 'logistic_regression_label_encoder.pkl')
    joblib.dump(scaler, 'logistic_regression_scaler.pkl')
    joblib.dump(X_enhanced.columns.tolist(), 'logistic_regression_features.pkl')
    
    print(f"\nLogistic Regression model saved successfully!")
    print("Saved files:")
    print("- logistic_regression_model.pkl")
    print("- logistic_regression_label_encoder.pkl")
    print("- logistic_regression_scaler.pkl")
    print("- logistic_regression_features.pkl")
    
    return model, le, scaler, X_enhanced.columns.tolist()

def predict_with_logistic_regression(new_data, confidence_threshold=0.8):
    """Make predictions with the trained Logistic Regression model"""
    
    # Load components
    model = joblib.load('logistic_regression_model.pkl')
    le = joblib.load('logistic_regression_label_encoder.pkl')
    scaler = joblib.load('logistic_regression_scaler.pkl')
    feature_names = joblib.load('logistic_regression_features.pkl')
    
    # Feature engineering (same as training)
    X_enhanced = new_data.copy()
    X_enhanced['return_rate'] = new_data['returns'] / (new_data['units_sold'] + 1)
    X_enhanced['demand_signal'] = new_data['wishlist'] + new_data['cart']
    X_enhanced['popularity'] = new_data['avg_rating'] * np.log1p(new_data['units_sold'])
    
    # Ensure features are in the same order as training
    X_enhanced = X_enhanced[feature_names]
    
    # Scale features
    X_scaled = scaler.transform(X_enhanced)
    
    # Make predictions
    predictions_encoded = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)
    
    # Decode predictions
    predictions = le.inverse_transform(predictions_encoded)
    
    # Calculate confidence
    max_proba = np.max(probabilities, axis=1)
    high_confidence_mask = max_proba >= confidence_threshold
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        'prediction': predictions,
        'confidence': max_proba,
        'high_confidence': high_confidence_mask
    })
    
    # Add probability columns for each class
    for i, class_name in enumerate(le.classes_):
        results_df[f'prob_{class_name}'] = probabilities[:, i]
    
    return results_df, predictions, probabilities, high_confidence_mask, max_proba

def load_and_test_model():
    """Load saved model and test with sample data"""
    print("=== TESTING SAVED MODEL ===")
    
    # Sample data for testing
    sample_data = pd.DataFrame({
        'wishlist': [100, 5, 50, 200, 10],
        'cart': [20, 1, 10, 50, 2],
        'avg_rating': [4.8, 2.5, 4.2, 4.9, 3.5],
        'units_sold': [1000, 10, 500, 2000, 100],
        'returns': [20, 5, 25, 40, 15],
        'in_stock': [1, 0, 1, 1, 0]
    })
    
    # Make predictions
    results_df, predictions, probabilities, high_conf_mask, confidences = predict_with_logistic_regression(sample_data)
    
    print("Logistic Regression model predictions:")
    for i, (pred, conf, is_high_conf) in enumerate(zip(predictions, confidences, high_conf_mask)):
        status = "✓ HIGH CONFIDENCE" if is_high_conf else "⚠ LOW CONFIDENCE"
        print(f"Sample {i+1}: {pred} (confidence: {conf:.3f}) - {status}")
    
    print("\nDetailed Results DataFrame:")
    print(results_df.round(3))
    
    return results_df

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    # Train and save the model
    model, le, scaler, features = train_logistic_regression_model()
    
    print("\n" + "="*50)
    
    # Test the saved model
    results = load_and_test_model()