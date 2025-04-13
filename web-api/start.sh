#!/bin/bash

export PYTHONPATH=/web-api

python3 /app/scripts/seed_database.py \
./app/scripts/sample_facilities.json \
./app/scripts/raw_data.json \
"$GOOGLE_API_TOKEN"

exec fastapi run app/main.py --host 0.0.0.0 --port 8000 --reload --proxy-headers
