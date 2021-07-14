import psycopg2
import json
import numpy as np
import pandas as pd

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
		
	
	def seed_db(self,buildings,units,rooms,tenants):
		conn = self.conn
		try:
			cur = conn.cursor()
			
			buildings_query = """INSERT INTO rem.buildings(building_id,name,address_street,address_suburb,address_city,address_postal_code) 
			values(%s,%s,%s,%s,%s,%s) """
			for index,row in buildings.iterrows():
				building_query_params = tuple(row.values)
				cur.execute(buildings_query,building_query_params)
		
			units_query = """INSERT INTO rem.units(unit_id,gender,type,building_id) values(%s,%s,%s,%s)"""
			for index,row in units.iterrows():
				units_query_params = tuple(row.values)
				cur.execute(units_query,units_query_params)

			rooms_query = """INSERT INTO rem.rooms(room_id,unit_id,occupied,price) values(%s,%s,%s,%s)"""
			for index,row in rooms.iterrows():
				rooms_query_params = tuple(row.values)
				cur.execute(rooms_query,rooms_query_params)

			
			tenants_query = """INSERT INTO rem.tenants(tenant_id,name,surname,gender,email,contact,approved,room_id) 
			values(%s,%s,%s,%s,%s,%s,%s,%s)"""
			for index,row in tenants.iterrows():
				row['contact'] = '0'+str(row['contact'])
				tenants_query_params = tuple(row.values)
				cur.execute(tenants_query,tenants_query_params)
			
			conn.commit()
			conn.close()

		except  (Exception, psycopg2.Error) as error:
			print(error)

	
	# close db connection
	def close(self):
		self.conn.close()


# load sythetic data from csv files
def load_data(buildings_path,units_path,rooms_path,tenants_path):
	buildings_df = pd.read_csv(buildings_path)
	units_df = pd.read_csv(units_path)
	rooms_df = pd.read_csv(rooms_path)
	tenants_df = pd.read_csv(tenants_path)

	return buildings_df,units_df,rooms_df,tenants_df

if __name__=='__main__':
	buildings_path = 'db/data/buildings.csv'
	units_path = 'db/data/units.csv'
	rooms_path = 'db/data/rooms.csv'
	tenants_path = 'db/data/tenants.csv'
	buildings,units,rooms,tenants = load_data(buildings_path,units_path,rooms_path,tenants_path)
	db = Database('config/db_config.json')
	db.seed_db(buildings,units,rooms,tenants)