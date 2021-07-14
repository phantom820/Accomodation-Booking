-- schema
CREATE SCHEMA IF NOT EXISTS rem
    AUTHORIZATION postgres;

-- buildings
CREATE TABLE rem.buildings (
	building_id VARCHAR(10) PRIMARY KEY,
	name VARCHAR(100),
	address_street VARCHAR(100),
	address_suburb VARCHAR(100),
	address_city VARCHAR(100),
	address_postal_code VARCHAR(100)
);

-- building units
CREATE TABLE rem.units(
	unit_id VARCHAR(10) PRIMARY KEY NOT NULL,
	gender VARCHAR (6) NOT NULL,
	type VARCHAR ( 4 ) NOT NULL,
	building_id VARCHAR(10),
	CONSTRAINT fk_unit
		FOREIGN KEY(building_id) 
	  REFERENCES rem.buildings(building_id)

);

-- rooms
CREATE TABLE rem.rooms (
	room_id VARCHAR(10) PRIMARY KEY,
	occupied bool DEFAULT FALSE,
	price INT DEFAULT 5500,
	unit_id VARCHAR (10) NOT NULL,
	CONSTRAINT fk_room
      FOREIGN KEY(unit_id) 
	  REFERENCES rem.units(unit_id)
);

-- tenants
CREATE TABLE rem.tenants (
	tenant_id VARCHAR(20) PRIMARY KEY,
	name VARCHAR ( 50 ) NOT NULL,
	surname VARCHAR ( 50 ) NOT NULL,
	gender VARCHAR(6),
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	contact VARCHAR(10),
	approved bool DEFAULT FALSE,
	room_id VARCHAR(10) UNIQUE NOT NULL,
	CONSTRAINT fk_tenant
		FOREIGN KEY(room_id) 
	  REFERENCES rem.rooms(room_id)
);

-- tenant_details
CREATE TABLE rem.tenant_application_details(
	institution VARCHAR(250) NOT NULL,
	funding VARCHAR(20) NOT NULL,
	application_date DATE NOT NULL,
	approval_date DATE,
	tenant_id VARCHAR(20) UNIQUE NOT NULL,
	CONSTRAINT fk_tenant_application_details
  	FOREIGN KEY(tenant_id) 
  	REFERENCES rem.tenants(tenant_id)
);