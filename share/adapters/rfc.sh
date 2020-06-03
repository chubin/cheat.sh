#!/usr/bin/env bash

# Contributed by Erez Binyamin (github.com/ErezBinyamin)

# Search for an RFC
# Contrib to chubin - cheat.sh
RFC_get()
(
  rfc_describe() {
    sed -ne '/0001/,$p' ${RFC_INDEX} \
      | tr '\n' '#' \
      | sed 's/##/\n/g' \
      | sed 's/#    //g' \
      | grep -o '.*\. ' \
      | sed -r 's/^(.*)(January|February|March|April|May|June|July|August|September|October|November|December) [[:digit:]]{4}(.*)$/\1/'
  }

  mkdir -p /tmp/RFC_get
  local WEB_RESP="/tmp/RFC_get/rfc_get_web_resp_${RANDOM}.html"
  local RFC_INDEX="/tmp/RFC_get/rfc_index.html"
  local isNum='^[0-9]+$'
  # Update RFC_INDEX if file does not exist
  [ -f ${RFC_INDEX} ] || curl 'https://www.ietf.org/download/rfc-index.txt' 2>/dev/null > ${RFC_INDEX}
  local MIN_RFC=1
  local MAX_RFC=$(sed '/^ / d' ${RFC_INDEX} | tail -n 1 | sed 's/ .*//')

  # Syntax check Usage statement
  if [ $# -lt 1 ] || [[ ${1,,} == "-h" ]] || [[ ${1,,} == "--help" ]] || [[ ${1,,} == ":help" ]] || [[ ${1,,} == ":usage" ]]
  then
    printf "
    USAGE:
      rfc <RFC_number>		Search RFC by number
      rfc <Topic_string>	Search RFC by topic
      rfc :list			List available RFC's
      rfc :usage		Show this help message
    \n"
    return 0
  fi
  # Get corresponding RFC by number
  if [[ ${1} =~ $isNum ]]
  then
    # Validate RFC range
    if [ "$1" -gt $MAX_RFC ] || [ "$1" -lt $MIN_RFC ]
    then
      echo "Valid RFC numbers: [ ${MIN_RFC} - ${MAX_RFC} ]"
      return 1
    fi
    # If valid N: Retrieve RFC <N>
    curl "https://www.ietf.org/rfc/rfc${1}.txt" --write-out %{http_code} --silent --output ${WEB_RESP} 2>/dev/null | grep -q '200'
    if [ $? -ne 0 ]
    then
      # Attempt to retrieve PDF link to RFC <N>
      curl "https://www.rfc-editor.org/info/rfc${1}" --write-out %{http_code} --silent --output ${WEB_RESP} 2>/dev/null | grep -q '200'
      # Webpage error code (Not 200 OK)
      if [ $? -ne 0 ]
      then
        echo "Error retrieving https://www.rfc-editor.org/info/rfc${1}"
        echo "Please create github issue at https://github.com/chubin/cheat.sh/issues"
        return 2
      # RFC never issued
      elif grep -q '<h2>Not Issued</h2>' ${WEB_RESP}
      then
        echo "RFC ${1} was never issued"
        return 0
      # RFC does not exist
      elif grep -q 'does not exist</h3>' ${WEB_RESP}
      then
        echo "RFC ${1} does not exist"
        return 0
      # RFC exists only as PDF
      elif grep -q 'https.*\.pdf' $WEB_RESP
      then
        grep -o 'https.*\.pdf' $WEB_RESP
        return 0
      # Unknown error
      else
        echo "Error retrieving RFC $1"
        echo "Please create github issue at https://github.com/chubin/cheat.sh/issues"
        return 2
      fi
    fi
  # Print list of available RFCs
  elif [[ "${1,,}" == ":list" ]]
  then
    # Format RFC_INDEX to show short description of each RFC
    rfc_describe \
      | grep -v 'Not Issued' \
      | sed 's/ .*//; s/^0*//'
    return 0
  # Print list of available RFCs
  elif [[ "${1,,}" == ":describe" ]]
  then
    # Format RFC_INDEX to show short description of each RFC
    rfc_describe
    return 0
  # Format list of RFCs related to keyword:   RFC_N  RFC_Title
  else
    ARG="$*"
    rfc_describe \
      | grep -i "$ARG" \
      > $WEB_RESP
  fi
  # Format nicely and print
  sed -i '/Page [0-9]/,+2d; /page [0-9]/,+2d' ${WEB_RESP}
  if grep -q '<!DOCTYPE html>' ${WEB_RESP}
  then
    echo "Error retrieving RFC $1"
    echo "Please create github issue at https://github.com/chubin/cheat.sh/issues"
    return 2
  else
    cat -s ${WEB_RESP}
    return 0
  fi
)

RFC_get "$1"
