import sys
from typing import Dict, Tuple
import os
import pandas as pd
import pickle
import yaml
import boto3
from sklearn.base import BaseEstimator, TransformerMixin

from src.constant import *
from src.exception import CustomException
from src.logger import logging


class MainUtils:
    def __init__(self) -> None:
        pass

    def read_yaml_file(self, filename: str) -> dict:
        try:
            with open(filename, "rb") as yaml_file:
                return yaml.safe_load(yaml_file)

        except Exception as e:
            raise CustomException(e, sys) from e

    def read_schema_config_file(self) -> dict:
        try:
            schema_config = self.read_yaml_file(os.path.join("config", "schema.yaml"))

            return schema_config

        except Exception as e:
            raise CustomException(e, sys) from e

    

    @staticmethod
    def save_object(file_path: str, obj: object) -> None:
        logging.info("Entered the save_object method of MainUtils class")

        try:
            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)

            logging.info("Exited the save_object method of MainUtils class")

        except Exception as e:
            raise CustomException(e, sys) from e

    

    @staticmethod
    def load_object(file_path: str) -> object:
        logging.info("Entered the load_object method of MainUtils class")

        try:
            with open(file_path, "rb") as file_obj:
                obj = pickle.load(file_obj)

            logging.info("Exited the load_object method of MainUtils class")

            return obj

        except Exception as e:
            raise CustomException(e, sys) from e
   
    @staticmethod     
    def load_object(file_path):
        try:
            with open(file_path,'rb') as file_obj:
                return pickle.load(file_obj)
        except Exception as e:
            logging.info('Exception Occured in load_object function utils')
            raise CustomException(e,sys)
    
    


class MulticollinearityReducer(BaseEstimator, TransformerMixin):   # costum class for multicollinearity reduction algorithm (preprocessor)
    def __init__(self, correlation_threshold=0.95):
        self.correlation_threshold = correlation_threshold
        self.columns_to_drop = []

    def fit(self, X, y=None):
        # Calculate the correlation matrix
        correlation_matrix = X.corr()

        # Identify highly correlated pairs
        highly_correlated_pairs = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                if abs(correlation_matrix.iloc[i, j]) >= self.correlation_threshold:
                    pair = (correlation_matrix.columns[i], correlation_matrix.columns[j])
                    highly_correlated_pairs.append(pair)

        # Decide which column to drop (you can customize this logic)
        for col1, col2 in highly_correlated_pairs:
            # Here, you can implement your logic to decide which column to drop.
            # For example, you can choose to keep the column with the most significance.
            # self.columns_to_drop.append(col1)  # To drop col1
            self.columns_to_drop.append(col2)  # To drop col2

        return self

    def transform(self, X):
        # Drop the chosen columns from the DataFrame
        logging.info(f"Columns to drop: {self.columns_to_drop}")
        
        # Remove extra spaces from the left and make column names case-insensitive
        X_cleaned = X.rename(columns=lambda x: x.strip().lower())
        columns_to_drop_cleaned = [col.strip().lower() for col in self.columns_to_drop]
        
        # Drop the columns based on cleaned column names
        X_dropped = X_cleaned.drop(columns=columns_to_drop_cleaned)
        
        return X_dropped   