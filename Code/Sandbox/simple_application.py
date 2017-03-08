
### This application will work as-is in EB, but fails as soon as we
### re-type message to a Numpy Array!!!!

# Web service dependencies
from flask import Flask, request, abort, jsonify

#~~~~~~~~~~~~~~~~~~~~~~~~~
#### Define Flask API ####
#~~~~~~~~~~~~~~~~~~~~~~~~~

application = Flask(__name__)

@application.route('/rideshare', methods=['POST'])
def make_predict():

    #all kinds of error checking should go here
    data = request.get_json(force=True) # <----------- Pick up the API request in JSON

    #print(data)

    message = [int(data['first']), int(data['second'])]
    calc = sum(message)
    #print(message)
    #return our prediction
    output = {'ride_count': int(calc)}
    return jsonify(results=output)   # <-------------------------------------------------------------- Send response

if __name__ == '__main__':
    application.run(host="0.0.0.0", port = 9000, debug = True)
