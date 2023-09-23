import sys
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from zipfile import Path
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
import certifi
ca = certifi.where()

@dataclass
class DataIngestionConfig:
    artifact_folder = os.path.join(os.getcwd(),"artifacts")
    
class DataIngestion:
    def __init__(self):
        self.data_ingestion_config= DataIngestionConfig()
        self.utils = MainUtils()
        
    def export_collection_as_dataframe(self,collection_name, db_name):
        try:
            mongo_client = MongoClient("mongodb+srv://SufiyanisticGuy:sufi7000@cluster0.dcxialt.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=ca)
            collection = mongo_client[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            
            return df 
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def export_data_into_feature_store_file_path(self):
        try:
            logging.info(f"Exporting data from mongodb")
            raw_file_path = self.data_ingestion_config.artifact_folder
            os.makedirs(raw_file_path,exist_ok=True)
            
            breast_data = self.export_collection_as_dataframe(
                            collection_name="breast_cancer",
                            db_name="pwskills_project"
                            )
            
            logging.info(f"Saving exported data into feature store file path: {raw_file_path}")
            feature_store_file_path = os.path.join(raw_file_path,'breast_data.csv')
            breast_data.to_csv(feature_store_file_path,index=False)
            
            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_ingestion(self) -> Path:
        """
            Method Name :   initiate_data_ingestion
            Description :   This method initiates the data ingestion components of training pipeline 
            
            Output      :   train set and test set are returned as the artifacts of data ingestion components
            On Failure  :   Write an exception log and then raise an exception
            
            Version     :   1.2
            Revisions   :   moved setup to cloud
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        
        try:   
            feature_store_file_path = self.export_data_into_feature_store_file_path()
            
            logging.info("Got the data from mongodb")
            
            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )
            
            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e, sys) from e
        


if __name__ == "__main__":
     di = DataIngestion()
     feature_store_file_path  = di.initiate_data_ingestion()    
        