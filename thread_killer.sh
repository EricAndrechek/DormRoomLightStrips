#!/bin/bash



sudo pgrep -fl python3 | awk '!/ARGV[1]/{print $1}' | awk '!/ARGV[2]/{print $1}' | sudo xargs kill -9

SESSION_NAME='switch'
sudo screen -ls "$SESSION_NAME" | (
  IFS=$(printf '\t');
  sed "s/^$IFS//" |
  while read -r name stuff; do
      sudo screen -S "$name" -X quit
  done
)