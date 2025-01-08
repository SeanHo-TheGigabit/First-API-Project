#!/bin/bash

docker compose up --build celery db redis --force-recreate --no-deps
