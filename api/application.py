from flask import Flask, json,request,make_response
from flask import render_template
from flask import jsonify
from database import Database
from flask_cors import CORS
from flask_mail import Mail, Message
import pandas as pd
import attachment
import json


# configuration  stuff
app = Flask(__name__)
with open('config/mail_config.json','r') as f:
            mail_config_json = json.load(f)
app.config['MAIL_SERVER'] = mail_config_json['MAIL_SERVER']
app.config['MAIL_PORT'] = mail_config_json['MAIL_PORT']
app.config['MAIL_USERNAME'] = mail_config_json['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = mail_config_json['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = mail_config_json['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = mail_config_json['MAIL_USE_SSL']
cors = CORS(app)
mail = Mail(app)
db = Database('config/db_config.json')

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('booking_reference.html',result = {'IDENTITY NUMBER':'9906095341086','NAME':'TSHEPO','SURNAME':'NKAMBULE'})

@app.route('/api/')
def email():
    msg = Message('Booking Receipt Confirmation', sender = 'phantomdanny980@gmail.com', recipients = ['nkambule773@gmail.com'])
    msg_txt = attachment.generate_attachment('')
    msg.body = msg_txt
    # attachment 
    with app.open_resource('attachments/ca_booking.pdf') as fp:
        msg.attach("ca_booking.pdf","application/octet-stream",fp.read())
    try:
        mail.send(msg)
        return "Sent"
    except:
        return "Failed to send" 

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
            return "FAILUR",404
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
    if result is not None:
        if result['status'] == 0:            
            email = Message('Booking Receipt Confirmation', sender = 'phantomdanny980@gmail.com', recipients = [args['email']])
            email_text = attachment.generate_email_attachment(args)
            if email_text is not None:
                email.body = email_text
                with app.open_resource('attachments/ca_booking.pdf') as fp:
                    email.attach("ca_booking.pdf","application/octet-stream",fp.read())
                try:
                    mail.send(email)
                    result['mail_sent'] = 0
                    return jsonify(result),201

                except:
                    print('Failed to send email with error : ')
                    result['mail_sent'] = 1
                    return jsonify(result),201

            else:
                print('Failed to send email with error : ')
                result['mail_sent'] = 1
                return jsonify(result),201

        else:
            return jsonify(result),400

    return jsonify({'status':1,'error message':'did not return'})

# save the html then convert it to pdf

if __name__ == '__main__':
    app.run(debug=True)

