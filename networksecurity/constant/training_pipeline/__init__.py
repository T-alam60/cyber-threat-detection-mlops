
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


SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")

SAVED_MODEL_DIR =os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"






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



"""
Data Validation related constants
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_VALID_DIR: str = "validated"

DATA_VALIDATION_INVALID_DIR: str = "invalid"

DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"

DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

PREPROCCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"




# Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"

DATA_TRANSFORMED_DATA_DIR: str = "transformed"

DATA_TRANSFORMED_TRAIN_DIR: str = "transformed"

DATA_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

DATA_TRANSFORMED_TRAIN_FILE_NAME: str = "transformed.csv"

DATA_TRANSFORMED_TEST_FILE_NAME: str = "transformed.csv"

DATA_TRANSFORMED_OBJECT_FILE_NAME: str = "transformed_object.pkl"

DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}


DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"




"""
Model Trainer ralated constant start with MODE TRAINER VAR NAME
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05

TRAINING_BUCKET_NAME = "netwworksecurity"



