#!/bin/bash

################################################################
#                                                              #
#       This script allows you to run a query/several queries  #
#       against a list of postgres instances                   #
#       Usage : ./launch_sql sql_file                          #
#       (You should put your credentials in .pgpass file       #
#        to avoid typing your password each time)              #
#                                                              #
################################################################

PORT=5432
USER="foo"
DB="foo_db"
SQL_FILE=$1

servers=(
127.0.0.1
192.168.0.2
192.168.0.3
192.168.0.4
)

if [ -z $1 ]; then
    echo "Usage : ./launch_sql sql_file"
    exit 1
fi;

do_launch()
{
    psql -p $PORT -h $1 -U $USER $DB -f $SQL_FILE
    if [ $? = 0 ]; then
        echo "Conn : OK";
    else
        echo "Conn : Not OK";
    fi;
}

for s in "${servers[@]}"
do
    do_launch $s
done
