import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException


class TrainPipeline:
    def __init__(self) -> None:
        self.data_ingestion = DataIngestion()

        self.data_transformation = DataTransformation()

        self.model_trainer = ModelTrainer()

    def run_pipeline(self):
        try:
            train_path, test_path = self.data_ingestion.initiate_data_ingestion()

            (
                train_arr,
                test_arr,
                preprocessor_file_path,
            ) = self.data_transformation.initiate_data_transformation(
                train_file_path=train_path, test_file_path=test_path
            )

            r2_square = self.model_trainer.initiate_model_trainer(
                train_array=train_arr,
                test_array=test_arr,
                preprocessor_path=preprocessor_file_path,
            )
            print("training completed. Trained model score : ", r2_square)

        except Exception as e:
            raise CustomException(e, sys)
