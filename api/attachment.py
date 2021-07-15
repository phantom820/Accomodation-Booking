import re
import pdfkit
from collections import OrderedDict
from flask import render_template

def generate_attachment(args):
	identity_number = args['tenant_id']
	email = args['email']
	name = args['name']
	surname = args['surname']
	gender = args['gender']
	building_obj = args['building']
	building = building_obj['name']+', '+building_obj['address_suburb']+', '+building_obj['address_city']
	room_obj = args['room_detail']
	room = room_obj['room_id']
	price = room_obj['price']
	institution = args['institution']
	
	ordered_attachment = OrderedDict()
	ordered_attachment["IDENTITY NUMBER"] = identity_number
	ordered_attachment["EMAIL"] = email
	ordered_attachment["NAME"] = name
	ordered_attachment["SURNAME"] = surname
	ordered_attachment["GENDER"] = gender
	ordered_attachment["BUILDING"] = building
	ordered_attachment["ROOM"] = room
	ordered_attachment["PRICE"] = price
	ordered_attachment["INSTITUTION"] = institution
	html = render_template('booking_reference.html',result = ordered_attachment)
	# text
	msg_txt = "Thank you for choosing to come to stay with us, we have received your application. It will be processed once you have paid the booking fee"
	msg_txt = msg_txt+". Please find attached document containing details your booking \n \n \n Kind Regards \n Campus Africa"
	msg_txt = "Dear "+name+"\n \n \n"+msg_txt
	# try to save
	try:
		f = open('api/attachments/ca_booking.html','w')
		f.write(html)
		f.close()
		pdfkit.from_url('api/attachments/ca_booking.html', 'api/attachments/ca_booking.pdf')
		return msg_txt
	except:
		print("Error occured when trying to generate attachment")


