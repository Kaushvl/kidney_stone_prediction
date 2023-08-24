from ksp.exception import CustomException
from ksp.logger import logging
import os,sys
import pickle
from ksp.utils import load_model
import pandas as pd


PREDICTION_FOLDER = 'batch_predictions'
PREDICTION_CSV = 'prediction_csv'
PREDICTION_FILE = 'output.csv'

ROOT_DIR = os.getcwd()
BATCH_PREDICTION = os.path.join(ROOT_DIR,PREDICTION_FOLDER,PREDICTION_CSV)



class batch_predictions:
    def __init__(self,input_file_path,
                 model_file_path,
                 transformer_file_path)->None:
        self.input_file_path = input_file_path
        self.model_file_path = model_file_path
        self.transformer_file_path = transformer_file_path
        

    def initiate_batch_prediction(self):
        try:
            with open(self.transformer_file_path,'rb') as f:
                processor = pickle.load(f)

            model = load_model(filepath=self.model_file_path)

            df = pd.read_csv(self.input_file_path)

            transformed_data = processor.transform(df)
            
            predictions = model.predict(transformed_data)

            df_prediction = pd.DataFrame(predictions,columns=['prediction'])

            BATCH_PREDICTION_PATH = BATCH_PREDICTION
            os.makedirs(BATCH_PREDICTION_PATH,exist_ok=True)
            
            CSV_PATH = os.path.join(BATCH_PREDICTION_PATH,PREDICTION_CSV)

            df_prediction.to_csv(CSV_PATH,index=False)

        except Exception as e:
            raise CustomException(e,sys)