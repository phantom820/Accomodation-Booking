import psycopg2
import numpy as np
import censusname
# from dotenv import load_dotenv
# import os

''' till we get fox for dotenv'''
# load_dotenv()
# POSTGRES_HOST = os.getenv('POSTGRES_HOST')
# POSTGRES_PORT = os.getenv('POSTGRES_PORT')
# POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
# POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
# POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')


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
	def seed_db(self,units,rooms,tenants):
		conn = self.conn
		try:
			cur = conn.cursor()
			units_query = """INSERT INTO bookings.units(unit_id,gender,type,building) values(%s,%s,%s,%s)"""
			for i in range(len(units)):
				units_query_params = units[i]
				cur.execute(units_query,units_query_params)

			rooms_query = """INSERT INTO bookings.rooms(room_id,unit_id,occupied,price) values(%s,%s,%s,%s)"""
			for i in range(len(rooms)):
				rooms_query_params = rooms[i]
				cur.execute(rooms_query,rooms_query_params)
			
			tenants_query = """INSERT INTO bookings.tenants(tenant_id,name,surname,gender,email,contact,room_id) values(%s,%s,%s,%s,%s,%s,%s)"""
			for i in range(len(tenants)):
				tenants_query_params =tenants[i]
				cur.execute(tenants_query,tenants_query_params)

			conn.commit()
			conn.close()

		except  (Exception, psycopg2.Error) as error:
			print(error)

	
	# close db connection
	def close(self):
		self.conn.close()



def synthetic_data(n):
	genders = ["MALE","FEMALE"]
	types = ["2","3"]
	buildings = ["49J","80J"]
	occupied = [False,True]
	division = {"2":['A','B'],'3':['A','B','C']}
	prices = {"2":5500,"3":4500}

	units = []
	rooms = []
	tenants = []
	count = 0
	identity = 9706095341086
	for i in range(n):
		index = int(np.round(np.random.uniform(0,1)))
		unit_id = buildings[index]+str(1101+count)
		gender = genders[index]
		type_ = types[index]
		building = buildings[index]
		unit = (unit_id,gender,type_,building)
		units.append(unit)
		room_divs = division[type_]
		for r in room_divs:
			idx = int(np.round(np.random.uniform(0,1)))
			room_id = unit_id+r	
			occ = occupied[idx]
			room = (room_id,unit_id,occ,prices[type_])	
			rooms.append(room)

			# there is a tenant
			if occ == True:
				tenant_id = str(identity)
				info = censusname.generate().split(' ')
				name,surname = info[0],info[1]
				email = name+surname+str(count)+'@gmail.com'
				contact = '07173399'+str(np.random.randint(10,40))
				tenant = (tenant_id,name,surname,gender,email,contact,room_id)
				tenants.append(tenant)
				identity = identity+1
		count = count+1

	return units,rooms,tenants


if __name__=='__main__':
	db = Database()
	units,rooms,tenants, = synthetic_data(500)
	db.seed_db(units,rooms,tenants)
	# print(tenants)