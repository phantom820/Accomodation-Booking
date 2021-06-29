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
		print(room_id)
		query = """ SELECT units.unit_id,room_id,type,price FROM bookings.units INNER JOIN bookings.rooms ON bookings.units.unit_id = bookings.rooms.unit_id AND bookings.rooms.room_id=(%s)"""
		query_params = (room_id,)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			query_results = []
			row = cur.fetchone()
			unit_id,room_id,type_,price = row
			room = {'unit_id':unit_id,'room_id':room_id,'type':type_,'price':price}
			cur.close()
			return room

		except (Exception, psycopg2.Error) as error:
			cur.close()
			print("Failed to select records", error)

	# get rooms filtering using the params
	def get_rooms(self,gender,type_,building,occupied):
		query = """ SELECT units.unit_id,room_id,type,price FROM bookings.units INNER JOIN bookings.rooms ON bookings.units.unit_id = bookings.rooms.unit_id AND 
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
				unit_id,room_id,type_,price = row
				room = {'unit_id':unit_id,'room_id':room_id,'type':type_,'price':price}
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
			print("Failed to select records", error)

	# close db connection
	def close(self):
		self.conn.close()
