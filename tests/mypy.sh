#!/usr/bin/env bash

SKIP_FILES=(
  lib/adapter/adapter.py
  lib/adapter/cmd.py
  lib/adapter/latenz.py
  lib/adapter/learnxiny.py
  lib/adapter/question.py
  lib/adapter/internal.py
)

contains_element () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

_mypy() {
  local file
  local result=0
  
  # mypy lib/*.py lib/fmt/*.py lib/frontend/*.py

  for file in lib/*.py lib/fmt/*.py lib/frontend/*.py lib/adapter/*.py
  do
    contains_element "$file" "${SKIP_FILES[@]}" && continue
    mypy --follow-imports=skip "$file" || result=1
  done

  return "$result"    
}

_mypy
