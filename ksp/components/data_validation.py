import numpy as np
from ksp.entity import config_entity,artifact_entity
from ksp import utils
from ksp.config import TARGET_COLUMN
from ksp.exception import CustomException
import os,sys
from ksp.logger import logging
import pandas as pd




class DataValidation:
    try:
        def __init__(self,
                    data_validation_config: config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact,):
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validaiton_error = dict()
    except  Exception as e: 
        raise CustomException(e, sys)
            
    def handling_outliers(data):
        factor = 1.5
        q1 = np.percentile(data,25)
        q3 = np.percentile(data,75)
        iqr = q3 - q1
        lower_bound = q1 - (factor* iqr)
        upper_bound = q3 + (factor* iqr)

        treated_data = data.copy()
        treated_data[(data < lower_bound) | (data> upper_bound)] = np.NAN

        return treated_data
    
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            logging.info('checking for missing columns')
            base_columns = base_df.columns
            current_columns = current_df.columns
            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f'{base_column} is missing')
                    missing_columns.append(base_column)
                
                if len(missing_columns)>0:
                    self.validaiton_error[report_key_name] = missing_columns
                    return False
                return True
            
        except Exception as e:
            raise CustomException(e, sys)  
        

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:

        try:
            base_df = pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)

            base_df = self.handling_outliers(base_df)

            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            train_df = self.handling_outliers(train_df)

            test_df = self.handling_outliers(test_df)

            train_df_status = self.is_required_columns_exists(base_df=base_df,current_df=train_df,report_key_name="MISSING_COL_IN_TRAIN_FILE")

            test_df_status = self.is_required_columns_exists(base_df=base_df,current_df=test_df,report_key_name="MISSING_COL_IN_Test_FILE")

            utils.write_yaml_file(filepath=self.data_validation_config.report_file_path,
                                  data=self.validaiton_error)
            
            


        except Exception as e:
            raise CustomException(e, sys)

    
