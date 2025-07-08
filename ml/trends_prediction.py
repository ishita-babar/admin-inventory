import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

def load_column_data(file_path, column_name):
    """
    Load specific column from CSV file
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {file_path} with shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        if column_name not in df.columns:
            print(f"Error: Column '{column_name}' not found in {file_path}")
            return None, None
        
        # Get the specified column and remove NaN values
        column_data = df[column_name].dropna().astype(str).tolist()
        print(f"Extracted {len(column_data)} valid entries from column '{column_name}'")
        
        return column_data, df
    
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None, None

def create_embeddings(texts, model_name='all-MiniLM-L6-v2', save_path=None):
    """
    Create vector embeddings for given texts and save to pickle file
    """
    # Check if embeddings already exist
    if save_path and os.path.exists(save_path):
        print(f"Loading existing embeddings from {save_path}")
        try:
            with open(save_path, 'rb') as f:
                embeddings = pickle.load(f)
            print(f"Loaded embeddings with shape: {embeddings.shape}")
            return embeddings
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            print("Creating new embeddings...")
    
    print(f"Creating embeddings using model: {model_name}")
    model = SentenceTransformer(model_name)
    
    # Filter out empty texts
    valid_texts = [text.strip() for text in texts if text.strip()]
    
    if not valid_texts:
        print("No valid texts found for embedding")
        return None
    
    embeddings = model.encode(valid_texts, show_progress_bar=True)
    print(f"Created embeddings with shape: {embeddings.shape}")
    
    # Save embeddings if path provided
    if save_path:
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                pickle.dump(embeddings, f)
            print(f"Embeddings saved to {save_path}")
        except Exception as e:
            print(f"Error saving embeddings: {e}")
    
    return embeddings

def find_similar_pairs(products_embeddings, instagram_embeddings, products_df, instagram_texts, threshold=0.8):
    """
    Find pairs with similarity above threshold, removing duplicates
    """
    print(f"Computing similarity matrix...")
    similarity_matrix = cosine_similarity(products_embeddings, instagram_embeddings)
    
    print(f"Similarity matrix shape: {similarity_matrix.shape}")
    
    # Get valid product names and ids (matching the embeddings)
    valid_products_data = products_df[['name', 'product_id']].dropna()
    valid_products_data['name'] = valid_products_data['name'].astype(str)
    
    # Dictionary to store best matches for each unique product-hashtag combination
    best_matches = {}
    
    for i in range(similarity_matrix.shape[0]):
        for j in range(similarity_matrix.shape[1]):
            similarity = similarity_matrix[i, j]
            if similarity >= threshold:
                product_name = valid_products_data.iloc[i]['name']
                product_id = valid_products_data.iloc[i]['product_id']
                instagram_hashtag = instagram_texts[j]
                
                # Create unique key for product-hashtag combination
                key = (product_name, instagram_hashtag)
                
                # Keep only the best match for each unique combination
                if key not in best_matches or similarity > best_matches[key]['similarity_score']:
                    best_matches[key] = {
                        'similarity_score': similarity,
                        'product_id': product_id,
                        'product_name': product_name,
                        'instagram_hashtag': instagram_hashtag
                    }
    
    # Convert dictionary values to list
    high_similarity_pairs = list(best_matches.values())
    
    # Sort by similarity score (descending)
    high_similarity_pairs.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    return high_similarity_pairs

def save_results_to_csv(similar_pairs, output_path):
    """
    Save similarity results to CSV file
    """
    if similar_pairs:
        results_df = pd.DataFrame(similar_pairs)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        results_df.to_csv(output_path, index=False)
        print(f"Results saved to '{output_path}'")
        return True
    else:
        print("No similar pairs found to save")
        return False

def main():
    """
    Main function to execute the similarity comparison
    """
    print("Starting Vector Embedding Similarity Comparison (Deduplicated)")
    print("="*60)
    
    # File paths
    products_file = 'backend/src/main/resources/products.csv'
    instagram_file = 'ml/dataset_instagram-hashtag-scraper.csv'
    products_pkl = 'ml/products.pkl'
    instagram_pkl = 'ml/dataset_instagram-hashtag-scrapper.pkl'
    results_file = 'ml/trends_prediction.csv'
    
    # Load data from both CSV files
    print("Loading product names...")
    products_names, products_df = load_column_data(products_file, 'name')
    
    print("\nLoading Instagram hashtags...")
    instagram_hashtags, instagram_df = load_column_data(instagram_file, 'hashtag')
    
    if products_names is None or instagram_hashtags is None:
        print("Failed to load one or both datasets")
        return
    
    # Check if products.csv has 'id' column
    if 'product_id' not in products_df.columns:
        print("Error: 'id' column not found in products.csv")
        return
    
    print(f"\nProducts data: {len(products_names)} entries")
    print(f"Instagram data: {len(instagram_hashtags)} entries")
    
    # Create embeddings for products
    print("\nCreating embeddings for product names...")
    products_embeddings = create_embeddings(products_names, save_path=products_pkl)
    
    if products_embeddings is None:
        print("Failed to create embeddings for product names")
        return
    
    # Create embeddings for Instagram hashtags
    print("\nCreating embeddings for Instagram hashtags...")
    instagram_embeddings = create_embeddings(instagram_hashtags, save_path=instagram_pkl)
    
    if instagram_embeddings is None:
        print("Failed to create embeddings for Instagram hashtags")
        return
    
    # Find similar pairs (deduplicated)
    print(f"\nFinding similar pairs with threshold >= 0.8 (removing duplicates)...")
    similar_pairs = find_similar_pairs(
        products_embeddings, 
        instagram_embeddings, 
        products_df, 
        instagram_hashtags, 
        threshold=0.8
    )
    
    # Display results
    print(f"\nFound {len(similar_pairs)} unique pairs with similarity >= 0.8")
    print("="*60)
    
    if similar_pairs:
        # Show top 10 results
        top_results = similar_pairs[:10] if len(similar_pairs) > 10 else similar_pairs
        
        for idx, pair in enumerate(top_results, 1):
            print(f"\nPair {idx}:")
            print(f"Similarity Score: {pair['similarity_score']:.4f}")
            print(f"Product ID: {pair['product_id']}")
            print(f"Product Name: {pair['product_name']}")
            print(f"Instagram Hashtag: {pair['instagram_hashtag']}")
            print("-" * 50)
        
        if len(similar_pairs) > 10:
            print(f"\n... and {len(similar_pairs) - 10} more pairs")
    else:
        print("No pairs found with similarity >= 0.8")
    
    # Save results to CSV
    success = save_results_to_csv(similar_pairs, results_file)
    
    if success:
        print(f"\nProcess completed successfully!")
        print(f"- Product embeddings saved to: {products_pkl}")
        print(f"- Instagram embeddings saved to: {instagram_pkl}")
        print(f"- Deduplicated similarity results saved to: {results_file}")
    else:
        print(f"\nProcess completed but no matches found above threshold 0.8")

if __name__ == "__main__":
    main()