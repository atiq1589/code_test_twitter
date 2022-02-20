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

docker volume rm code_test_twitter_twitter_mongodb_cfg01 code_test_twitter_twitter_mongodb_cfg02 code_test_twitter_twitter_mongodb_cfg03 
docker volume rm code_test_twitter_twitter_mongodb_shard01_svr01 code_test_twitter_twitter_mongodb_shard01_svr02 code_test_twitter_twitter_mongodb_shard01_svr03 
docker volume rm code_test_twitter_twitter_mongodb_shard02_svr01 code_test_twitter_twitter_mongodb_shard02_svr02 code_test_twitter_twitter_mongodb_shard02_svr03 

