import re
import pdfkit
from collections import OrderedDict
from flask import render_template
from weasyprint import HTML

def generate_email_attachment(args):
	identity_number = args['tenant_id']
	email = args['email']
	name = args['name']
	surname = args['surname']
	gender = args['gender']
	building = args['building']
	building_name = building['name']+', '+building['address_suburb']+', '+building['address_city']
	room = args['room']
	room_id = room['room_id']
	room_price = room['price']
	institution = args['institution']
	
	ordered_attachment = OrderedDict()
	ordered_attachment["IDENTITY NUMBER"] = identity_number
	ordered_attachment["EMAIL"] = email
	ordered_attachment["NAME"] = name
	ordered_attachment["SURNAME"] = surname
	ordered_attachment["GENDER"] = gender
	ordered_attachment["BUILDING"] = building_name
	ordered_attachment["ROOM"] = room_id
	ordered_attachment["PRICE"] = room_price
	ordered_attachment["INSTITUTION"] = institution

	html_str = render_template('booking_reference.html',result = ordered_attachment)
	email_txt = "Thank you for choosing to come to stay with us, we have received your application. It will be processed once you have paid the booking fee"
	email_txt = email_txt+". Please find attached document containing details your booking \n \n \n Kind Regards \n Campus Africa"
	email_txt = "Dear "+name+"\n \n \n"+email_txt


	try:
		pdfkit.from_string(html_str,'api/attachments/ca_booking.pdf')
		return email_txt
	
	except:
		print("Error occured when trying to generate email attachment")


