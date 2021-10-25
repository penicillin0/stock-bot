#!/bin/sh
cd ../src
if [ -f ./lambda.zip ]; then
  rm ./lambda.zip
fi
zip -r lambda.zip .
aws lambda update-function-code \
--zip-file fileb://./lambda.zip \
--function-name stock-core30-twitter-bot
rm lambda.zip
