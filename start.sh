#!/bin/bash
chmod -R 777 .
docker-compose up -d
sleep 10
docker-compose down
sleep 10
docker-compose up -d
