#!/bin/bash

export MONGODB_VERSION=6.0-ubi8
docker run --name mongodb -d -p 27017:27017 -v ~/data:/data/db mongodb/
