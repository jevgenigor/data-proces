from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np

def train_model(features, labels):
    model = RandomForestClassifier()
    param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
    }
    grid_search = GridSearchCV(model, param_grid, cv=5)
    grid_search.fit(features, labels)
    return grid_search.best_estimator_

def predict(model, features):
    return model.predict(features)