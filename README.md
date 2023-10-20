# Semantic Search using Airbnb Data

## Project Overview

To implement a natural language search feature for Airbnb properties. We aim to enable users to search for properties using their own words, making it more intuitive and personalized. Specifically, we plan to leverage customer reviews from all properties to enable semantic search, allowing users to input queries like "quiet cottage close to the beach in LA" or "cozy cabin in the woods by a river in Seattle." Additionally, we intend to explore the use of booking data to find interesting trends in pricing and availability for properties returned in the search results. This proposal seeks to address the question of how enhancing Airbnb's search capabilities with natural language processing and predictive analytics can improve the user experience and increase booking efficiency.

## Directory Structure

```bash
.
├── data/
│   ├── raw/         # Raw data files (original airbnb .csv files)
│   └── processed/   # Processed data files (.pkl and/or .parquet)
├── notebooks/       # Jupyter notebooks for tests
├── src/             # Modularized code files (.py)
│   ├── data/        # Data processing scripts (e.g., data ingest and pre-processing, cleaning)
│   ├── feature/     # Feature engineering scripts for tests
│   ├── models/      # Machine learning models and related 
│   ├── ui/          # UI development related scripts 
│   └── utils/       # Utility scripts (useful generic functions)
├── config/          # Configuration files for hyperparameters, settings, etc. (.yaml)
├── docs/            # Documentation (e.g., project description, API docs)
├── results/         # Model checkpoints, logs, and evaluation results
├── tests/           # Unit tests and integration tests
├── .gitignore       # Git ignore file (specify files/folders that don't need to be uploaded to git)
├── README.md        # Project README file
└── requirements.txt # Python dependencies
```