#!/usr/bin/env bash

# check if database exists, if yes then delete the database

if [ -e database.db ];
then
	rm database.db
fi

# create database and update 2 database tables from the text files
sqlite3 database.db < ./src/CreateDb.txt

# Execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt
