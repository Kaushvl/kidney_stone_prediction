import pymongo
import pandas as pd
import numpy as np
import json,os,sys

class EnvironmentVariable:
    mongo_db_url = "mongodb+srv://kvushvl:kaushalbro1@cluster0.ajqs2ox.mongodb.net/?retryWrites=true&w=majority"


env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = 'target'
print("env_var, mongo_db_url")

# if __name__ == '__main__':
    # obj = EnvironmentVariable()
    # print(obj.mongo_db_url)