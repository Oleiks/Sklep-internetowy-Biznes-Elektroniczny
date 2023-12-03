#!/bin/bash
chmod -R 755 .
docker-compose up -d
sleep 10
docker-compose down
sleep 10
docker-compose up -d
