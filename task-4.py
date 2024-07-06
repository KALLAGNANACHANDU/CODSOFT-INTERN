import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
# Load dataset
movies = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv')
ratings = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/ratings.csv')

# Create user-item matrix
user_item_matrix = ratings.pivot(index='user_id', columns='book_id', values='rating').fillna(0)
user_item_sparse = csr_matrix(user_item_matrix.values)

print(user_item_matrix.head())
# Fit the NearestNeighbors model
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(user_item_sparse)

# Find the knn for each user
distances, indices = knn.kneighbors(user_item_sparse, n_neighbors=10)

# distances and indices
print(distances)
print(indices)
# Function to ratings
def predict_ratings(user_item_matrix, indices):
    user_item_matrix_np = user_item_matrix.to_numpy()
    mean_user_rating = user_item_matrix_np.mean(axis=1)
    ratings_diff = (user_item_matrix_np - mean_user_rating[:, np.newaxis])
    pred = np.zeros(user_item_matrix_np.shape)
    
    for i in range(user_item_matrix_np.shape[0]):
        user_ratings = ratings_diff[indices[i]].mean(axis=0)
        pred[i] = mean_user_rating[i] + user_ratings
    
    return pred

# ratings
predicted_ratings = predict_ratings(user_item_matrix, indices)
predicted_ratings_df = pd.DataFrame(predicted_ratings, index=user_item_matrix.index, columns=user_item_matrix.columns)
print(predicted_ratings_df.head())
# Function to recommend items
def recommend_items(user_id, num_recommendations):
    user_row_number = user_id - 1  # Adjust for zero-indexing
    sorted_user_predictions = predicted_ratings_df.iloc[user_row_number].sort_values(ascending=False)
    recommendations = sorted_user_predictions.head(num_recommendations).index
    recommended_books = movies[movies['book_id'].isin(recommendations)]
    return recommended_books

# Recommend items for a user
user_id = 1
num_recommendations = 5
recommendations = recommend_items(user_id, num_recommendations)
print(recommendations)
