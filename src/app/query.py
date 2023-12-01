import os

os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface/"
os.environ["HF_HOME"] = "/tmp/huggingface/"
os.environ["SENTENCE_TRANSFORMERS_HOME"] = "/tmp/sentence_transformers/"

import json
import string
import re
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
import pickle
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import boto3


# Set the NLTK data path to /tmp for Lambda
nltk.data.path.append("/tmp")

# Download NLTK data
nltk.download('stopwords', download_dir='/tmp')
nltk.download('wordnet', download_dir='/tmp')


# Update util.http_get for caching
util.http_get = lambda *args, **kwargs: util.http_get(*args, **kwargs, cache_folder="/tmp/")

def download_from_s3(bucket, key, download_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, download_path)

def clean_query(text):
    text = "".join([char.lower() for char in text if char not in string.punctuation])
    return text

def semantic_search_airbnb(query, bucket, key):
    # Download nltk data
    nltk.data.path.append("/tmp")
    nltk.download('stopwords', download_dir='/tmp')
    nltk.download('wordnet', download_dir='/tmp')

    # Initialize SBERT model
    print('##### INITIALIZING SBERT MODEL #####')
    model_name = 'multi-qa-MiniLM-L6-cos-v1'
    model = SentenceTransformer(model_name)

    # Download and load the pickle file
    temp_download_path = '/tmp/cached-embeddings-multi-qa-MiniLM-L6-cos-v1_weighted_clean.pkl'
    download_from_s3(bucket, key, temp_download_path)
    with open(temp_download_path, "rb") as fIn:
        cache_data = pickle.load(fIn)

    # Weighted embeddings calculation
    weights = torch.tensor([0.5, 0.5])
    embeddings = ['embeddings_host','embeddings_reviews']
    corpus_embeddings = torch.zeros_like(cache_data[embeddings[0]])

    for i, corpus in enumerate(embeddings):
        weighted_embeddings = cache_data[corpus] * weights[i]
        corpus_embeddings += weighted_embeddings

    # Query processing
    cleaned_query = clean_query(query)
    query_embedding = model.encode(cleaned_query, show_progress_bar=True, convert_to_tensor=True)

    top_k = 15
    print(f'##### PERFORMING SEMANTIC SEARCH FOR QUERY: "{query}" #####')
    search_results = util.semantic_search(
        query_embedding, corpus_embeddings, top_k=top_k
    )

    # Extract the indices of the most similar sentences
    similar_indices = search_results[0][0:top_k]

    # Extract results
    df_result = pd.DataFrame()
    for col in ['id', 'name', 'subtext', 'description', 'link', 'photo', 'price', 'location','lat','long','starRating']:
        for indice in [similar_indices[i]['corpus_id'] for i in range(len(similar_indices))]:
            df_result.loc[indice, col] = cache_data[col][indice]
            result = cache_data[col][indice]
            if str(result) == 'nan':
                if col == 'description':
                    df_result.loc[indice, col] = 'This property does not have a description.'
                elif col == 'location':
                    df_result.loc[indice, col] = 'California, United States'
            else:
                df_result.loc[indice, col] = result 

    df_result['score'] = [item['score'] for item in similar_indices]
    df_result['subtext'] = df_result['subtext'].apply(lambda t: '•'.join(t.split('•')[1:]) if '★' in t else t)
    df_result['description'] = df_result['description'].str.replace('<br />','')


    return df_result.to_json(orient='records')  # This returns a JSON array

    #return df_result.to_json(orient='records')[1:-1] #Old return statement that did not work


def lambda_handler(event, context):
    # Fetch the query from the Lambda event
    query_params = event.get('queryStringParameters', {})
    query = query_params.get('query', '') if query_params else ''

    # S3 Bucket and Key
    bucket_name = 'capstone-airbnb'
    key = 'cached-embeddings-multi-qa-MiniLM-L6-cos-v1_weighted_clean.pkl'

    # Perform the semantic search
    result_json = semantic_search_airbnb(query, bucket_name, key)

    # Create a response
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": result_json  # result_json is already a JSON string
    }

    return response
