#!/bin/bash

# TOOLS
source /config/shell/tools.sh

# SECRETS
source /config/shell_secrets.txt

# SCRIPT CONST
TEMP_PATH="temp"

curl $PARSEHUB_GET_DMI_URL | gunzip > "$TEMP_PATH/dmi_tts.json"
_curl_upload_file "$TEMP_PATH/dmi_tts.json"
rm -f $TEMP_PATH/dmi_tts.json