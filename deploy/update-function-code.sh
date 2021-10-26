#!/bin/sh
cd ../src
if [ -f ./lambda.zip ]; then
  rm ./lambda.zip
fi

if [ -f ./core30.json ]; then
  rm ./core30.json
fi

cp ../data/core30.json ./
zip -r lambda.zip .
aws lambda update-function-code \
--zip-file fileb://./lambda.zip \
--function-name stock-core30-twitter-bot
rm lambda.zip core30.json
