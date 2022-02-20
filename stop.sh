#!/bin/bash

docker-compose -f docker-compose.config-server.yaml down

sleep 2

docker-compose -f docker-compose.shard-server01.yaml down

sleep 2

docker-compose -f docker-compose.shard-server02.yaml down

sleep 2

docker-compose -f docker-compose.router-server.yaml down

sleep 2

docker-compose -f docker-compose.redis-server.yaml down

sleep 2

docker-compose -f docker-compose.api-server.yaml down