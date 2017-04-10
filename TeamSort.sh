#PART 1
#first this script needs to initialize a db server
# then create a new database
#then we will run our sql script on that db:
createdb teamdata
cd sql
psql teamdata -f create_tables.sql
cd ..

#now we need to run our import script
#we need the directory and name of import file
if [ "$#" -ne 2 ]; then
	echo "Usage: ./import_data.sh <csv file path>"
	exit;
fi
#magic python script to read through csv files etc
#insert that data into the database


#PART 2

#This is where the python script that sorts the 
#data in the database will go
#the python script will need the name of the database
python3 TeamSort.py teamdata

#Part 3
#This is where the python script that prints out the 
#results of the sort will go. We can combine this with the above script
#if your guys want. This is where we would implement some GUI 
#perhaps?