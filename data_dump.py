import pymongo
import pandas as pd
import json

client = pymongo.MongoClient("mongodb+srv://kvushvl:kaushalbro1@cluster0.ajqs2ox.mongodb.net/?retryWrites=true&w=majority")
db = client.text
DATA_FILE_PATH = ("C:\Projects\kidney_stone_pred\kidney_stone_prediction\kidney_stone_data.csv")
DATABASE_NAME = 'kidney_stone'
COLLECTION_NAME = 'kidney_stone_database'

if __name__ == '__main__':
    df = pd.read_csv(DATA_FILE_PATH)
    print(df.shape)
    df.reset_index(drop = True,inplace=True)
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)