import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformationConfig,DataTransformation
from src.components.model_trainer import ModelTrainerConfig,ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts','train.csv')
    test_data_path: str=os.path.join('artifacts','test.csv')
    row_data_path: str=os.path.join('artifacts','row.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_congif=DataIngestionConfig()


    def initiate_data_ingestion(self):
        logging.info('Entered the data ingeston method or componet')
        try:
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('Read data successfully.')
            os.makedirs(os.path.dirname(self.ingestion_congif.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_congif.row_data_path,index=False,header=True)

            logging.info('train test split initiated')

            train_set,test_set=train_test_split(df,test_size=0.2 , random_state=42)

            train_set.to_csv(self.ingestion_congif.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_congif.test_data_path,index=False,header=True)

            logging.info("complate train test split in file ")

            return (
                self.ingestion_congif.train_data_path,
                self.ingestion_congif.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__=='__main__':
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    
    train_array, test_array ,preprocessor_path =data_transformation.initiate_data_transformation(train_data,test_data)


    model_trainer = ModelTrainer()
    r2 = model_trainer.initiate_model_trainer(train_array,test_array,preprocessor_path)
    print(r2)
