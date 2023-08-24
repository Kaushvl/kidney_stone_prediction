from ksp.logger import logging
import pymongo.mongo_client
from ksp.config import mongo_client 
from ksp.exception import CustomException
import sys,os,dill
import pandas as pd
import numpy as np
import pickle

def get_collection_as_dataframe(database_name:str,collection_name:str):
    try:
        logging.info(f"Reading data from database :{database_name} and collection: {collection_name}")
        df = pd.DataFrame(mongo_client[database_name][collection_name].find())
        logging.info(f"Dataframe shape is {df.shape}")
        if "_id" in df.columns:
            logging.info("droping _id column")
            df.drop(columns="_id",inplace=True)
        logging.info(f"rows and columns in df {df.shape}")
        return df

    except Exception as e:
        raise CustomException(e, sys)
    
def save_numpy_array_data(filepath:str,array:np.array):
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise CustomException(e, sys)
    
def load_numpy_array_data(filepath:str)->np.array:
    try:
        with open(filepath,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    

def save_object(filepath:str,obj:object)->None:
    try:
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,'wb') as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    


def load_object(filepath:str)-> object:
    try:
        if not os.path.exists(filepath):
            raise Exception(f"filepath :{filepath} doesn't exsist ")
        with open(filepath,'rb') as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

def load_model(filepath:str)-> object:
    try:
        if not os.path.exists(filepath):
            raise Exception(f"filepath :{filepath} doesn't exsist ")
        with open(filepath,'rb') as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns :
                if df[column].dtypes != 'O':
                    df[column] = df[column].astype('float')
        return df
    except Exception as e:
        raise CustomException(e, sys)