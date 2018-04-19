#!/bin/bash

echo "Starting uwsgi"
cd /app
su www-data -c " \
    cd /app
    . /etc/profile; \
    /usr/local/bin/uwsgi --enable-threads --lazy --ini /app/cfn_nag_app.ini" \
    2>&1 | tee -a /var/log/nginx/uwsgi.log &

echo "Starting nginx"
/usr/sbin/nginx

while [ ! -f /semaphore/done ]; do
    sleep 1
done
