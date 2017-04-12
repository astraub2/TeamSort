#!/usr/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./import_data.sh <dbname> <input dir>"
	exit;
fi

cp import_data.py $2
cd $2
python3 import_data.py > import_data.sql
psql -d $1 -f import_data.sql