def semantic_search_airbnb(query):
    # Libraries
    import string
    import re
    import nltk
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    import pickle
    import torch
    import pandas as pd
    from sentence_transformers import SentenceTransformer, util

    # Download nltk
    nltk.download('stopwords') 
    nltk.download('wordnet')

    ##
    ## Cleaning
    ##

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

    ##
    ## Semantic Search
    ##

    # SBERT model name
    model_name = 'multi-qa-MiniLM-L6-cos-v1'

    # Initialize SBERT model
    print('##### INITIALIZING SBERT MODEL #####')
    model = SentenceTransformer(model_name)

    # Cached Embeddings Path (changes according to model)
    embedding_cache_path = f'data\\cached_models\\cached-embeddings-{model_name}_weighted_clean.pkl'

    print('##### LOADING CACHED EMBEDDINGS #####')
    with open(embedding_cache_path, "rb") as fIn:
        cache_data = pickle.load(fIn)

    # Create a weight tensor
    weights = torch.tensor([0.5, 0.5])
    embeddings = ['embeddings_host', 'embeddings_reviews']
    corpus_embeddings = torch.zeros_like(cache_data[embeddings[0]])  # Initialize an empty tensor

    for i, corpus in enumerate(embeddings):
        # Weight the vectors with the specified weights
        weighted_embeddings = cache_data[corpus] * weights[i]

        # Add the weighted embeddings to the corpus_embeddings
        corpus_embeddings += weighted_embeddings

    # Encode the query
    clean_query = pd.Series(query).apply(clean_text)
    query_embedding = model.encode(query, show_progress_bar=True, convert_to_tensor=True)

    top_k = 10
    print(f'##### PERFORMING SEMANTIC SEARCH FOR QUERY: "{query}" #####')
    search_results = util.semantic_search(
        query_embedding, corpus_embeddings, top_k=top_k
    )

    # Extract the indices of the most similar sentences
    similar_indices = search_results[0][0:top_k]

    # Extract the actual sentences
    df_result = pd.DataFrame()
    for col in ['name', 'subtext', 'description', 'link', 'photo', 'price', 'location','lat','long','starRating']:
        for indice in [similar_indices[i]['corpus_id'] for i in range(len(similar_indices))]:
            df_result.loc[indice, col] = cache_data[col][indice]
    df_result['score'] = [item['score'] for item in similar_indices]

    return df_result

# Example usage
result_df = semantic_search_airbnb('cozy cabin')
print(result_df)
