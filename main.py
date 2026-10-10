
from networksecurity.components.data_ingestion import Dataingestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.logger import logger

from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    TrainingPipelineConfig
)

import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()

        # Data Ingestion
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = Dataingestion(dataingestionconfig)

        logger.info("Initiate the data ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()

        logger.info("Data Ingestion Completed")
        print(dataingestionartifact)

        # Data Validation
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(
            dataingestionartifact,
            data_validation_config
        )

        logger.info("Initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()

        logger.info("Data Validation Completed")
        print(data_validation_artifact)

        # Data Transformation
        data_transformation_config = DataTransformationConfig(
            trainingpipelineconfig
        )

        logger.info("Data Transformation Started")
        data_transformation = DataTransformation(
            data_validation_artifact,
            data_transformation_config
        )

        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )

        print(data_transformation_artifact)
        logger.info("Data Transformation Completed")

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
