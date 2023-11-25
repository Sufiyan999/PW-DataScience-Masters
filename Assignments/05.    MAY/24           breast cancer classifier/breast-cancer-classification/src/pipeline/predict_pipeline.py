import shutil
import os,sys
import pandas as pd
import pickle
from src.logger import logging
from src.exception import CustomException
import sys
from flask import request
from src.constant import *
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class PredictionPipelineConfig:
    prediction_output_dirname = "predictions"
    prediction_file_name = "predicted_file.csv"
    model_file_path = os.path.join(os.getcwd(), "artifacts/model.pkl")
    preprocessor_path = os.path.join(os.getcwd(),"artifacts/preprocessor.pkl")
    prediction_file_path = os.path.join(prediction_output_dirname,prediction_file_name)
    
class PredictionPipeline:
    def __init__(self,request):
        self.request = request
        self.utils = MainUtils()
        self.prediction_pipeline_config = PredictionPipelineConfig()
        
        
    def save_input_files(self):
        try:
            pred_file_input_dir = "prediction_artifacts"
            os.makedirs(pred_file_input_dir, exist_ok=True)            
            input_csv_file = self.request.files['file']
            pred_file_path = os.path.join(pred_file_input_dir, input_csv_file.filename)
            input_csv_file.save(pred_file_path)
            
            return pred_file_path
        
        except Exception as e:
            raise CustomException(e,sys)
        
        
        
        
    def predict(self, features):
        try:
            model = self.utils.load_object(self.prediction_pipeline_config.model_file_path)
            preprocessor = self.utils.load_object(self.prediction_pipeline_config.preprocessor_path)
            
            
            transformed_x = preprocessor.transform(features)
            preds = model.predict(transformed_x)
            
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def get_predicted_dataframe(self, input_dataframe_path):
        try:
            prediction_column_name = "target"
            input_dataframe = pd.read_csv(input_dataframe_path)
            
            for unwanted_column in ["index" ,"Unnamed: 0" ,"target","_id"]:
                input_dataframe =  input_dataframe.drop(columns=unwanted_column) if unwanted_column in input_dataframe.columns else input_dataframe

            predictions = self.predict(input_dataframe)
            input_dataframe[prediction_column_name] = [pred for pred in predictions]
            target_column_mapping = {0:"Benign", 1:"Malignant"}
            input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map(target_column_mapping)
            
            os.makedirs(self.prediction_pipeline_config.prediction_output_dirname, exist_ok=True)
            input_dataframe.to_csv(self.prediction_pipeline_config.prediction_file_path, index=False)
            logging.info("Predictions Completed")
            
            return input_dataframe
            
        except Exception as e:
            raise CustomException(e,sys)
        
     #run pipeline   
    def run_pipeline(self):
        try:
            input_csv_path = self.save_input_files()
            print("INPUT_CSV_PATH: ", input_csv_path)
            self.get_predicted_dataframe(input_csv_path)
            
            return self.prediction_pipeline_config
        
        except Exception as e:
            raise CustomException(e,sys)