import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import warnings
warnings.filterwarnings('ignore')

def predict_redis_data(input_file='ml/redis_data.csv', output_file='ml/redis_data_with_predictions.csv', confidence_threshold=0.8):
    """
    Load redis_data.csv, make predictions using saved Logistic Regression model,
    and add label column with predictions
    """
    print("=== REDIS DATA PREDICTION ===")
    
    # Load the redis data
    try:
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} records from {input_file}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Data shape: {df.shape}")
    except FileNotFoundError:
        print(f"Error: {input_file} not found!")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
    # Check if required columns exist
    required_columns = ['wishlist', 'cart', 'avg_rating', 'units_sold', 'returns', 'in_stock']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        return None
    
    # Display sample data
    print("\nSample data:")
    print(df.head())
    
    # Load saved model components
    try:
        model = joblib.load('ml/regression_model/logistic_regression_model.pkl')
        le = joblib.load('ml/regression_model/logistic_regression_label_encoder.pkl')
        scaler = joblib.load('ml/regression_model/logistic_regression_scaler.pkl')
        feature_names = joblib.load('ml/regression_model/logistic_regression_features.pkl')
        print(f"\nModel components loaded successfully!")
        print(f"Classes: {le.classes_}")
        print(f"Feature names: {feature_names}")
    except FileNotFoundError as e:
        print(f"Error: Model files not found. Please train the model first.")
        print(f"Missing file: {e}")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
    
    # Prepare features for prediction
    print(f"\n=== FEATURE ENGINEERING ===")
    
    # Extract base features
    X = df[required_columns].copy()
    
    # Apply same feature engineering as training
    X_enhanced = X.copy()
    X_enhanced['return_rate'] = X['returns'] / (X['units_sold'] + 1)
    X_enhanced['demand_signal'] = X['wishlist'] + X['cart']
    X_enhanced['popularity'] = X['avg_rating'] * np.log1p(X['units_sold'])
    
    # Ensure features are in the same order as training
    X_enhanced = X_enhanced[feature_names]
    
    print(f"Enhanced features shape: {X_enhanced.shape}")
    print(f"Enhanced features: {X_enhanced.columns.tolist()}")
    
    # Handle any missing values
    if X_enhanced.isnull().any().any():
        print("Warning: Found missing values, filling with 0")
        X_enhanced = X_enhanced.fillna(0)
    
    # Scale features
    X_scaled = scaler.transform(X_enhanced)
    print(f"Scaled features shape: {X_scaled.shape}")
    
    # Make predictions
    print(f"\n=== MAKING PREDICTIONS ===")
    predictions_encoded = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)
    
    # Decode predictions
    predictions = le.inverse_transform(predictions_encoded)
    
    # Calculate confidence
    max_proba = np.max(probabilities, axis=1)
    high_confidence_mask = max_proba >= confidence_threshold
    
    # Add predictions to original dataframe
    result_df = df.copy()
    result_df['label'] = predictions
    result_df['confidence'] = max_proba
    result_df['high_confidence'] = high_confidence_mask
    
    # Add probability columns for each class
    for i, class_name in enumerate(le.classes_):
        # Replace spaces with underscores for column names
        col_name = class_name.replace(' ', '_')
        result_df[f'prob_{col_name}'] = probabilities[:, i]
    
    # Show prediction summary
    print(f"\n=== PREDICTION SUMMARY ===")
    print(f"Total predictions: {len(predictions)}")
    print(f"Prediction distribution:")
    print(pd.Series(predictions).value_counts())
    print(f"\nPrediction percentages:")
    print(pd.Series(predictions).value_counts(normalize=True).round(3))
    
    print(f"\nConfidence analysis:")
    print(f"Mean confidence: {max_proba.mean():.3f}")
    print(f"Median confidence: {np.median(max_proba):.3f}")
    print(f"Min confidence: {max_proba.min():.3f}")
    print(f"Max confidence: {max_proba.max():.3f}")
    
    for threshold in [0.7, 0.8, 0.9, 0.95]:
        pct = (max_proba > threshold).mean() * 100
        print(f"Predictions with confidence > {threshold}: {pct:.1f}%")
    
    # Show sample predictions
    print(f"\n=== SAMPLE PREDICTIONS ===")
    sample_df = result_df.head(10)[['sku_id', 'wishlist', 'cart', 'avg_rating', 'units_sold', 'returns', 'in_stock', 'label', 'confidence', 'high_confidence']]
    print(sample_df.round(3))
    
    # Save results
    result_df.to_csv(output_file, index=False)
    print(f"\n=== RESULTS SAVED ===")
    print(f"Full results saved to: {output_file}")
    print(f"Columns in output file: {result_df.columns.tolist()}")
    
    # Create a simple version with just the label column added
    simple_result = df.copy()
    simple_result['label'] = predictions
    simple_output_file = input_file.replace('.csv', '_with_labels.csv')
    simple_result.to_csv(simple_output_file, index=False)
    print(f"Simple version (with just label) saved to: {simple_output_file}")
    
    return result_df

def analyze_predictions(df):
    """Analyze the predictions in more detail"""
    print(f"\n=== DETAILED PREDICTION ANALYSIS ===")
    
    # Group by prediction and show statistics
    for action in df['label'].unique():
        subset = df[df['label'] == action]
        print(f"\n{action} predictions ({len(subset)} items):")
        print(f"  Average confidence: {subset['confidence'].mean():.3f}")
        print(f"  High confidence rate: {subset['high_confidence'].mean()*100:.1f}%")
        print(f"  Average units sold: {subset['units_sold'].mean():.0f}")
        print(f"  Average rating: {subset['avg_rating'].mean():.2f}")
        print(f"  Average return rate: {(subset['returns']/subset['units_sold']).mean():.3f}")
        print(f"  In stock rate: {subset['in_stock'].mean()*100:.1f}%")

def main():
    """Main execution function"""
    # Make predictions
    result_df = predict_redis_data()
    
    if result_df is not None:
        # Analyze predictions
        analyze_predictions(result_df)
        
        # Show low confidence predictions for review
        print(f"\n=== LOW CONFIDENCE PREDICTIONS (< 0.8) ===")
        low_conf = result_df[result_df['confidence'] < 0.8]
        if len(low_conf) > 0:
            print(f"Found {len(low_conf)} low confidence predictions:")
            print(low_conf[['sku_id', 'label', 'confidence', 'prob_DISCOUNT', 'prob_NO_CHANGE', 'prob_RESTOCK']].head(10).round(3))
        else:
            print("No low confidence predictions found!")
        
        print(f"\n=== PROCESS COMPLETED SUCCESSFULLY ===")
        print(f"Check the output files for your predictions!")
    else:
        print("Prediction process failed!")

if __name__ == "__main__":
    main()