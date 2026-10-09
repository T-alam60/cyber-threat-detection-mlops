from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.logger import logger

# configration of the data ingestion config 
from networksecurity.entity.config_entity import DataIngestionConfig

import os 
import numpy as np 
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_DB_URL')

