#!/bin/bash
source secrets.sh
for (( ; ; ))
do
    python sb8200-scraper.py | curl -k  "http://$SPLUNK_SERVER:8088/services/collector" -H "Authorization: Splunk $SPLUNK_TOKEN" --data "@-"
    sleep 2m
done