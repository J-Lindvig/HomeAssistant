#!/bin/bash

# TOOLS
source /config/shell/tools.sh

# SECRETS
source /config/shell_secrets.txt

# SCRIPT CONST
TEMP_PATH="temp"

curl $PARSEHUB_GET_BOLD_DK_URL | gunzip > "$TEMP_PATH/soccer.json"
_curl_upload_file "$TEMP_PATH/soccer.json"
rm -f $TEMP_PATH/soccer.json