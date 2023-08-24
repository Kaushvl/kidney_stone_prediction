from ksp.logger import logging
from ksp.exception import CustomException
from ksp.entity import config_entity
import sys, os
from ksp.entity import artifact_entity
import pandas as pd
from ksp.utils import get_collection_as_dataframe
from ksp.components.data_transformation import DataTransformation
from sklearn.model_selection import train_test_split
from ksp.components.model_trainer import ModelTrainer

class DataIngestion:

    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> artifact_entity.DataIngestionArtifact:
        try:
            df: pd.DataFrame = get_collection_as_dataframe(database_name= "kidney_stone",collection_name = "kidney_stone_database")

            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            # print(df.shape)

            df = df.drop(columns=['id'])
            # print(df.shape)

            df.to_csv(self.data_ingestion_config.feature_store_file_path, index=False)

            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size)

            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)

            train_df.to_csv(self.data_ingestion_config.train_file_path,index=False)
            test_df.to_csv(self.data_ingestion_config.test_file_path,index=False)

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )

            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)

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