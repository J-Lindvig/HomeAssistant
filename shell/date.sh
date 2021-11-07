#!/bin/bash

startDate="2021-09-23 09:00:00";
startTS=$(date -d "$startDate" +%s)
finalDate=$(date "+%Y-%m-%d %H:%M:00")
finalTS=$(date -d "$finalDate" +%s)

clear
echo "START DATO OG TID:"
echo "------------------"
echo "$startDate ($startTS)"
echo
echo "SLUT DATO OG TID:"
echo "-----------------"
echo "$finalDate ($finalTS)"
echo
echo "DELTA:"
echo "------"
echo "$(( $finalTS - $startTS)) sekunder"
echo "$(( ($finalTS - $startTS) / 60 )) minutter"