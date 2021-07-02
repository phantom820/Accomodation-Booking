import psycopg2


'''temporary'''
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
POSTGRES_DATABASE="accomodation_management"
POSTGRES_USERNAME="postgres"
POSTGRES_PASSWORD="postgres"

class Database:
	def __init__(self):
		self.conn = psycopg2.connect(user=POSTGRES_USERNAME, password=POSTGRES_PASSWORD,
                                  host=POSTGRES_HOST,port=POSTGRES_PORT,database=POSTGRES_DATABASE)

	# get units filtering using parameters
	def get_units(self,gender,type_,building):
		query = """ SELECT* from bookings.units where gender=(%s) and type=(%s) and building=(%s)"""
		query_params = (gender,type_,building)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			query_results = []
			row = cur.fetchone()
			while row is not None:
				unit_id,gender,type_,building = row
				unit = {'unit_id':unit_id,'gender':gender,'type':type_,'building':building}
				query_results.append(unit)
				row = cur.fetchone()
			cur.close()
			return query_results
		except (Exception, psycopg2.Error) as error:
			cur.close()
			print("Failed to select records", error)
		
	# get a room with specified room_id
	def get_room(self,room_id):
		query = """ SELECT units.unit_id,room_id,type,price FROM bookings.units INNER JOIN bookings.rooms ON bookings.units.unit_id = bookings.rooms.unit_id AND bookings.rooms.room_id=(%s)"""
		query_params = (room_id,)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			query_results = []
			row = cur.fetchone()
			room = {}
			if row is not None:
				unit_id,room_id,type_,price = row
				room = {'unit_id':unit_id,'room_id':room_id,'type':type_,'price':price}
				query_results.append(room)
			cur.close()
			return query_results

		except (Exception, psycopg2.Error) as error:
			cur.close()
			print("Failed to select records", error)

	# get rooms filtering using the params
	def get_rooms(self,gender,type_,building,occupied):
		query = """ SELECT units.unit_id,room_id,type,price,building FROM bookings.units INNER JOIN bookings.rooms ON bookings.units.unit_id = bookings.rooms.unit_id AND 
		bookings.units.gender=(%s) AND bookings.units.type = (%s) AND bookings.units.building = (%s) AND bookings.rooms.occupied=(%s)"""
		query_params = (gender,type_,building,occupied)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			query_results = []
			row = cur.fetchone()
			while row is not None:
				unit_id,room_id,type_,price,building = row
				room = {'unit_id':unit_id,'room_id':room_id,'type':type_,'price':price,'building':building}
				query_results.append(room)
				row = cur.fetchone()
			cur.close()
			return query_results

		except (Exception, psycopg2.Error) as error:
			cur.close()
			print("Failed to select records", error)

	# update a room occupation
	def update_room(self,room_id,occupied):
		query = """ UPDATE bookings.rooms SET occupied=(%s) where bookings.rooms.room_id = (%s)"""
		query_params = (occupied,room_id)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			cur.close()
			if cur.rowcount>0:
				return {'status':'update successful'}
			
			return {'status':'update failed'}
		

		except (Exception, psycopg2.Error) as error:
			cur.close()
			print("Failed to update records", error)

	# get a room with specified room_id
	def get_tenant(self,tenant_id):
		query = """ SELECT* FROM bookings.tenants WHERE tenant_id=(%s)"""
		query_params = (tenant_id,)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			row = cur.fetchone()
			query_results = []
			if row is not None:
				tenant_id,name,surname,gender,email,contact,room_id,approved = row
				tenant = {'tenant_id':tenant_id,'name':name,'surname':surname,'gender':gender,'email':email,
				'contact':contact,'room_id':room_id,"approved":approved}
				query_results.append(tenant)
			cur.close()
			return query_results

		except (Exception, psycopg2.Error) as error:
			cur.close()
			print("Failed to select records", error)

	# add a tenant
	def add_tenant(self,tenant):
		tenant_insert_query = """INSERT INTO bookings.tenants(tenant_id,name,surname,gender,email,contact,room_id,approved)
		values(%s,%s,%s,%s,%s,%s,%s,%s)"""
		tenant_insert_params = (tenant['tenant_id'],tenant['name'],tenant['surname'],tenant['gender'],tenant['email'],
			tenant['contact'],tenant['room_id'],False)
		room_update_query = """UPDATE bookings.rooms SET occupied=true WHERE room_id=(%s)"""
		room_update_params = (tenant['room_id'].upper(),)
		details_query = """INSERT INTO bookings.details(tenant_id,institution,funding,booking_date) values(%s,%s,%s,current_date)"""
		details_params = (tenant['tenant_id'],tenant['institution'],tenant['funding'])

		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(tenant_insert_query,tenant_insert_params)
			cur.execute(room_update_query,room_update_params)
			cur.execute(details_query,details_params)

			conn.commit()
			cur.close()
			if cur.rowcount>0:
				return {'status':'insertion successful'}
			
			return {'status':'insertion failed'}

		except (Exception, psycopg2.Error) as error:
			cur.close()
			print("Failed to update records", error)
		
	# close db connection
	def close(self):
		self.conn.close()
