#!/bin/bash

if [ -f "./redis_bin/redis-server" ]
then
    echo "Redis bin found. Running it!"
    ./redis_bin/redis-server
else
    echo "Redis bin not found. Consider running build_redis.sh"
fi

