from networksecurity.components.data_ingestion import Dataingestion
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.logger import logger
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys




if __name__ == "__main__":
    try:
        TrainingPipelineConfig = TrainingPipelineConfig()
        DataIngestionConfig = DataIngestionConfig(TrainingPipelineConfig)
        data_injestion = Dataingestion(DataIngestionConfig)
        logger.info("initate the data ingestion")
        datainjestioartifact =data_injestion.initiate_data_ingestion()

        
        print(datainjestioartifact) 

    except Exception as e:
        raise NetworkSecurityException(e,sys)