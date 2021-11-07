#!/bin/bash

BASE_URL="DEFAULT"

while getopts e:s:d:u:t: option; do
  echo ${OPTARG}
  case "${option}" in
    e) ENTITY=${OPTARG};;
    s) ID=${OPTARG};;
    d) DIRECTION=${OPTARG};;
    u) BASE_URL=${OPTARG};;
    t) APITOKEN=${OPTARG};;
  esac
done

echo "Entity:    $ENTITY"
echo "Stop ID:   $ID"
echo "Direction: $DIRECTION"
echo "Server:    $BASE_URL"
echo "Token:     $APITOKEN"