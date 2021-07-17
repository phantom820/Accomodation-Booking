import psycopg2
import json

class Database:
	def __init__(self,db_config_path):
		try:
			with open(db_config_path,'r') as f:
				db_config_json = json.load(f)
				POSTGRES_HOST = db_config_json["HOST"]
				POSTGRES_PORT = db_config_json["PORT"]
				POSTGRES_DATABASE = db_config_json["DATABASE"]
				POSTGRES_USERNAME = db_config_json["USERNAME"]
				POSTGRES_PASSWORD = db_config_json["PASSWORD"]
				self.conn = psycopg2.connect(user=POSTGRES_USERNAME, password=POSTGRES_PASSWORD,
                                  host=POSTGRES_HOST,port=POSTGRES_PORT,database=POSTGRES_DATABASE)
		except:
			print('Exception occured could not load db config file at',db_config_path)

	# get buildings		
	def get_buildings(self):
		query = """SELECT row_to_json(t) FROM (SELECT* FROM REM.BUILDINGS)t;"""
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query)
			conn.commit()
			rows = cur.fetchall()	
			results = []
			if len(rows)!=0:
				for row in rows:
					results.append(row[0])
			cur.close()
			return results

		except (Exception, psycopg2.Error) as error:
			print("Failed to select building records with error : ",error)
		
		finally:
			conn.rollback()

			
	# get units filtering using parameters
	def get_units(self,gender,type_,building):
		query = """SELECT row_to_json(t) from (SELECT* FROM REM.UNITS WHERE gender=(%s) AND type=(%s) AND building_id=(%s))t;"""
		query_params = (gender,type_,building)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			results = []
			rows = cur.fetchall()
			if len(rows)!=0:
				for row in rows:
					results.append(row[0])
			cur.close()
			return results

		except (Exception, psycopg2.Error) as error:
			print("Failed to select  records of units with error : ", error)
		
		finally:
			conn.rollback()

	# get rooms filtering using the params
	def get_rooms(self,gender,type_,building_id,occupied):
		query = """SELECT row_to_json(t) from (SELECT* FROM rem.rooms INNER JOIN rem.units ON rooms.unit_id=units.unit_id 
						   	and units.gender=(%s) AND units.type=(%s) AND units.building_id=(%s) AND rem.rooms.occupied=(%s))t;"""
		query_params = (gender,type_,building_id,occupied)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			results = []
			rows = cur.fetchall()
			if len(rows)!=0:
				for row in rows:
					results.append(row[0])
			cur.close()
			return results

		except (Exception, psycopg2.Error) as error:
			print("Failed to select room records with error : ", error)
	
		finally:
			conn.rollback()


	# get a room with specified room_id
	def get_room(self,room_id):
		query = """select row_to_json(t) from (select* from rem.rooms INNER JOIN rem.units on rooms.unit_id=units.unit_id 
								 where rooms.room_id=(%s))t;"""
		query_params = (room_id,)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			results = []
			rows = cur.fetchall()
			if len(rows)!=0:
				for row in rows:
					results.append(row[0])
			cur.close()
			return results[0]
			
		except (Exception, psycopg2.Error) as error:
			print("Failed to select room record with error : ", error)

		finally:
			conn.rollback()

	# update a room occupation
	def update_room(self,room_id,occupied):
		query = """ UPDATE rem.rooms SET occupied=(%s) where room_id=(%s)"""
		query_params = (occupied,room_id)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			cur.close()
			if cur.rowcount>0:
				return {'status':0}
			return {'status':1}
		
		except (Exception, psycopg2.Error) as error:
			print("Failed to update record with error : ", error)

		finally:
			conn.rollback()

	# get a tenant with specified tenant_id
	def get_tenant(self,tenant_id):
		query = """select row_to_json(t) from (SELECT* FROM rem.tenants where tenant_id=%s)t"""
		query_params = (tenant_id,)
		conn = self.conn
		cur = conn.cursor()
		try:
			cur.execute(query,query_params)
			conn.commit()
			rows = cur.fetchall()
			return rows

		except (Exception, psycopg2.Error) as error:
			print("Failed to select tenant record with error : ", error)

		finally:
			conn.rollback()

	# add a tenant
	def add_tenant(self,tenant):
		tenant_insert_query = """INSERT INTO rem.tenants(tenant_id,name,surname,gender,email,contact,approved,room_id)
		values(%s,%s,%s,%s,%s,%s,%s,%s)"""
		tenant_insert_params = (tenant['tenant_id'],tenant['name'],tenant['surname'],tenant['gender'],tenant['email'],
			tenant['contact'],False,tenant['room_id'])
		room_update_query = """UPDATE rem.rooms SET occupied=true WHERE room_id=(%s)"""
		room_update_params = (tenant['room_id'].upper(),)
		details_query = """INSERT INTO rem.tenant_application_details(tenant_id,institution,funding,application_date) values(%s,%s,%s,current_date)"""
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
				return {'status':0}
			return {'status':1}

		except (Exception, psycopg2.Error) as error:
			print("Failed to add tenant record with error : ",error)

		finally:
			conn.rollback()
			
	# close db connection
	def close(self):
		self.conn.rollback()

# if __name__=='__main__':
# 	db = Database('config/db_config.json')
	# print(db.get_buildings())
	# print(db.get_units('MALE','2','1'))
	# print(db.get_rooms('MALE','2','2',False)[0])
	# print(db.get_room('11110A'))
	# print(db.update_room('11110A',False))
	# print(db.get_tenant("9706095341086"))