import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import torch
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import string
import re
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Set option to display up to 500 characters in each column
pd.set_option("max_colwidth", 500)

# Other columns to save in the DataFrame
cols_aux_final = ['id', 'name', 'subtext', 'description', 'link', 'photo', 'price', 'location','review_scores_rating','latitude','longitude']

# Specify the path to the pickle file
pickle_file_path = 'data\\processed\\processed_data.pkl'

# Read the DataFrame from the pickle file
print("Reading processed data from pickle file...")
df = pd.read_pickle(pickle_file_path).loc[:100]
print("Processed data loaded successfully.")

# Download nltk resources
print("Downloading NLTK resources...")
nltk.download('stopwords') 
nltk.download('wordnet')
print("NLTK resources downloaded successfully.")

# Function to perform all cleaning steps
def clean_text(text):
    # Remove punctuation
    text = "".join([char for char in text if char not in string.punctuation])
    
    # Lowercase the text
    text = text.lower()
    
    # Tokenization
    tokens = re.split(r'\W+', text)
    
    # Remove stopwords
    tokens = [word for word in tokens if word not in stopwords]
    
    # Stemming
    tokens = [porter_stemmer.stem(word) for word in tokens]
    
    # Lemmatization
    tokens = [wordnet_lemmatizer.lemmatize(word) for word in tokens]

    return tokens

# Set of English stopwords
stopwords = set(nltk.corpus.stopwords.words('english'))

# Initialize stemmer and lemmatizer
porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()

# SBERT model name
model_name = 'multi-qa-MiniLM-L6-cos-v1'

# Initialize SBERT model
print('Initializing SBERT model...')
model = SentenceTransformer(model_name)
print('SBERT model initialized successfully.')

# Cached Embeddings Path (changes according to model)
embedding_cache_path = f'data\\cached_models\\cached-embeddings-{model_name}_weighted_clean.pkl'

# Current corpus texts
corpus_texts_host = df['corpus_text_host'].fillna('')
corpus_texts_reviews = df['corpus_text_reviews'].fillna('')

# Encode ALL the current corpus texts into embeddings
print('Encoding corpus texts...')
storage_dict = {}
for corpus_name, corpus_text in zip(['embeddings_host', 'embeddings_reviews'], [corpus_texts_host, corpus_texts_reviews]):
    print(f'> {corpus_name}')
    corpus_embeddings = model.encode(corpus_text, show_progress_bar=True, convert_to_tensor=True)
    
    storage_dict['text_' + corpus_name.split('_')[1]] = corpus_text 
    storage_dict[corpus_name] = corpus_embeddings
    
for col in cols_aux_final:
    storage_dict[col] = df[col].to_list()

# Update & export complete text and embeddings as pkl for future executions
print('Exporting...')
with open(embedding_cache_path, "wb") as fOut:
    pickle.dump(storage_dict, fOut)

print(f"Data exported to {embedding_cache_path}.")
