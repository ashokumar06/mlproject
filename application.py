import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.components import *
from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages,request ,jsonify 

import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging

from src.pipeline.predict_pipeline import PredictPipeline , CustomData

# from src.pipeline.train_pipeline import TrainPipeline

application = Flask(__name__)
app = application 
app.secret_key = 'asdfghjnkml'

@app.route('/', methods=['GET'])
def index():
    try:
        return render_template('index.html')   
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)})

@app.route('/predict', methods=['POST', 'GET'])

def predict():
    try:

        if request.method == 'POST':
            
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('race_ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )
            data_df = data.get_data_as_data_frame()
            logging.info(f"Received data: {data_df}")

            print(data_df)

            predict_pipeline = PredictPipeline()
            result = predict_pipeline.predict(data_df)
            if result:
                flash('Prediction: {}'.format(result[0]))
            
            return render_template('home.html')

            

        else:
            return render_template('home.html')
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')