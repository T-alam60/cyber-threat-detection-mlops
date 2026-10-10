
import os
import sys
import numpy as np
import pandas as pd

"""
Common constant variables for the NetworkSecurity project.
"""

# Target column name in the dataset
TARGET_COLUMN: str = "Result"

# Name of the machine learning pipeline
PIPELINE_NAME: str = "networksecurity"

# Directory to store pipeline artifacts
ARTIFACT_DIR: str = "Artifacts"

# Original dataset file name
FILE_NAME: str = "phisingData.csv"

# Training dataset file name
TRAIN_FILE_NAME: str = "train.csv"

# Testing dataset file name
TEST_FILE_NAME: str = "test.csv"





"""
Data ingestion related constants start with
DATA_INGESTION_VAR_NAME.
"""

# MongoDB collection name
DATA_INGESTION_COLLECTION_NAME: str = "networkdata"

# MongoDB database name
DATA_INGESTION_DATABASE_NAME: str = "ALAMAI"

# Directory for data ingestion artifacts
DATA_INGESTION_DIR_NAME: str = "data_ingestion"

# Directory for feature store data
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

# Directory for storing ingested data
DATA_INGESTION_INGESTED_DIR: str = "ingested"

# Train-test split ratio: 20% for testing
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

#DATA_INGESTION_COLLECTION_NAME = "Network_Data"
#DATA_INGESTION_COLLECTION_NAME = "networkdata"
