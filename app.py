import os
from flask import Flask, request, jsonify, Response
import pymongo, json
from pymongo import Connection

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)

app.config.update(
    DEBUG = True,
)

#--------------------------------------
MONGODB_URI = 'mongodb://admin:admin@ds053658.mongolab.com:53658/iron_cacahe' 
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()
posts = db['rows']


#----------------------------------------
# controllers
#----------------------------------------
@app.route("/get_value", methods=['POST', 'GET'])
def get_value():
    cursor = posts.find({"db": "twitter_urls"})
    for doc in cursor:
        skip_value = doc["skip"]
    obj = {"skip": skip_value}
    response = json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': ')) 
    return Response(response,  mimetype='application/json')   

@app.route("/set_value", methods=['POST', 'GET'])
def update_value():
    rv = request.values
    skip_value = int(rv["skip_value"])
    #doc = posts.find_one({'crunchbase_slug':crunchbase_slug})
    response = posts.update({"db": "twitter_urls"}, {"$set": {"skip": skip_value}})
    status = {"success": True}
    response = json.dumps(status, sort_keys=False, indent=4, separators=(',', ': ')) 
    return Response(response,  mimetype='application/json')

#----------------------------------------
# launch
#----------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)