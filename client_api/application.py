from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse,abort
from database import Database


app = Flask(__name__)
api = Api(app)
db = Database()

# rooms list
class RoomsListApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('gender', type = str, location = 'json',default='Male')
        self.reqparse.add_argument('type', type = str, location = 'json',default='3')
        self.reqparse.add_argument('building', type = str, location = 'json',default='49J')
        self.reqparse.add_argument('occupied',type = bool,location = 'json',default=False)
        self.db = db
        super(RoomsListApi,self).__init__()
    
    def get(self):
        args = self.reqparse.parse_args()
        
        for arg in args:
            if arg is None:
                print(arg,' missing')
                abort(404)

        gender = args['gender']
        type_ = args['type']
        building = args['building']
        occupied = args['occupied']
        rooms = self.db.get_rooms(gender,type_,building,occupied)
        return rooms

# single room
class RoomApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('room_id', type = str, location = 'json')
        self.reqparse.add_argument('occupied', type = str, location = 'json')
        self.db = db
        super(RoomApi,self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        room_id = args['room_id']
        if room_id == None:
            print('Missing args')
            abort(404)
        room = db.get_room(room_id)
        return room

    def put(self):
        args = self.reqparse.parse_args()        
        for arg in args:
            if arg is None:
                print(arg,' missing')
                abort(404)
        room_id = args['room_id']
        occupied = args['occupied']
        result = self.db.update_room(room_id,occupied)
        return result

api.add_resource(RoomsListApi, '/rooms')
api.add_resource(RoomApi,'/room')

if __name__ == '__main__':
    app.run(debug=True)
