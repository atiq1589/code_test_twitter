# Setup
This application depends on PIPENV. it will help if it is already installed in your system

## Install Dependencies
1. run `pipenv install`

## Run Application [Not Recommended]
1. run `pipenv shell`
1. run `uvicorn main:app --reload`

## Run Application with Docker [Recommended]
Please note at least 3 redis sentinel node required as quorum set to 2.
up to 5 redis sentinel server can be added
run `docker-compose up --scale redis-node-sentinel=3 -d`

## Check
1. go to http://127.0.0.1:8000 or
1. `curl 127.0.0.1:8000`

## Attach to API server
`docker attach --sig-proxy=false tweeter_api_server`
