#~~~~~~~~~~~~~~~~~~~~~~~~
#### Import packages ####
#~~~~~~~~~~~~~~~~~~~~~~~~

## ML Dependencies
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import boto, pickle

# Web service dependencies
from flask import Flask, request, abort, jsonify




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#### Get the model from S3 and unpickle
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
conn = boto.connect_s3() # <------------------------------------------------------------------- Connect to S3 and get the model
bucket = conn.get_bucket('pcar-phase3-demo')
rf_key = bucket.get_key('pickle_dumps/rideshare_rf_model.pkl')
rf_key.get_contents_to_filename('rideshare_rf_model.pkl')

# Now unpickle the model
rf = pickle.load(open('rideshare_rf_model.pkl', 'rb')) # <------------------------------------- Unpickle the model

print("This is Flask, I'm alive!!!")

#~~~~~~~~~~~~~~~~~~~~~~~~~
#### Define Flask API ####
#~~~~~~~~~~~~~~~~~~~~~~~~~

application = Flask(__name__)

@application.route('/rideshare', methods=['POST'])
def make_predict():
    #all kinds of error checking should go here
    data = request.get_json(force=True) # <------------------------------------------------- Pick up the API request in JSON
    predict_request = [data['weathersit'],data['weekday'],data['atemp'], data['hum'], data['windspeed']]
    predict_request = np.array(predict_request).reshape(1,-1)
    predict_request = pd.DataFrame(predict_request, columns = ('weathersit', 'weekday', 'atemp', 'hum', 'windspeed'))

    # Set formating
    def factorize_df(df, col_list):
        for col_name in col_list:
            df[col_name] = df[col_name].astype('category')
        return df
    predict_request = factorize_df(predict_request, ('weathersit', 'weekday')) # <--------------- Format the request for model

    # Dataframe goes into random forest, prediction comes out
    ride_count = rf.predict(predict_request)  # <----------------------------------------------- Run the request through prediction

    #return our prediction
    output = {'ride_count': int(ride_count[0])}
    return jsonify(results=output)   # <-------------------------------------------------------------- Send response

if __name__ == '__main__':
    application.run(host='0.0.0.0', port = 9000, debug = True)
