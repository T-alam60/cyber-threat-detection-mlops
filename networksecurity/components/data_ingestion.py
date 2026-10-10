
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.logger import logger

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo

from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class Dataingestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # MongoDB se data read karke DataFrame banana

# MongoDB se data read karke DataFrame banana
    def export_collection_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            print("Database name:", database_name)
            print("Collection name:", collection_name)

            # MongoDB se connection establish karna
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                serverSelectionTimeoutMS=10000
            )

            # Connection check karna
            self.mongo_client.admin.command("ping")
            print("MongoDB connected successfully")

            collection = self.mongo_client[database_name][collection_name]

            # Collection mein documents count karna
            document_count = collection.count_documents({})
            print("Total documents:", document_count)

            # Documents ko DataFrame mein convert karna
            df = pd.DataFrame(list(collection.find()))

            # _id column remove karna
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            # "na" ko NaN mein convert karna
            df.replace({"na": np.nan}, inplace=True)

            print("DataFrame shape:", df.shape)
            print(df.head())

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    

    # Data ko feature store CSV file mein save karna

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = (
                self.data_ingestion_config.feature_store_file_path
            )

            # Folder exist nahi karta toh create karna
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # DataFrame ko CSV mein save karna
            dataframe.to_csv(
                feature_store_file_path,
                index=False,
                header=True
            )

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Data ko training aur testing sets mein divide karna
    def split_data_train_test_split(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )

            logger.info("Train-test split completed successfully")

            # Training aur testing files ke parent folders create karna
            os.makedirs(
                os.path.dirname(
                    self.data_ingestion_config.training_file_path
                ),
                exist_ok=True
            )

            os.makedirs(
                os.path.dirname(
                    self.data_ingestion_config.testing_file_path
                ),
                exist_ok=True
            )

            # Training data ko CSV mein save karna
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True
            )

            # Testing data ko CSV mein save karna
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True
            )

            logger.info("Training and testing files exported successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Complete data ingestion pipeline execute karna
    def initiate_data_ingestion(self):
        try:
            # Step 1: MongoDB se data lena
            dataframe = self.export_collection_dataframe()

            # Step 2: Feature store mein data save karna
            dataframe = self.export_data_into_feature_store(dataframe)

            # Step 3: Train aur test data create karna
            self.split_data_train_test_split(dataframe)

            # Step 4: Artifact object banana
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=(
                    self.data_ingestion_config.training_file_path
                ),
                test_file_path=(
                    self.data_ingestion_config.testing_file_path
                )
            )

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
