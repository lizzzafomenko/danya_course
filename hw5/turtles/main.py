#!/opt/conda/envs/dsenv/bin/python3

import sys
import os
import logging
from joblib import dump
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import mean_squared_error
import lightgbm as lgb

from scipy.stats import pearsonr

import mlflow
import mlflow.sklearn

df_condition = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-03/tortoise_body_condition_cleaned.csv')
df_clutch = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-03/clutch_size_cleaned.csv')

df_condition['individual'] = df_condition['individual'].astype(str)
df_clutch['individual'] = df_clutch['individual'].astype(str)

df_clutch['year'] = pd.to_datetime(df_clutch['date']).dt.year

df_agg = df_condition.groupby(['individual']).agg({
    'body_mass_grams': 'mean',
    'body_condition_index': 'mean',
    'straight_carapace_length_mm': 'mean',
    'season': lambda x: x.mode()[0] if not x.mode().empty else np.nan, 
    'locality': lambda x: x.mode()[0] if not x.mode().empty else np.nan,
    'sex': 'first' 
}).reset_index()
df = df_clutch.merge(df_agg, on=['individual'], how='inner')

categorical_cols = ['season', 'sex', 'locality']
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_array = encoder.fit_transform(df[['season', 'sex', 'locality_x', 'locality_y']])
encoded_df = pd.DataFrame(
    encoded_array,
    columns=encoder.get_feature_names_out(['season', 'sex', 'locality_x', 'locality_y']),
    index=df.index
)

df = df.drop(columns=['season', 'sex', 'locality_x', 'locality_y', 'date']).join(encoded_df)

X = df.drop(['eggs', 'individual'], axis = 1)
y = df['eggs']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

mlflow.set_experiment("яички черепашек")
with mlflow.start_run(run_name="LinearRegression"):
    mlflow.log_param("model_type", "LinearRegression")
    params = {"tol": 1e-06}
    mlflow.log_params(params)
    model = LinearRegression(**params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    corr, pval = pearsonr(y_test, y_pred)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("Pearson Correlation Coefficient", corr)
    mlflow.log_metric("Pearson Correlation P-value", pval)
    mlflow.sklearn.log_model(model, "model")

with mlflow.start_run(run_name="LGBMRegressor"):
    mlflow.log_param("model_type", "LGBMRegressor")
    params = {"n_estimators": 100,  "max_depth": 2, "learning_rate": 0.05, "min_child_samples": 2, "colsample_bytree": 0.8}
    mlflow.log_params(params)
    boosting = lgb.LGBMRegressor(**params)
    boosting.fit(X_train, y_train)
    y_pred = boosting.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    corr, pval = pearsonr(y_test, y_pred)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("Pearson Correlation Coefficient", corr)
    mlflow.log_metric("Pearson Correlation P-value", pval)
    mlflow.sklearn.log_model(model, "model")