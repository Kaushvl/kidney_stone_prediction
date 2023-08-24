import pandas as pd
import numpy as np
from ksp.entity import artifact_entity,config_entity
from ksp.exception import CustomException
import os,sys
from ksp.config import TARGET_COLUMN
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from ksp import utils


class DataTransformation:
   
    def __init__(self, data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                    data_transformation_config : config_entity.DataTransformationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        
        except  Exception as e:
            raise CustomException(e, sys)
        
    def handling_outliers(self,base_df,working_df):
        try:

            factor = 1.5
            q1 = np.percentile(base_df,25)
            q3 = np.percentile(base_df,75)
            iqr = q3 - q1
            lower_bound = q1 - (factor* iqr)
            upper_bound = q3 + (factor* iqr)

            # treated_data = working_df.copy()
            working_df[(base_df < lower_bound) | (base_df> upper_bound)] = np.NAN

            return working_df
        
        except  Exception as e:
            raise CustomException(e, sys)
        
    @classmethod   
    def get_data_transformer_object(cls)->Pipeline:
        try:
            knn_imputer = KNNImputer(n_neighbors=3)
            std_scaler = StandardScaler()
            pipeline = Pipeline(steps=[
                ('Imputer',knn_imputer),
                ('RobustScaler',std_scaler)
            ])
            return pipeline

        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            base_df = pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)


            train_df = self.handling_outliers(base_df,train_df)
            test_df = self.handling_outliers(base_df,test_df)

            print(train_df.columns)
            input_feature_train_df = train_df.drop(columns= [TARGET_COLUMN])
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])


            
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,target_feature_train_df]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_df]


            utils.save_numpy_array_data(filepath=self.data_transformation_config.transform_train_path,array=train_arr)
            utils.save_numpy_array_data(filepath=self.data_transformation_config.transform_test_path,array=test_arr)

            utils.save_object(filepath=self.data_transformation_config.tranform_object_path,obj=transformation_pipeline)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.tranform_object_path,
                transform_train_path=self.data_transformation_config.transform_train_path,
                transform_test_path=self.data_transformation_config.transform_test_path,
            )

            return data_transformation_artifact


        except Exception as e:
            raise CustomException(e, sys)


