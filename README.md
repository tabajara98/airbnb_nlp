# Semantic Search using Airbnb Data

## Project Overview

To implement a natural language search feature for Airbnb properties. We aim to enable users to search for properties using their own words, making it more intuitive and personalized. Specifically, we plan to leverage customer reviews from all properties to enable semantic search, allowing users to input queries like "quiet cottage close to the beach in LA" or "cozy cabin in the woods by a river in Seattle." This proposal seeks to address the question of how enhancing Airbnb's search capabilities with natural language processing and predictive analytics can improve the user experience and increase booking efficiency.

## Contact Information

Feel free to connect with us on LinkedIn:
- [Ajay Prasad](https://www.linkedin.com/in/ajjuprasad/)
- [Antonio Tabajara](https://www.linkedin.com/in/antonio-tabajara/)
- [Sean Lee](https://www.linkedin.com/in/sean-lee-datascience/)

## Data Access Statement

This project uses the Inside Airbnb data, a mission driven project that provides data and advocacy about Airbnb's impact on residential communities. The data can be accessed or obtained from [Inside Airbnb](https://insideairbnb.com/).

- **Data Ownership:** Inside Airbnb was founded by by Murray Cox, an artist, activist and technologist who conceived the project, compiled and analyzed the data and built the site. John Morris, designer and artist, designed and directed the user experience. It relies on the kind contribution of a variety of collaborators and partners.
- **Licenses:** This data is licensed under a Creative Commons Attribution 4.0 International License.

## Directory Structure

```bash
.
├── data/
│   ├── raw/         # Raw data files (original airbnb .csv files)
│   ├── processed/   # Processed data files (.pkl)
│   └── cached_models/ # Embedded vectors of processed data files and other relevant property data (.pkl) 
├── notebooks/       # Jupyter notebooks for tests
├── src/             # Modularized code files (.py)
│   ├── data/        # Data processing scripts (e.g., data ingest and pre-processing, cleaning)
│   ├── nlp/         # NLP-related tasks, including the SentenceTransformer model
│   ├── app/         # Semantic Search Query & AWS lambda functions
│   ├── react_app/   # React application files (web app components, json, assets, etc)
│   └── ui/          # UI development related scripts 
├── docs/            # Documentation (e.g., project description, API docs)
├── .gitignore       # Git ignore file (specify files/folders that don't need to be uploaded to git)
├── README.md        # Project README file
└── requirements.txt # Python dependencies
```
