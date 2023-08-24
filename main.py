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
from ksp.components.data_ingestion import DataIngestion
from flask import Flask,render_template,request
from ksp.pipeline.prediction_pipeline import CustomData,PredictionPipeline
from prediction.batch import *
from ksp.pipeline.training_pipeline import Train


# preprocessor_path = config_entity.DataTransformationConfig().tranform_object_path
# 
# model_path = artifact_entity.ModelTrainerArtifact.model_path

upload_folder = 'batch_predictions/uploaded_csv'


# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gravity = float(request.form['gravity'])
#         ph = float(request.form['ph'])
#         osmo = int(request.form['osmo'])
#         cond = float(request.form['cond'])
#         urea = int(request.form['urea'])
#         calc = float(request.form['calc'])


#         cd = CustomData(gravity, ph, osmo, cond, urea, calc)
#         df = cd.get_data_as_dataframe()

#         return PredictionPipeline(df)
#     return 'render_template'

# if __name__ == '__main__':
#     app.run(debug=True)



app = Flask(__name__,template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gravity = float(request.form['gravity'])
        ph = float(request.form['ph'])
        osmo = int(request.form['osmo'])
        cond = float(request.form['cond'])
        urea = int(request.form['urea'])
        calc = float(request.form['calc'])

       
        cd = CustomData(gravity, ph, osmo, cond, urea, calc)
        df = cd.get_data_as_dataframe()

       
        prediction_pipeline = PredictionPipeline()
        result = prediction_pipeline.predict(df)
        
        return result 
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)