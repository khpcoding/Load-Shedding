#!/bin/bash 
while true; do 
  echo "Sending 40 requests..."; 
  seq 1 40 | xargs -I {} -P 40 curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5000/; 
  echo "Waiting 5 seconds..."; 
  sleep 5; 
done
