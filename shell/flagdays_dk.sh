#!/bin/bash

##########          TOOLS          ##########
# I have a bunch of tools in a separate file
# Essentially you will only need this function:

# _send_data
# $1 = query
# $2 = URL
# _send_data() {
#   curl -X POST \
#   -H "Accept: application/json" \
#   -H "Authorization: Bearer $APITOKEN" \
#   -H "Content-Type: application/json" \
#   -d "$1" \
#   $2
#}

# LOAD THE TOOL-BOX
source /config/shell/tools.sh

##########          CONST          ##########
# I have stored my shell-secrets in "/config/shell_secrets.txt"
# These are the needed secrets:

# APITOKEN="YOUR TOKEN"
# API_STATES_PATH="api/states"
# BASE_URL="http://YOUR_HA_IP:8123/"

# LOAD THE SECRETS
source /config/shell_secrets.txt

# ENTITY OF THE SENSOR
ENTITY="sensor.flagdays_dk"

# SCRAPING DETAILS
URL="https://www.justitsministeriet.dk/temaer/flagning/flagdage/"
HTML_YEAR_STRING="<h2>Officielle flagdage"

# HALF MAST DAYS
GOOD_FRIDAY="Langfredag"
GERMAN_OCCUPATION_DAY="9-4"

# NORDIC NATIONALDAYS
GREENLAND="Grønland"
FAROE_ISLANDS="Færø"

# IMAGES
FLAG_IMAGE_PATH="/local/images/flags"
DENMARK_IMAGE="Denmark.png"
GREENLAND_IMAGE="Greenland.png"
FAROE_ISLANDS_IMAGE="Faroe_Islands.png"
DEFAULT_FLAG=$DENMARK_IMAGE

# SCRIPT CONST
TEMP_PATH="temp"
FLAG_TMP_FILE="flag_temp.html"
FLAG_PROCESSED_FILE="flag_processed.txt"

MONTHS="januar februar marts april maj juni juli august september oktober november december"

##########          FUNCTIONS          ##########
# RETURN THE CORRECT IMAGE OF THE FLAG WITH PATH
flag_image() {
  case $EVENT in
    *"$GREENLAND"*)       echo $FLAG_IMAGE_PATH/$GREENLAND_IMAGE;;
    *"$FAROE_ISLANDS"*)   echo $FLAG_IMAGE_PATH/$FAROE_ISLANDS_IMAGE;;
    *)                    echo $FLAG_IMAGE_PATH/$DENMARK_IMAGE;;
  esac
}

# IF THE EVENT IS "GOOD FRIDAY" RETURN TRUE ELSE FALSE
good_friday() {
  case $EVENT in
    *"$GOOD_FRIDAY"*)     echo "true";;
    *)                    echo "false";;
  esac
}

# IF THE EVENT IS THE DAY OF THE GERMAN OCCUPATION
# RETURN "12:00:00" WHICH IS THE TIME OF DAY TO HOIST THE FALG TO THE TOP
# ELSE RETURN FALSE
german_occupation_day() {
  case $GERMAN_OCCUPATION_DAY in
    "$DAY-$MONTH")        echo "\"12:00:00\"";;
    *)                    echo "false";;
  esac
}
##########          FUNCTIONS END         ##########

##########          MAIN          ##########
# INITIAL CLEANUP
rm -f $TEMP_PATH/$FLAG_TMP_FILE $TEMP_PATH/$FLAG_PROCESSED_FILE

# FETCH THE HTML PAGE FROM THE DANISH JUSTICE DEPARTMENT
# AND SAVE IT IN A TEMP FILE
curl $URL -o $TEMP_PATH/$FLAG_TMP_FILE

# EXTRACT THE YEAR
YEAR=$(grep $HTML_YEAR_STRING $TEMP_PATH/$FLAG_TMP_FILE | cut -d' ' -f3 | cut -d'<' -f1)

# EXTRACT THE DATA AND STORE IT IN A NEW TEMP FILE
grep -o '<figure class="wp-block-table is-style-stripes"><table><tbody><tr>.*</figure>' $TEMP_PATH/$FLAG_TMP_FILE | sed 's/.*<tbody>//g' | sed 's/<\/tbody>.*//g' | sed 's/<\/tr>/\n/g' | sed 's/<\/td><td>/|/g' | awk 'NF' | sed 's/<tr><td>//g' | sed 's/<\/td>//g' > $TEMP_PATH/$FLAG_PROCESSED_FILE

# PREPARE SOME PLACEHOLDERS
# STATE IS USED TO TEST WHETHER A EVENT IS IN THE FUTURE/TODAY > 0
STATE=-1
# MAIN QUERY STRING IS RESET
QUERY=""
# ATTRIBUTES STRING IS DEFINED WITH THE NAME OF THE LIST OF EVENTS
ATTR="\"events\": [ "
# CALCULATE DAYS (NOW) FROM THE EPOCH
NOW_DAYS_FROM_EPOCH=$(( ($(date +"%s") / 86400) - 1 ))

echo "START:" > $TEMP_PATH/Debug.txt

# READ LINES FROM THE 2ND TEMP FILE
while read line; do

  # EXTRACT THE DAY OF THE EVENT
  DAY=$(echo "$line" | cut -d'.' -f1)

  # EXTRACT THE MONTH OF THE EVENT AND FIND IT IN THE LIST OF MONTHS
  MONTH=$(echo "$line" | cut -d' ' -f2 | cut -d'|' -f1)
  i=1
  for A_MONTH in $MONTHS; do
    if [[ $A_MONTH == $MONTH ]]; then
      MONTH=$i
      break
    fi
    i=$((i+1))
  done

  # CALCULATE TIMESTAMP AND DAYS FROM EPOCH FOR THE EVENT
  EVENT_TIMESTAMP=$(date -d "$YEAR-$MONTH-$DAY" +"%s")
  EVENT_DAYS_FROM_EPOCH=$(( $(date -d "$YEAR-$MONTH-$DAY" +"%s") / 86400 ))

  # FORMAT THE DATE IN A PROPER WAY DD-MM-YYYY
  DATE=$(date -d "$YEAR-$MONTH-$DAY" +"%d-%m-%Y")

  # EXTRACT THE DESCRIPTION OF THE EVENT
  EVENT=$(echo "$line" | cut -d'|' -f2)

  # CHECK EVENTS UNTIL WE HAVE FOUND THE FIRST EVENT IN THE FUTURE
  # STATE < 0, WE HAVE NOR FOUND IT YET
  if [[ $STATE -lt 0 ]]; then

    # SET NEW_STATE TO THE DAYS FROM NOW TO THE EVENT
    NEW_STATE=$(( $EVENT_DAYS_FROM_EPOCH - $NOW_DAYS_FROM_EPOCH ))

    # IS THE EVENT IN THE PAST OR FUTURE
    # NEW_STATE >= 0, IS EITHER TODAY OR IN THE FUTURE
    if [[ $NEW_STATE -ge 0 ]]; then

      # SET THE STATE TO THE NEW_STATE
      # SEARCH NO FUTHER
      STATE=$NEW_STATE

      # PREPARE THE MAIN PART OF THE QUERY TO THE API
      # THE STATE OF THE ENTITY IS THE NEW_STATE
      QUERY="{ \"state\": \"$NEW_STATE\", \"attributes\": { \"date\": \"$DATE\", \"event\": \"$EVENT\", \"timestamp\": \"$EVENT_TIMESTAMP\", \"icon\": \"mdi:flag\", \"friendly_name\": \"`echo $EVENT | cut -d'.' -f1`\", \"default_flag\": \"$FLAG_IMAGE_PATH/$DEFAULT_FLAG\""

      # ADD THE IMAGE OF THE FALG
      QUERY="$QUERY, \"entity_picture\": \"$(flag_image)\""

      # GOOD FRIDAY...?
      QUERY="$QUERY, \"half_mast_all_day\": $(good_friday)"

      # GERMAN_OCCUPATION_DAY...?
      QUERY="$QUERY, \"half_mast_end_time\": $(german_occupation_day)"
    fi
  fi

  # START A NEW ATTRIBUTE WITH DATE, EVENT & TIMESTAMP
  ATTR="$ATTR{ \"date\": \"$DATE\", \"event\": \"$EVENT\", \"timestamp\": \"$EVENT_TIMESTAMP\""

  # ADD IMAGE OF THE FLAG
  ATTR="$ATTR, \"entity_picture\": \"$(flag_image)\""

  # GOOD FRIDAY...?
  ATTR="$ATTR, \"half_mast_all_day\": $(good_friday)"

  # GERMAN_OCCUPATION_DAY...?
  ATTR="$ATTR, \"half_mast_end_time\": $(german_occupation_day)"

  # END THE ATTRIBUTE STRING
  ATTR="$ATTR },"

done < $TEMP_PATH/$FLAG_PROCESSED_FILE

echo $QUERY >> $TEMP_PATH/Debug.txt
#echo ${ATTR:0:-1} >> $TEMP_PATH/Debug.txt

# FINISH THE QUERY BY APPENDING THE ATTRIBUTES, STRIPPING THE LAST CHARACTER
QUERY="$QUERY, ${ATTR:0:-1} ] } }"

# SEND THE QUERY TO HOME ASSISTANTS API
_send_data "$QUERY" "$BASE_URL$API_STATES_PATH/$ENTITY"

echo $QUERY >> $TEMP_PATH/Debug.txt

# $1 = JSON string
# $2 = Filename with path
# UPLOAD TO REST SERVICE
_curl_upload_rest "$QUERY" "$TEMP_PATH/flagdays.json"

# CLEANUP ON EXIT
rm -f $TEMP_PATH/$FLAG_TMP_FILE $TEMP_PATH/$FLAG_PROCESSED_FILE
##########          MAIN END          ##########
