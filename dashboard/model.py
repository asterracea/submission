from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

# Seleksi fitur yang relevan
features = ['season', 'weathersit', 'temp', 'hum', 'hr']
target = 'count'

# Encode categorical features
hour_df=pd.read_csv('cleaned_hour.csv')
hour_df_encoded = hour_df.copy()
hour_df_encoded['season'] = hour_df_encoded['season'].map({'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4})
hour_df_encoded['weathersit'] = hour_df_encoded['weathersit'].map({
    'Clear/Partly Cloudy': 1, 
    'Misty/Cloudy': 2, 
    'Light Snow/Rain': 3, 
    'Severe Weather': 4
})

# Split data into train and test sets
X = hour_df_encoded[features]
y = hour_df_encoded[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize numeric features (if necessary)
X_train[['temp', 'hum']] = X_train[['temp', 'hum']].clip(0, 1)
X_test[['temp', 'hum']] = X_test[['temp', 'hum']].clip(0, 1)
