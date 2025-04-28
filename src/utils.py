import os 
import sys
import numpy as np
import pandas as pd
from src.exception import CustomException
import dill
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        model_report = {}
        
        # Iterate through models
        for model_name, model in models.items():
            # Get parameter grid for the current model
            param_grid = params.get(model_name, {})
            
            # Only use GridSearchCV if parameters are provided
            if param_grid:
                grid_search = GridSearchCV(
                    estimator=model,
                    param_grid=param_grid,
                    cv=3,
                    scoring='r2',
                    verbose=1
                )
                grid_search.fit(X_train, y_train)
                
                # Get the best model
                best_model = grid_search.best_estimator_
                
                # Log best parameters
                logging.info(f"Best parameters for {model_name}: {grid_search.best_params_}")
                
                # Store the best model in the models dictionary for later use
                models[model_name] = best_model
            else:
                # For models without hyperparameters like LinearRegression
                model.fit(X_train, y_train)
            
            # Make predictions using the best model (or fitted model if no hyperparameters)
            y_pred = models[model_name].predict(X_test)
            
            # Calculate and store metrics
            model_report[model_name] = {
                "R2 Score": r2_score(y_test, y_pred),
                "Mean Absolute Error": mean_absolute_error(y_test, y_pred),
                "Mean Squared Error": mean_squared_error(y_test, y_pred)
            }
            
            logging.info(f"{model_name} - R2 Score: {model_report[model_name]['R2 Score']}")
            
        return model_report
    except Exception as e:
        raise CustomException(e, sys)