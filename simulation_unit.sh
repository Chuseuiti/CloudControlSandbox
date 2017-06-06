#!/bin/bash
# Script executing httpmon and sending the corresponding workload every 8 seconds, 8 seconds is the granularity defined in the output workload csv file

#./httpmon-master/httpmon --url http://localhost/PHP/index.html --concurrency 100

python cloud_controller.py &

sleep 2m

url="http://localhost/PHP/index.html"

function setStart {
	echo [`date +%s`] start
}
function setCount {
	echo [`date +%s`] count=$1
	echo "count=$1" >&9
}
function setOpen {
	echo [`date +%s`] open=$1
	echo "open=$1" >&9
}
function setThinkTime {
	echo [`date +%s`] thinktime=$1
	echo "thinktime=$1" >&9
}
function setConcurrency {
	echo [`date +%s`] concurrency=$1
	echo "concurrency=$1" >&9
	
}
function setTimeout {
	echo [`date +%s`] timeout=$1
	echo "timeout=$1" >&9
}

#
# Initialization
#

# Create FIFO to communicate with httpmon and start httpmon
rm -f httpmon.fifo
mkfifo httpmon.fifo
../httpmon-master/httpmon --dump --url $url --concurrency 0 --timeout 30 --deterministic < httpmon.fifo &> httpmon.log &
exec 9<> httpmon.fifo

#
# Setting parameters
#
#setOpen 1
#setThinkTime 1
#setTimeout 4
#setCount 120900
setStart

#
# Reading file and setting concurrency
#
while read -r time hour concurrency;
do

echo "Concurrency:" $concurrency
setConcurrency $concurrency


sleep 8

done < "workload/de_wikipedia-de-1000s-sorted.csv"

sleep 50m

pkill -9 httpmon

sleep 30m

pkill -9 python 

