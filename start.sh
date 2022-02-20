#!/bin/bash

docker-compose -f docker-compose.redis-server.yaml up --scale redis-node-sentinel=3 -d

sleep 5

docker-compose -f docker-compose.config-server.yaml up -d

sleep 5

docker exec -it twitter_mongodb_cfg01 sh /etc/mongo/config/replica_set_cfgrs_01.sh

docker-compose -f docker-compose.shard-server01.yaml up -d

sleep 5

docker exec -it twitter_mongodb_shard01_svr01 sh /etc/mongo/config/replica_set_shard_01.sh

# docker-compose -f docker-compose.shard-server02.yaml up -d

# sleep 5

# docker exec -it twitter_mongodb_shard02_svr01 sh /etc/mongo/config/replica_set_shard_02.sh

docker-compose -f docker-compose.router-server.yaml up -d

sleep 5

docker exec -it twitter_mongodb_router_01 sh /etc/mongo/config/router01_shard_config.sh

docker-compose -f docker-compose.api-server.yaml up -d

