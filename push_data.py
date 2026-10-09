
import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.logger import logger


class networkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            self.mongo_client.admin.command("ping")

            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

            logger.info("Data inserted successfully into MongoDB Atlas")
            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

        finally:
            if hasattr(self, "mongo_client"):
                self.mongo_client.close()


if __name__ == "__main__":
    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE = "ALAMAI"
    collection = "networkdata"

    networkobj = networkDataExtract()

    records = networkobj.csv_to_json(file_path=FILE_PATH)
    print("Total records:", len(records))

    no_of_records = networkobj.insert_data_mongodb(
        records, DATABASE, collection
    )

    print("Inserted records:", no_of_records)
