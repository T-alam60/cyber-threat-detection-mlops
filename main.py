
from networksecurity.components.data_ingestion import Dataingestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.logger import logger
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.config_entity import DataValidationConfig

import sys


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()

        # Data Ingestion
        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config
        )

        data_ingestion = Dataingestion(data_ingestion_config)

        logger.info("Initiate the data ingestion")

        data_ingestion_artifact = (
            data_ingestion.initiate_data_ingestion()
        )

        logger.info("Data Ingestion Completed")
        print(data_ingestion_artifact)

        # Data Validation
        data_validation_config = DataValidationConfig(
            training_pipeline_config
        )

        data_validation = DataValidation(
            data_ingestion_artifact,
            data_validation_config
        )

        logger.info("Initiate the data validation")

        data_validation_artifact = (
            data_validation.initiate_data_validation()
        )

        logger.info("Data Validation Completed")
        print(data_validation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
