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
1. run `sh start.sh` to Start
1. run `sh stop.sh` to Stop
1. run `sh clean.sh` to Stop and Delete all the volumes =

## Check
1. go to http://127.0.0.1:8000/docs or
1. `curl 127.0.0.1:8000`

## Attach to API server
`docker attach --sig-proxy=false twitter_api_server`
