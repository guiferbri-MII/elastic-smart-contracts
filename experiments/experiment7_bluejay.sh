#!/bin/bash

curl -X POST "http://localhost:6100/api/v1/shutdown" -s -o /dev/null
curl -X POST "http://localhost:6100/api/v1/startup" -s -o /dev/null
sleep 30
curl "http://localhost:5400/api/v6/setUpAccountableRegistry/bluejay_ans1"
sleep 200
curl -X DELETE "http://localhost:6100/api/v1/stop/bluejay_ans1"
