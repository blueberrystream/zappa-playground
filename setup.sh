#!/bin/bash

# make .env file
port=`expr $UID + 28700`
echo FLASK_RUN_PORT=$port > .env

echo
echo "Your env: http://f0.fact:$port"

# make .envrc file
cp .envrc.sample .envrc

echo
echo "We use direnv for Zappa operations."
echo "Please set up direnv. https://github.com/direnv/direnv"
echo "And append your aws-cli credential to .envrc file."
echo
