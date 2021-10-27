import pickle
import numpy as np

from flask import Flask 
from flask import request
from flask import jsonify 

model_file = 'catboostreg.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)
    

app = Flask('salary_predictor')

@app.route('/predict', methods = ['POST'])
def predict():
    salary = request.get_json()
        
    X = dv.transform([salary])
    y_pred = model.predict(X)
    
    result = {
        'Predicted Salary': np.expm1(y_pred)[0]
    }
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0', port = 9696)
