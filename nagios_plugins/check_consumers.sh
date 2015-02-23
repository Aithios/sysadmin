#!/bin/bash
CONSUMER_DIR=/var/www/consumers
consumers=(
    "test_consumer7.php"
    "test_consumer2.php"
    "test_consumer5.php"
)

CRIT=false

cd $CONSUMER_DIR
for c in "${consumers[@]}"
do
    ret=$(php $c status | grep pid | cut -d' ' -f 7)
    if [[ $ret = '' ]];
    then
        echo WARNING : $c not running !
        exit 1
    fi
done

echo "OK : Consumers : ALL OK"
exit 0
