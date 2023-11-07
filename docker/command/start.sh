#!/bin/bash

# service nginx start

cd /code/

# pip3 install -U urllib3
# pip3 install -r requirements.txt

# sleep 23s

python3 manage.py makemigrations
python3 manage.py migrate auth
python3 manage.py migrate authtoken
python3 manage.py migrate


python3 manage.py loaddata fixtures/users.json
python3 manage.py loaddata fixtures/type_transfer.json

# python3 manage.py collectstatic

# python3 manage.py dumpdata settings.TypeTransfer > fixtures/type_transfer.json

python3 manage.py runserver 0.0.0.0:9001 --insecure

