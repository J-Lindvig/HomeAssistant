#!/bin/bash

# DO NOT ALTER BELOW THIS LINE
ICON="mdi:train"
API_PATH="api/services/"
API_STATES_PATH="api/states"
URL="http://xmlopen.rejseplanen.dk/bin/rest.exe/departureBoard"
TEMP_FILE=$(mktemp rejseplan_xml.XXXXXX -u)
QUERY=""
NEXT_DEPARTURES="\"next_departures\": [ "

### FUNCTIONS
# SEND DATA TO HOME ASSISTANT
# $1 = QUERY (THE DATA AS JSON)
# $2 = URL
_send_data() {
  curl -X POST \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $APITOKEN" \
  -H "Content-Type: application/json" \
  -d "$1" \
  $2
}

# CALCULATE AND SET THE GLOBAL ATTRIBUTES
_set_attributes() {
  local dateString=$(echo "$1" | cut -d'=' -f6 | cut -d'"' -f2)
  local TTHH=$(echo "$1" | cut -d'=' -f5 | cut -d'"' -f2 )
  local DD=$(echo "$dateString" | cut -d'.' -f1)
  local MM=$(echo "$dateString" | cut -d'.' -f2)
  local YY=$(echo "$dateString" | cut -d'.' -f3)
  DUE_AT_TS=$(date -d "20$YY-$MM-$DD $TTHH:00" +%s)
  DIRECTION=$(echo $1 | cut -d'=' -f12 | cut -d'"' -f2)
  DUE_IN="$(( ( $DUE_AT_TS - $(date -d "$(date "+%Y-%m-%d %H:%M:00")" +%s) ) / 60 ))"
  DUE_AT="$DD.$MM.$YY $TTHH"
  FINAL_STOP=$(echo $1 | cut -d'=' -f11 | cut -d'"' -f2)
  ROUTE=$(echo $1 | cut -d'=' -f2 | cut -d'"' -f2)
  SCHEDULED_AT=$DUE_AT
  STOP=$(echo $1 | cut -d'=' -f4 | cut -d'"' -f2)
  TYPE=$(echo $1 | cut -d'=' -f3 | cut -d'"' -f2)
  TRACK=$(echo $1 | cut -d'=' -f9 | cut -d'"' -f2)
}

# LOAD PARAMETERS FROM COMMAND LINE
while getopts e:n:i:s:d:u:t: option; do
  case "${option}" in
    e) ENTITY=${OPTARG};;
    n) NAME=${OPTARG};;
    i) ICON=${OPTARG};;
    s) ID=${OPTARG};;
    d) DIRECTION=${OPTARG};;
    u) BASE_URL=${OPTARG};;
    t) APITOKEN=${OPTARG};;
  esac
done

# INITIAL CLEANUP
rm -f $TEMP_FILE

# FETCH THE DATA, GREP THE DEPARTURE TAGS AND SAVE IT AS A FILE
curl "$URL?id=$ID&direction=$DIRECTION" | grep '<Departure ' > $TEMP_FILE

# EXTRACT THE FIRST LINE
line=$(head -n 1 $TEMP_FILE)

# SET THE ATTRIBUTES
_set_attributes "$line"

# IS THE FRIENDLY NAME OF THE SENSOR SET, IF NOT GENERATE IT FROM ROUTE AND FINAL_STOP
if [[ ! $NAME ]]; then
  NAME="$ROUTE $FINAL_STOP"
fi

# START THE STATE JSON
QUERY="{\"state\": $DUE_IN, \"attributes\": { \"attribution\": \"Data provided by rejseplanen.dk\", \"stop_id\": $ID, \"direction\": \"$DIRECTION\", \"due_in\": $DUE_IN, \"due_at\": \"$DUE_AT\", \"due_at_ts\": \"$DUE_AT_TS\", \"final_stop\": \"$FINAL_STOP\", \"route\": \"$ROUTE\", \"scheduled_at\": \"$SCHEDULED_AT\", \"stop\": \"$STOP\", \"type\": \"$TYPE\", \"track\": \"$TRACK\", \"unit_of_measurement\": \"min\", \"friendly_name\": \"$NAME\", \"icon\": \"$ICON\""

# FIND THE NEXT DEPARTURES
{
read; # SKIP THE FIRST LINE

# READ THE REST OF THE FILE
while read line; do

  # SET THE ATTRIBUTES
  _set_attributes "$line"

  NEXT_DEPARTURES="$NEXT_DEPARTURES{\"direction\": \"$DIRECTION\", \"due_in\": $DUE_IN, \"due_at\": \"$DUE_AT\", \"due_at_ts\": \"$DUE_AT_TS\", \"final_stop\": \"$FINAL_STOP\", \"route\": \"$ROUTE\", \"scheduled_at\": \"$SCHEDULED_AT\", \"stop\": \"$STOP\", \"type\": \"$TYPE\", \"track\": \"$TRACK\""
  NEXT_DEPARTURES="$NEXT_DEPARTURES}, "
done
} < $TEMP_FILE

# STRIP THE LAST 2 CHARACTERS FROM THE NEXT DEPARTURES
QUERY="$QUERY, ${NEXT_DEPARTURES:0:-2} ] } }"

# SEND THE DATA TO HOME ASSISTANT
_send_data "$QUERY" "$BASE_URL$API_STATES_PATH/$ENTITY"

# CLEANUP
rm -f $TEMP_FILE