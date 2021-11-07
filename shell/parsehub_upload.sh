#!/bin/bash

# SECRETS
source /config/shell_secrets.txt

# SCRIPT CONST
TEMP_PATH="temp"

curl "https://www.parsehub.com/api/v2/projects/$1/last_ready_run/data?api_key=$PARSEHUB_API_TOKEN" | gunzip > "$TEMP_PATH/$2"
curl -T "$TEMP_PATH/$2" -u $FTP_USER:$FTP_PASS ftp://$FTP_URL
rm -f $TEMP_PATH/$2