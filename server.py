from flask import Flask, request, jsonify
from flask_cors import CORS
import util
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)
util.load_saved_artifacts()

mongo_uri = 'mongodb+srv://superAdmin:superAdmin123@realestate.ivmmyaf.mongodb.net/realestate_app'
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db['realestates']

@app.route('/', methods=['GET'])
def welcome():
    response = jsonify({"message": "Welcome"})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
async def predict_home_price():

    data = request.json
    total_sqft = float(data['total_sqft'])
    location = data['location']
    bhk = int(data['bhk'])
    bath = int(data['bath'])
    product_id= data['id']

    estimated_price =  util.get_estimated_price(location,total_sqft,bhk,bath)

    query = {'_id': ObjectId(product_id)}
    update = {'$set': {'predictedPrice': estimated_price}}
    collection.update_one(query, update)

    response = jsonify({
        'estimated_price': estimated_price
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()