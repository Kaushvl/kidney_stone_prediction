from ksp.logger import logging
from flask import Flask,render_template,request
from ksp.pipeline.prediction_pipeline import CustomData,PredictionPipeline
from prediction.batch import *



upload_folder = 'batch_predictions/uploaded_csv'



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
        logging.info(result)
        return list(result)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)