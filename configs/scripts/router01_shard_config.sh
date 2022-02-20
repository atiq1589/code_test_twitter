#!/bin/bash

mongo <<EOF
sh.addShard("shard01svr/twitter_mongodb_shard01_svr01,twitter_mongodb_shard01_svr02,twitter_mongodb_shard01_svr03");
# sh.addShard("shard02svr/twitter_mongodb_shard02_svr01,twitter_mongodb_shard02_svr02,twitter_mongodb_shard02_svr03");

sh.enableSharding("twitterDb");

sh.shardCollection("twitterDb.tweets", {"user_id": "hashed"});
EOF
