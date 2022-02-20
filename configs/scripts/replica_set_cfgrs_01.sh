#!/bin/bash

mongo <<EOF
var config = {
    "_id": "cfgrs",
    configsvr: true,
    "members": [
        { _id: 0, host: "twitter_mongodb_cfg01:27017" },
        { _id: 1, host: "twitter_mongodb_cfg02:27017" },
        { _id: 2, host: "twitter_mongodb_cfg03:27017" }
    ]
};
rs.initiate(config, { force: true });
rs.status();
EOF