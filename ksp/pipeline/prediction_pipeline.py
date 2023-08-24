from ksp.exception import CustomException
from ksp.logger import logging
import os,sys
from ksp.utils import load_model
from ksp.entity import config_entity,artifact_entity
import pandas as pd


class PredictionPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            preprocessor_path = artifact_entity.DataTransformationArtifact.transform_object_path

            model_path = artifact_entity.ModelTrainerArtifact.model_path

            preprocessor = load_model(preprocessor_path)

            model = load_model(model_path)

            data_scaled = preprocessor.transform(features)

            pred = model.predict(data_scaled)

            return pred


        except Exception as e:
            raise CustomException(e, sys)
        
# gravity,ph,osmo,cond,urea,calc
class CustomData:
    def __init__(self,
                 gravity:float,
                 ph:float,
                 osmo:int,
                 cond:float,
                 urea:int,
                 calc:float):
        self.gravity = gravity
        self.ph = ph
        self.osmo = osmo
        self.cond = cond
        self.urea = urea
        self.calc = calc


    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "gravity":[self.gravity],
                "ph":[self.ph],
                "osmo":[self.osmo],
                "cond":[self.cond],
                "urea":[self.urea],
                "calc":[self.calc]
            }

            df = pd.DataFrame(custom_data_input_dict)
            
            return df

        except Exception as e:
            raise CustomException(e, sys)
        