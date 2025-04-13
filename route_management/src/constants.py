import os

GOOGLE_API_TOKEN = os.getenv("GOOGLE_API_TOKEN")
DIRECTION_GOOGLE_API_URL = "https://maps.googleapis.com/maps/api/directions"
webapi_ip = "0.0.0.0" # to be changed
webapi_port = "8000"
webapi_url = webapi_ip + ":" + webapi_port
