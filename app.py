from flask import Flask, render_template, request, jsonify
import pymongo
import sys
import JSONEncoder

app = Flask(__name__)
# mongoDB connection
client_cloud = pymongo.MongoClient("mongodb+srv://root:root@cluster0.9bpnr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client_cloud["flaskAssignment"]
collection = client_cloud["students"]

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')

@app.route('/mongo', methods=['POST'])
def insertDoc():
    if (request.method=='POST'):
        name=request.json["name"]
        course=request.json["course"]
        duration=request.json["duration"]
        remarks=request.json["remarks"]
        isPlaced = request.json["placed"]
        try:
            record = {"name":name,"course":course,"duration":duration,"remarks":remarks,"isPlaced":isPlaced}
            database["students"].insert_one(record)
            result = {"Status":"Success","Msg":"Data inserted."}
            return jsonify(result)
        except Exception as e:
            return jsonify(e)

@app.route('/mongo', methods=['GET'])
def getAllDocuments():
    try:
        allData = list(database["students"].find())
        return jsonify(JSONEncoder.JSONEncoder().encode(allData))
    except Exception as e:
        return jsonify({"Msg":"Error"})

if __name__ == '__main__':
    app.run()
