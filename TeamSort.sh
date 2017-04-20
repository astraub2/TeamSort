#PART 1
#first this script needs to initialize a db server
# then create a new database
#then we will run our sql script on that db:
dropdb teamsort
createdb teamsort
cd sql
psql teamsort -f create_tables.sql
echo "Database made, tables made"
cd ../import
#now we need to run our import script
#we need the directory and name of import file
# if [ "$#" -ne 2 ]; then
# 	echo "Usage: ./import_data.sh <csv file path>"
# 	exit;
# fi
#for now, input needs to be a file called "userdata.csv"
#in the import folder
python3 import_data.py > import_data.sql
psql -d teamsort -f import_data.sql
echo "Import script done, data imported"
#magic python script to read through csv files etc
#insert that data into the database

#PART 2

#This is where the python script that sorts the 
#data in the database will go
#the python script will need the name of the database
cd ../src
python TeamSort.py

#Part 3
#This is where the python script that prints out the 
#results of the sort will go. We can combine this with the above script
#if your guys want. This is where we would implement some GUI 
#perhaps?