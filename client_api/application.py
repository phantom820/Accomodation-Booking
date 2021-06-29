from flask import Flask,request
from flask import jsonify
from flask_restful import abort
from database import Database
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)
db = Database()

@app.route('/api/')
def home():
    return jsonify('home')

@app.route('/api/rooms/<room_id>',methods=['GET'])
def get_room(room_id): 
    room = db.get_room(room_id)
    return jsonify(room)

@app.route('/api/rooms/',methods = ['GET'])
def get_rooms():
    gender = request.args.get('gender')
    type_ = request.args.get('type')
    building = request.args.get('building')
    occupied = request.args.get('occupied')
    rooms = db.get_rooms(gender,type_,building,occupied)
    return jsonify(rooms)

@app.route('/api/room',methods=['PUT'])
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

if __name__ == '__main__':
    app.run(debug=True)
