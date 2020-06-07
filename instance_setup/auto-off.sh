#!/bin/bash
threshold=10

count=0
while true
do

  # extract average load over the last minute
  load=$(uptime | sed -e 's/.*load average: //g' | awk '{ print $1 }')
  # multiply by 100, for ease of comparison
  load2=$(awk -v a="$load" 'BEGIN {print a*100}')
  echo "Avg load over last minute: $load2 (out of 100)"
  if [ $load2 -lt $threshold ]
  then
    echo "Load below threshold of $threshold. Idling..."
    ((count+=1))
  else
    echo "Load above threshold of $threshold. Resetting counter."
    ((count=0))
  fi
  echo "Idle minutes count = $count"

  if (( count>10 ))
  then
    echo Shutting down
    # wait a little bit more before actually pulling the plug
    sleep 60
    history -a
    sudo poweroff
  fi

  sleep 10

done