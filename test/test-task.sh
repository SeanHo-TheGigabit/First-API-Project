#!/bin/bash

curl -X 'POST' \
  'http://localhost:5000/task/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "x": 20,
  "y": 3
}'

curl -X 'GET' \
  'http://localhost:5000/task/b57ba43d-3344-4d64-a597-ecc758eeed7b' \
  -H 'accept: application/json'