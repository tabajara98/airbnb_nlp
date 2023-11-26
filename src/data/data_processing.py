import pandas as pd
import os

# Set option to display up to 500 characters in each column
pd.set_option("max_colwidth", 500)

print("Reading data...")

##
## Read
##

## Listings
listings_folder_path = 'data\\raw\\listings'

# Initialize an empty DataFrame for listings
df_listings = pd.DataFrame()

# Iterate through each listing file in the folder
for listing_file in os.listdir(listings_folder_path):
    listing_file_path = os.path.join(listings_folder_path, listing_file)

    # Read the CSV file with gzip compression
    df = pd.read_csv(listing_file_path, compression='gzip')

    # Concatenate the current DataFrame with the overall listings DataFrame
    df_listings = pd.concat([df, df_listings])

print("Listings data read successfully.")

## Reviews
reviews_folder_path = 'data\\raw\\reviews'

# Initialize an empty DataFrame for reviews
df_reviews = pd.DataFrame()

# Iterate through each review file in the folder
for review_file in os.listdir(reviews_folder_path):
    review_file_path = os.path.join(reviews_folder_path, review_file)

    # Read the CSV file with gzip compression
    df = pd.read_csv(review_file_path, compression='gzip')

    # Concatenate the current DataFrame with the overall reviews DataFrame
    df_reviews = pd.concat([df, df_reviews])

print("Reviews data read successfully.")

print("Transforming data...")

##
## Transform
##

# Listings
# Split name into actual name and summary
df_listings['subtext'] = df_listings['name'].str.split(' · ').str[1:].apply(lambda x: ' · '.join(x))
df_listings['subtext'] = df_listings['subtext'].str.replace('·', '•')
df_listings['name'] = df_listings['name'].str.split(' · ').str[0]

# Rename columns for clarity
df_listings.rename(columns={'listing_url': 'link', 'picture_url': 'photo', 'neighbourhood': 'location'}, inplace=True)

listings_id_column = 'id'
listings_nlp_columns = [
    'amenities',
    'accommodates',
    'name',
    'subtext',
    'property_type',
    'room_type',
    'location',
    'neighbourhood_cleansed',
    'description'
]

# Other columns to save in the DataFrame
cols_aux_final = ['id', 'name', 'subtext', 'description', 'link', 'photo', 'price', 'location','review_scores_rating','latitude','longitude']

# Combine specified columns into a new column 'corpus_text_host'
df_listings.loc[:, 'corpus_text_host'] = ''
for nlp_col in listings_nlp_columns:
    df_listings.loc[:, 'corpus_text_host'] += ' ' + df_listings.loc[:, nlp_col].fillna('').astype(str) + '. '

# Select final columns for the listings DataFrame
df_listings = df_listings[cols_aux_final + ['corpus_text_host']]

# Reviews
# Group reviews by listing_id and concatenate comments
df_reviews_grouped_id = df_reviews.groupby(
    by='listing_id',
    as_index=False
).agg(
    {'comments': lambda review: ' '.join(review.fillna(''))}
)

# Merge listings DataFrame with reviews DataFrame based on the 'id' and 'listing_id' columns
df = pd.merge(
    left=df_listings,
    right=df_reviews_grouped_id,
    left_on='id',
    right_on='listing_id',
    how='left'
)

# Rename the 'comments' column to 'corpus_text_reviews'
df.rename(columns={'comments': 'corpus_text_reviews'}, inplace=True)

# Drop the redundant 'listing_id' column
df.drop(['listing_id'], axis=1, inplace=True)

print("Data transformation completed.")

# Save the final DataFrame as a pickle file
pickle_file_path = 'data\\processed\\processed_data.pkl'
df.to_pickle(pickle_file_path)

print(f"Data saved as pickle file: {pickle_file_path}")
print("Task completed.")
