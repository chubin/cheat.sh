#!/bin/bash

# 1) start server:
#   without caching:
#       CHEATSH_CACHE_TYPE=none CHEATSH_PORT=50000 python bin/srv.py
#       (recommended)
#   with caching:
#       CHEATSH_REDIS_PREFIX=TEST1 CHEATSH_PORT=50000 python bin/srv.py
#       (for complex search queries + to test caching)
# 2) configure CHTSH_URL
# 3) run the script

CHTSH_SCRIPT=$(dirname "$(dirname "$(realpath "$(readlink -f "$0")")")")/share/cht.sh.txt

# work from script's dir
cd "$(dirname "$0")" || exit

# detect Python - if not set in env, try default virtualenv
PYTHON="${PYTHON:-../ve/bin/python}"
# if no virtalenv, try current python3 binary
if ! command -v "$PYTHON" &> /dev/null; then
  PYTHON=$(command -v python3)
fi
python_version="$($PYTHON -c 'import sys; print(sys.version_info[0])')"
echo "Using PYTHON $python_version: $PYTHON"

skip_online="${CHEATSH_TEST_SKIP_ONLINE:-NO}"
test_standalone="${CHEATSH_TEST_STANDALONE:-YES}"
show_details="${CHEATSH_TEST_SHOW_DETAILS:-YES}"
update_tests_results="${CHEATSH_UPDATE_TESTS_RESULTS:-NO}"
CHTSH_URL="${CHTSH_URL:-http://localhost:8002}"

TMP=$(mktemp /tmp/cht.sh.tests-XXXXXXXXXXXXXX)
TMP2=$(mktemp /tmp/cht.sh.tests-XXXXXXXXXXXXXX)
TMP3=$(mktemp /tmp/cht.sh.tests-XXXXXXXXXXXXXX)
trap 'rm -rf $TMP $TMP2 $TMP3' EXIT

echo "Using cht.sh client at $CHTSH_SCRIPT"

export PYTHONIOENCODING=UTF-8

i=0
failed=0
{
  if [ -z "$1" ]; then
    cat -n tests.txt
  else
    cat -n tests.txt | sed -n "$(echo "$*" | sed 's/ /p; /g;s/$/p/')"
  fi
} > "$TMP3"


while read -r number test_line; do
  echo -e "\e[34mRunning $number: \e[36m$test_line\e[0m"
  if [ "$skip_online" = YES ]; then
    if [[ $test_line = *\[online\]* ]]; then
      echo "$number is [online]; skipping"
      continue
    fi
  fi

  if [[ "$python_version" = 2 ]] && [[ $test_line = *\[python3\]* ]]; then
    echo "$number is for Python 3; skipping"
    continue
  fi

  if [[ "$python_version" = 3 ]] && [[ $test_line = *\[python2\]* ]]; then
    echo "$number is for Python 2; skipping"
    continue
  fi

  #shellcheck disable=SC2001
  test_line=$(echo "$test_line" | sed 's@ *#.*@@')

  if [ "$test_standalone" = YES ]; then
    test_line="${test_line//cht.sh /}"
    [[ $show_details == YES ]] && echo "${PYTHON} ../lib/standalone.py $test_line"
    "${PYTHON}" ../lib/standalone.py "$test_line" > "$TMP"
  elif [[ $test_line = "cht.sh "* ]]; then
    test_line="${test_line//cht.sh /}"
    [[ $show_details == YES ]] && echo "bash $CHTSH_SCRIPT $test_line"
    eval "bash $CHTSH_SCRIPT $test_line" > "$TMP"
  else
    [[ $show_details == YES ]] && echo "curl -s $CHTSH_URL/$test_line"
    eval "curl -s $CHTSH_URL/$test_line" > "$TMP"
  fi

  if ! diff -u3 results/"$number" "$TMP" > "$TMP2"; then
    if [[ $update_tests_results = NO ]]; then
      if [ "$show_details" = YES ]; then
        cat -t "$TMP2"
      fi
      echo "FAILED: [$number] $test_line"
    else
      cat "$TMP" > results/"$number"
      echo "UPDATED: [$number] $test_line"
    fi
    ((failed++))
  fi
  ((i++))
done < "$TMP3"

if [[ $update_tests_results = NO ]]; then
  echo TESTS/OK/FAILED "$i/$((i-failed))/$failed"
else
  echo TESTS/OK/UPDATED "$i/$((i-failed))/$failed"
fi

test $failed -eq 0
