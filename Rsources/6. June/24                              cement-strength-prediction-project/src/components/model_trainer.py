import os
import sys
from dataclasses import dataclass

from sklearn.pipeline import Pipeline, make_pipeline

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBClassifier

from src.exception import CustomException
from src.logger import logging
from src.utils import  load_object, save_object, upload_file, read_yaml_file, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")
    model_config_file_path =os.path.join("config", "model.yaml")


class CustomModel:
    def __init__(self, preprocessing_object, trained_model_object):
        self.preprocessing_object = preprocessing_object

        self.trained_model_object = trained_model_object

    def predict(self, X):
        transformed_feature = self.preprocessing_object.transform(X)

        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    
    def finetune_best_model(self,
                            best_model_object:object,
                            best_model_name,
                            X_train,
                            y_train,
                            ) -> object:
        
        try:

            model_param_grid = read_yaml_file(self.model_trainer_config.model_config_file_path)["model_selection"]["model"][best_model_name]["search_param_grid"]


            grid_search = GridSearchCV(
                best_model_object, param_grid=model_param_grid, cv=5, n_jobs=-1, verbose=1 )
            
            grid_search.fit(X_train, y_train)

            best_params = grid_search.best_params_

            print("best params are:", best_params)

            finetuned_model = best_model_object.set_params(**best_params)
            

            return finetuned_model
        
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_model_trainer(self, train_array, test_array, preprocessor_path):
        try:
            logging.info(f"Splitting training and testing input and target feature")

            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                        'Linear Regression': LinearRegression(),
                        'Ridge Regression': Ridge(),
                        'Lasso Regression': Lasso(),
                        'Random Forest Regression': RandomForestRegressor(),
                        'Gradient Boosting Regression':GradientBoostingRegressor()
                        }

            logging.info(f"Extracting model config file path")


            
            preprocessor = load_object(file_path=preprocessor_path)



            logging.info(f"Extracting model config file path")

            model_report: dict = evaluate_models(X=x_train, y=y_train, models=models)

            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]


            best_model = self.finetune_best_model(
                best_model_name= best_model_name,
                best_model_object= best_model,
                X_train= x_train,
                y_train= y_train
            )

            best_model.fit(x_train, y_train)
            y_pred = best_model.predict(x_test)
            best_model_score = r2_score(y_test, y_pred)

            if best_model_score < 0.6:
                raise Exception("No best model found with an accuracy greater than the threshold 0.6")
            
            logging.info(f"Best found model on both training and testing dataset")

 
            custom_model = CustomModel(
                preprocessing_object=preprocessor,
                trained_model_object=best_model,
            )

            logging.info(
                f"Saving model at path: {self.model_trainer_config.trained_model_file_path}"
            )

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=custom_model,
            )

          

            upload_file(
                from_filename=self.model_trainer_config.trained_model_file_path,
                to_filename="model.pkl",
                bucket_name="cement-strength",
            )

            return best_model_score

        except Exception as e:
            raise CustomException(e, sys)
