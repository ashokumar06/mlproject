import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "proprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformation(self):
        """
        This function is responsible for data transformations.
        """
        try:
            numerical_fea = ['reading score', 'writing score']
            categorical_fea = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']
           
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(handle_unknown='ignore')),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            
            logging.info("Both column standard scaling and encoding completed")
            
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_fea),
                    ("cat_pipeline", cat_pipeline, categorical_fea)
                ]
            )
            
            return preprocessor
            
        except Exception as e:
            raise CustomException(e, sys)
            
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Read train and test data completed")
            
            # Preprocessing object
            preprocessing_obj = self.get_data_transformation()
            
            target_column_name = 'math score'
            numerical_fea = ['reading score', 'writing score']
            
            # Splitting the data into input and target features
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]
           
            logging.info("Applying preprocessing object on training and testing dataframe")
            
            # Apply the transformation to the data
            input_feature_train_arry = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arry = preprocessing_obj.transform(input_feature_test_df)
            
            # Combine features with target for model training
            train_arr = np.c_[input_feature_train_arry, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arry, np.array(target_feature_test_df)]
            
            # Save the preprocessing object for future use
            logging.info("Saving preprocessing object")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            
        except Exception as e:
            raise CustomException(e, sys)