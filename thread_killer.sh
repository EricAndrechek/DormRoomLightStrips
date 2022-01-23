#!/bin/bash



pids = $(sudo pgrep -fl python3)

for pid in pids; do
    if [[ $1 !=~ pid ]] || [[ $2 !=~ pid ]]; then
        sudo kill -9 $pid
    fi
done

SESSION_NAME='switch'
sudo screen -ls "$SESSION_NAME" | (
  IFS=$(printf '\t');
  sed "s/^$IFS//" |
  while read -r name stuff; do
      sudo screen -S "$name" -X quit
  done
)