#!/bin/bash

backend_url=http://localhost:5000

# To get all stores
echo "GET /store"
curl "$backend_url"/store

# To create a new store
echo "POST /store"
curl -X POST -H "Content-Type: application/json" -d '{"name": "New Store"}' "$backend_url"/store

# To create a new item in a store
echo "POST /store/My%20Store/item"
curl -X POST -H "Content-Type: application/json" -d '{"name": "Table", "price": 25.99}' "$backend_url"/store/My%20Store/item

# To get a specific store
echo "GET /store/My%20Store"
curl "$backend_url"/store/My%20Store

# To get items in a specific store
echo "GET /store/My%20Store/item"
curl "$backend_url"/store/My%20Store/item