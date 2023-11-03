def semantic_search_airbnb(query):
    
    # Libraries
    import string
    import re
    import nltk
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    import pickle
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
    model = SentenceTransformer(model_name)

    # Cached Embeddings Path (changes according to model)
    embedding_cache_path = f'cache\\cached-embeddings-{model_name}_noclean.pkl'

    with open(embedding_cache_path, "rb") as fIn:
            cache_data = pickle.load(fIn)
    corpus_text = cache_data['text']
    corpus_embeddings = cache_data['embeddings']

    # Encode the query
    clean_query = pd.Series(query).apply(clean_text)
    query_embedding = model.encode(query,show_progress_bar=True,convert_to_tensor=True)

    top_k = 10
    search_results = util.semantic_search(
        query_embedding, corpus_embeddings, top_k=top_k
    )

    # Extract the indices of the most similar sentences
    similar_indices = search_results[0][0:top_k]

    # Extract the actual sentences
    df = pd.DataFrame()
    df['Corpus_Text'] = [corpus_text[c_id] for c_id in [similar_indices[i]['corpus_id'] for i in range(len(similar_indices))]]
    df['Score'] = [item['score'] for item in similar_indices]
    
    return df