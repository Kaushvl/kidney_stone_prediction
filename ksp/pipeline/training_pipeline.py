from ksp.logger import logging
from ksp.exception import CustomException
from ksp.entity import config_entity
import sys, os
from ksp.entity import artifact_entity
import pandas as pd
from ksp.components.data_transformation import DataTransformation
from ksp.components.model_trainer import ModelTrainer
from ksp.components.data_ingestion import DataIngestion


class Train:
    def __init__(self):
        self.c = 0
        print(self.c)

    def main(self):
        pass

if __name__ == "__main__":

    training_pipeline_config = config_entity.TrainingPipelineConfig()

    data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    print(data_ingestion_config.to_dict())

    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
    data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,data_transformation_config=data_transformation_config)
    data_transformation_artifact = data_transformation.initiate_data_transformation()


    model_trainer_config  = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
    model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
    model_trainer_artifact = model_trainer.initiate_model_trainer()