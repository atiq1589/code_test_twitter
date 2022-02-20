#!/bin/bash

mongo <<EOF
var config = {
  _id: "shard01svr",
  members: [
    { _id: 0, host: "twitter_mongodb_shard01_svr01:27017" },
    { _id: 1, host: "twitter_mongodb_shard01_svr02:27017" },
    { _id: 2, host: "twitter_mongodb_shard01_svr03:27017" }
  ]
}
rs.initiate(config, { force: true });
EOF