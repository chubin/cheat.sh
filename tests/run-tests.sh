#!/bin/bash

TMP=$(mktemp /tmp/cht.sh.tests-XXXXXXXXXXXXXX)
TMP2=$(mktemp /tmp/cht.sh.tests-XXXXXXXXXXXXXX)
trap 'rm -rf $TMP $TMP2' EXIT


i=0
failed=0
while read -r test_line; do
  test_line="${test_line// #.*//}"
  eval "$test_line" > "$TMP"
  diff results/"$i" "$TMP" > "$TMP2"
  if [ "$?" != 0 ]; then
    echo FAILED: [$i] $test_line
    ((failed++))
  fi
  ((i++))
done < tests2.txt

echo TESTS/OK/FAILED "$i/$[i-failed]/$failed"


