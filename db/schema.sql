CREATE SCHEMA IF NOT EXISTS bookings
    AUTHORIZATION postgres;
    

CREATE TABLE bookings.units (
	unit_id VARCHAR(10) PRIMARY KEY,
	gender VARCHAR (6) NOT NULL,
	type VARCHAR ( 50 ) NOT NULL,
	building VARCHAR ( 50 )  NOT NULL
);

CREATE TABLE bookings.rooms (
	room_id VARCHAR(10) PRIMARY KEY,
	unit_id VARCHAR ( 10 ) NOT NULL,
	occupied bool DEFAULT FALSE,
	price INT DEFAULT 5500,
	CONSTRAINT fk_room
      FOREIGN KEY(unit_id) 
	  REFERENCES bookings.units(unit_id)
);


CREATE TABLE bookings.tenants (
	tenant_id VARCHAR(20) PRIMARY KEY,
	name VARCHAR ( 50 ) UNIQUE NOT NULL,
	surname VARCHAR ( 50 ) NOT NULL,
	gender VARCHAR(6),
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	contact VARCHAR(10),
	room_id VARCHAR(10) UNIQUE NOT NULL,
	CONSTRAINT fk_tenant
      FOREIGN KEY(room_id) 
	  REFERENCES bookings.rooms(room_id)
);
