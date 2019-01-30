#!/bin/bash

docker build -t niklas/conflict_monitoring .
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v /data:/data -p 8080:8080 niklas/conflict_monitoring