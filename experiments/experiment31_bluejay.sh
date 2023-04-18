#!/bin/bash

curl -X POST "http://localhost:6100/api/v1/shutdown" -s -o /dev/null
curl -X POST "http://localhost:6100/api/v1/startup" -s -o /dev/null
sleep 30
curl "http://localhost:5400/api/v6/setUpAccountableRegistry/bluejay_ans1?from=2023-04-13T22:00:00.000Z&to=2023-04-17T21:59:59.999Z"
sleep 200
curl "http://localhost:5400/api/v6/setUpAccountableRegistry/bluejay_ans2?from=2023-04-13T22:00:00.000Z&to=2023-04-17T21:59:59.999Z"
sleep 200
curl "http://localhost:5400/api/v6/setUpAccountableRegistry/bluejay_ans3?from=2023-04-13T22:00:00.000Z&to=2023-04-17T21:59:59.999Z"
sleep 200
curl -X DELETE "http://localhost:6100/api/v1/stop/bluejay_ans3"
sleep 100
curl -X DELETE "http://localhost:6100/api/v1/stop/bluejay_ans2"
sleep 100
curl -X DELETE "http://localhost:6100/api/v1/stop/bluejay_ans1"
