#!/usr/bin/env bash

remove_by_name()
{
  local query; query="$1"
  local q

  redis-cli KEYS "$query" | while read -r q; do
    redis-cli DEL "$q"
  done
}

if [ -z "$1" ]; then
  echo Usage:
  echo
  echo "    $0 QUERY"
  exit 1
fi

remove_by_name "$1"
