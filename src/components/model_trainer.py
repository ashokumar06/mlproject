import  os 
import sys 
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor ,GradientBoostingRegressor,AdaBoostRegressor

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging


from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array,preprocessor_path):
        try:
            logging.info("Splitting training and test data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1], 
                train_array[:,-1], 
                test_array[:,:-1], 
                test_array[:,-1]
                )
            logging.info("Splitting completed")
            logging.info("Training the model")

            models = {
                "RandomForestRegressor": RandomForestRegressor(),
                "GradientBoostingRegressor": GradientBoostingRegressor(),
                "AdaBoostRegressor": AdaBoostRegressor(),
                "LinearRegression": LinearRegression(),
                "KNeighborsRegressor": KNeighborsRegressor(),
                "DecisionTreeRegressor": DecisionTreeRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoostRegressor": CatBoostRegressor(silent=True)
            }

            params = {
                "RandomForestRegressor": {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [None, 10, 20],
                    "min_samples_split": [2, 5, 10]
                },
                "GradientBoostingRegressor": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 0.2],
                    "max_depth": [3, 5, 7]
                },
                "AdaBoostRegressor": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.1, 0.5, 1.0]
                },
                "KNeighborsRegressor": {
                    "n_neighbors": [3, 5, 7],
                    "weights": ['uniform', 'distance']
                },
                "DecisionTreeRegressor": {
                    "max_depth": [None, 10, 20],
                    "min_samples_split": [2, 5, 10]
                },
                "XGBRegressor": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 0.2],
                    "max_depth": [3, 5, 7]
                },
                "CatBoostRegressor": {
                    "iterations": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 0.2],
                    "depth": [4, 6, 8]
                }
            }
            
            
            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models, params)
            logging.info("Model training completed")
            
            # save the best model
            # Sort the models based on 'R2 Score'
            model_report_sorted = sorted(model_report.items(), key=lambda x: x[1]['R2 Score'], reverse=True)

            best_model_name, best_model_info = model_report_sorted[0]
            best_model_score = best_model_info['R2 Score']

            if best_model_score < 0.6:
                raise CustomException("No best model found with R2 score > 0.6")
            logging.info(f"Best model found: {best_model_name} with R2 score: {best_model_score}")
            

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=models[best_model_name]
            )
            logging.info(f"Model saved at {self.model_trainer_config.trained_model_file_path}")

            predicted = models[best_model_name].predict(X_test)
            r2 = r2_score(y_test, predicted)

            return r2

        except Exception as e:
            raise CustomException(e, sys)