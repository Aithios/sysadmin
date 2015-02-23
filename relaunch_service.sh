#!/bin/bash

#################################################################
#                                                               #
#       This script justs try to listen on a port / ip          #
#       every 30 seconds.                                       #
#       If it couldn't within 5 seconds it simply restarts      #
#       the service.                                            #
#                                                               #
#################################################################


SERVICE_HOST=127.0.0.1
SERVICE_PORT=7778
SERVICE=apache2

while true
do
    sleep 30
    nc -z $SERVICE_HOST $SERVICE_PORT -w 5
    echo $?
    if [[ $? -eq 0 ]];
    then
        continue
    else
        /etc/init.d/$SERVICE restart
    fi
done
