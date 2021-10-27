import pickle

import pandas as pd 
import numpy as np


from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

output_file = 'catboostreg.bin'

# Reading the data
data = pd.read_csv(r'C:\Users\User\Desktop\midterm-project\midterm-project\data\cleaned_data.csv')

# Label Encoding
label_encoded_columns = ['area', 'country']
le = LabelEncoder()

for column in label_encoded_columns:
    data[column] = le.fit_transform(data[column])

# Train Test Split
data_full_train, data_test = train_test_split(data, random_state =25, test_size = 0.2, shuffle = True)
data_full_train = data_full_train.reset_index(drop = True)
data_test = data_test.reset_index(drop = True)

y_full_train = data_full_train['totalyearlycompensation']
y_test = data_test['totalyearlycompensation'] 

del data_full_train['totalyearlycompensation']
del data_test['totalyearlycompensation']

#Training the model
# We don't need to use cross-validation since we have cross-validated + we have optimised the parameters 

print('Training the final model:')
# One-Hot Encoding for training data
dicts_full_train = data_full_train.to_dict(orient = 'records')

dv = DictVectorizer(sparse = False)
X_full_train = dv.fit_transform(dicts_full_train)

# Model = cbr, or CatBoostRegressor
cbr = CatBoostRegressor(task_type = 'GPU', depth = 2, learning_rate = 0.01, bagging_temperature = 3, l2_leaf_reg = 0.002, silent = True)
cbr.fit(X_full_train, y_full_train)

# One-Hot Encoding for test data 
dicts_test = data_test.to_dict(orient = 'records')

dv = DictVectorizer(sparse = False)
X_test = dv.fit_transform(dicts_test)

y_pred = cbr.predict(X_test)

def rmse(y_pred, y_test):
    score = float(mean_squared_error(y_pred, y_test))** 0.5
    return score 

# Returning RMSE score
score = rmse(y_pred, y_test)
print('Done!')
print('RMSE score: ' + str(round(score,3)))

with open(output_file, 'wb') as f_out:
    pickle.dump((dv, cbr), f_out)

print(f'the model is saved to {output_file}')