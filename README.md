# Accomodation-Booking

This is an online student residence booking application, in which students will be able reserve rooms for accomodation during an academic year. Students will be able to book room (make a reservation) and keep track of whether their reservation has been approved and finalized.

### Features implemented
- Booking a room (with email confirmation)


## Prerequisites
- python 3.5
- pipenv
- postgresql

Note having anaconda installed makes things easier as you would not to change your python version (just create a conda env with specified version and develop in it).
pgadmin is also useful for managing db.

## Installing
After installing all the above you will have to place 2 config files in the config folder (db_config.json and mail_config.json) . Once these are placed you then have
to instantiated the database and install python packages by running the following froom the root of the repo

 - bash db/install.bash localhost 5432 postgres

## Running
Assuminig everything went well (Otherwise you will figure it out) to run the flask server using the following
 - pipenv run python api/application.py 
Then serve the index.html file using live serve in the IDE of your choice (Just use VSCODE)
