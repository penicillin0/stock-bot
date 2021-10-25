#!/bin/sh
source ../.env

aws lambda update-function-configuration \
--function-name stock-core30-twitter-bot \
--layers $LAYER_ARN \
--environment Variables={`cat ../.env | tr -s "\n" | tr '\n' ',' | sed s/,$//`}
