from flask import Flask,request,make_response
from flask import jsonify
from flask_restful import abort
from database import Database
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
db = Database('config/db_config.json')

@app.route('/api/')
def home():
    a = {'A':[1],'B':[2]}
    df = pd.DataFrame(a)
    return jsonify('home')

@app.route('/api/buildings/',methods=['GET'])
def get_buildings():
    buildings = db.get_buildings()
    return jsonify(buildings)

@app.route('/api/rooms/',methods=['GET'])
def get_rooms():
    gender = request.args.get('gender')
    type_ = request.args.get('type')
    building = request.args.get('building')
    occupied = request.args.get('occupied')
    rooms = db.get_rooms(gender,type_,building,occupied)
    return jsonify(rooms)

@app.route('/api/rooms/<room_id>',methods=['GET'])
def get_room(room_id): 
    room = db.get_room(room_id)
    return jsonify(room)

@app.route('/api/rooms',methods=['PUT'])
def put_room():
    arg_keys = ['room_id','occupied']
    args = request.get_json()        
    for arg_key in arg_keys:
        if arg_key not in args:
            abort(404)
    room_id = args['room_id']
    occupied = args['occupied']
    result = db.update_room(room_id,occupied)
    return jsonify(result)

@app.route('/api/tenants/<tenant_id>',methods=['GET'])
def get_tenant(tenant_id):
    tenant = db.get_tenant(tenant_id)
    return jsonify(tenant)

@app.route('/api/tenants/<tenant_id>/quote',methods=['GET'])
def get_quote(tenant_id):
    tenant = db.get_tenant(tenant_id)
    return jsonify(tenant)


@app.route('/api/tenants',methods=['PUT'])
def put_tenant():
    args = request.get_json()
    result = db.add_tenant(args)
    return jsonify(result),201


if __name__ == '__main__':
    app.run(debug=True)
