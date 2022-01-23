#!/bin/bash

SESSION_NAME='switch'
sudo screen -ls "$SESSION_NAME" | (
  IFS=$(printf '\t');
  sed "s/^$IFS//" |
  while read -r name stuff; do
      sudo screen -S "$name" -X quit
  done
)