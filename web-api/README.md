# Env

python -m venv venv


source venv/bin/activate

> .\venv\Scripts\activate for Windows CMD

pip install "fastapi[standard]

# Dependencies

To install required deps, run the following command.

```
pip install -r requirements.txt
```

To update requirements file, run: 

```
pip freeze > requirements.txt
```

# Standalone deployment

```
docker network create --driver bridge web-net
```

## Deploy MongoDB

```
docker run --network web-net --name mongodb -d -p 27017:27017 -e "MONGODB_REPLICA_SET_MODE=primary" -e "MONGODB_REPLICA_SET_NAME=rs0" -e "ALLOW_EMPTY_PASSWORD=yes" docker.io/bitnami/mongodb:7.0.5-debian-11-r1
```

## Deploy MongoExpress (Optionally)

```
docker run --network web-net --name mongo-express -d -p 8081:8081 -e "ME_CONFIG_MONGODB_URL=mongodb://mongodb/" -e "ME_CONFIG_MONGODB_ENABLE_ADMIN=true" mongo-express
```

Default credentials:
Username: admin
Password: pass