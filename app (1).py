from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Load quotes data
def load_quotes():
    quotes = pd.read_csv('data/quotes.csv')
    return quotes

# Recommend quotes based on user input
def recommend_quotes(user_input, quotes_df, top_n=5):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(quotes_df['text'])
    
    user_vector = tfidf.transform([user_input])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    recommendations = quotes_df.iloc[top_indices]
    
    return recommendations.to_dict('records')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.json.get('query', '')
    quotes_df = load_quotes()
    recommendations = recommend_quotes(user_input, quotes_df)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)