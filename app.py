from flask import Flask, render_template, request, jsonify, make_response
import pymongo
import sys
import JSONEncoder
import pandas as pd
import json

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

@app.route('/mongo', methods=['DELETE'])
def deleteDocument():
    try:
        id=request.json["id"]
        condel = {"_id":id}
        database["students"].delete_one(condel)
        return jsonify({"Status":"Success","Msg":"Data deleted."})
    except Exception as e:
        return jsonify({"Msg":"Error"})

@app.route('/mongo', methods=['PUT'])
def updateDocument():
    try:
        id=request.json["id"]
        newValue = request.json["nv"]
        condel = {"_id":id}
        database["students"].update_one(condel,newValue)
        return jsonify({"Status":"Success","Msg":"Data updated."})
    except Exception as e:
        return jsonify({"Msg":"Error"})
    
@app.route('/mongo/bulk', methods=['POST'])
def mongoBulkInsert():
    try:
        print(request.json['data'], file=sys.stderr)
        # database["courses"].insert_many([])
        return jsonify({"Status":"Success","Msg":"Data updated."})
    except Exception as e:
        return jsonify({"Msg":"Error"})
    
@app.route('/mongo/download', methods=['GET'])
def downloadDocuments():
    try:
        allData = list(database["students"].find())
        df=pd.DataFrame(allData)
        f=json.dumps(allData)
        resp = make_response(df.to_csv(JSONEncoder.JSONEncoder().encode(f)))
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    except Exception as e:
        print(e,file=sys.stderr)
        return jsonify({"Msg":"Error"})
    
if __name__ == '__main__':
    app.run()
