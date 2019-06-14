#!/bin/sh
apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev libressl-dev
export FLASK_APP=olirowanxyz.py
python -m venv venv
venv/bin/pip install -r /app/olirowanxyz/requirements.txt
source venv/bin/activate
mkdir /tmp/olirowanxyz
cd /app/olirowanxyz
flask db init --directory /tmp/olirowanxyz/migrations
flask db migrate -m "Initial Database State" --directory /tmp/olirowanxyz/migrations
flask db upgrade --directory /tmp/olirowanxyz/migrations
exec gunicorn -b :8000 --access-logfile - --error-logfile - olirowanxyz:app