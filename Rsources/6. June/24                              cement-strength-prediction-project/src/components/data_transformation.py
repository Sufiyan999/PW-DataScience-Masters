import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTETomek
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, read_schema_config_file
import os


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    
        
    def apply_outliers_capping(self,dataframe:pd.DataFrame):
        """
            Method Name :   apply_outliers_capping
            Description :   This method reduces the outliers
            
            Output      :   a pd.DataFrame
            On Failure  :   Write an exception log and then raise an exception
            
            Version     :   1.2
            Revisions   :   moved setup to cloud
        """


        try:

            outliers_columns = read_schema_config_file()['outlier_columns']

            df = dataframe.copy()
            for column in outliers_columns:

                percentile25 = df[column].quantile(0.25)
                percentile75 = df[column].quantile(0.75)
                iqr = percentile75 - percentile25
                upper_limit = percentile75 + 1.5 * iqr
                lower_limit = percentile25 - 1.5 * iqr
                df.loc[(df[column]>upper_limit), column]= upper_limit
                df.loc[(df[column]<lower_limit), column]= lower_limit   
            

            return df

        except Exception as e:
            raise CustomException(e,sys)


    def get_data_transformer_object(self) -> object:
        try:
            

            # define the steps for the preprocessor pipeline
            imputer_step = ('imputer', KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan))
            scaler_step = ('scaler', StandardScaler())

            preprocessor = Pipeline(
                steps=[
                imputer_step,
                scaler_step
                ]
            )
            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)



    def initiate_data_transformation(self, 
                                     train_file_path: str,
                                     test_file_path: str):
        try:
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            target_column_name =  read_schema_config_file()['target_column']

            #training dataframe
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]


            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            preprocessor = self.get_data_transformer_object()


            transformed_input_train_feature = preprocessor.fit_transform(input_feature_train_df)

            transformed_input_test_feature =preprocessor.transform(input_feature_test_df)

            

           

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]

            save_object(self.data_transformation_config.preprocessor_obj_file_path,
                        obj= preprocessor)

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
