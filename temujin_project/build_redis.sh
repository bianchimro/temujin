#!/bin/bash

#rebuild redis
rm -rf redis_build
rm -rf redis_bin

mkdir redis_build
wget http://download.redis.io/releases/redis-2.8.4.tar.gz -O redis_build/redis.tar.gz
cd redis_build
tar -xzvf redis.tar.gz 
rm -rf redis.tar.gz 
cd redis-2.8.4
make
cd ..
mv redis-2.8.4/src ../redis_bin
cd ..
rm -rf redis_build

