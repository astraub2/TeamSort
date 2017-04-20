#!/usr/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: ./import_data.sh <dbname> "
	exit;
fi

python3 import_data.py > import_data.sql
psql -d $1 -f import_data.sql