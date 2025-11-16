#!/bin/sh
while :
do
    curl -s https://the-trivia-api.com/v2/questions\?limit\=1 | jq '.[0].question'
    sleep 2
done