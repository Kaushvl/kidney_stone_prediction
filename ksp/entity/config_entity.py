import os,sys
from ksp.exception import CustomException
from dataclasses import dataclass
from datetime import datetime 

FILE_NAME = "data.csv"
TRAIN_FILE_PATH = "train.csv"
TEST_FILE_PATH = "test.csv"
TRANSFORM_OBJECT_PATH_NAME = "transformer.pkl"
MODEL_FILE_NAME = 'model.pkl'

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.database_name = "kidney_stone"
            self.collection_name = "kidney_stone_database"
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%y%m%d%H%M%S')}")
        except Exception as e:
            raise CustomException(e, sys)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name = "kidney_stone"
            self.collection_name = "kidney_stone_database"
            self.data_injestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_injestion")
            self.feature_store_file_path = os.path.join(self.data_injestion_dir,'feature_store',FILE_NAME)
            self.train_file_path = os.path.join(self.data_injestion_dir,'dataset',TRAIN_FILE_PATH)
            self.test_file_path = os.path.join(self.data_injestion_dir,'dataset',TEST_FILE_PATH)            
            self.test_size = 0.2

        except Exception as e:
            raise CustomException(e, sys)
        
    def to_dict(self)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise CustomException(e, sys)
        

class DataValidationConfig:
    def __init__(self,training_pipeline_config : TrainingPipelineConfig):
        try:
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_validation")
            self.report_file_path = os.paht.join(self.data_validation_dir,"report.yaml")
            self.base_file_path = os.path.join("data.csv")
        except  Exception as e:
            raise CustomException(e, sys)
        

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,'data_transformation')
            self.tranform_object_path = os.path.join(self.data_transformation_dir,"tranformer",TRANSFORM_OBJECT_PATH_NAME)
            self.transform_train_path = os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_PATH.replace("csv","npz"))
            self.transform_test_path = os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_PATH.replace("csv","npz"))

        except Exception as e:
            raise CustomException(e, sys)