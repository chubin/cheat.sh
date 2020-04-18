#!/usr/bin/env bash

# Contributed by Erez Binyamin (github.com/ErezBinyamin)

# Search for an RFC
# Contrib to chubin - cheat.sh
RFC_get()
{
  mkdir -p /tmp/RFC_get
  local WEB_RESP="/tmp/RFC_get/rfc_get_web_resp_${RANDOM}.html"
  local MIN_RFC=1
  local MAX_RFC=8650
  local isNum='^[0-9]+$'
  local NEVER_ISSUED=( "3333" "3350" "3399" "3699" "3799" "3800" "3899" "3900" "3907" "3908" "3999" "4000" "4099" "4100" "4199" "4200" "4232" "4299" "4300" "4399" "4400" "4499" "4500" "4599" "4600" "4658" "4699" "4700" "4751" "4799" "4800" "4899" "4900" "4921" "4922" "4989" "4999" "5099" "5100" "5108" "5199" "5200" "5299" "5300" "5312" "5313" "5314" "5315" "5319" "5399" "5400" "5499" "5500" "5599" "5600" "5699" "5700" "5799" "5800" "5809" "5821" "5822" "5823" "5899" "5900" "5999" "6000" "6099" "6100" "6102" "6103" "6199" "6200" "6299" "6300" "6399" "6400" "6499" "6500" "6523" "6524" "6599" "6600" "6634" "6699" "6700" "6799" "6800" "6899" "6900" "6966" "6995" "6999" "7000" "7099" "7327" "7907" "8523" "8524" "8535" "8566" "8626" "8644" "8646" "8647" "8648" )

  # Syntax check Usage statement
  if [ $# -lt 1 ] || [[ ${1,,} =~ "-h" ]] || [[ ${1,,} =~ "--help" ]]
  then
    printf "
    USAGE:
      $0 <RFC_number>
      $0 <Topic_string>
      $0 :list
      $0 <-h|--help>
    "
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
    echo "Valid RFC numbers: [ ${MIN_RFC} - ${MAX_RFC} ]"
    #for i in `seq 1 $MAX_RFC`
    #do
    #       echo "${NEVER_ISSUED[@]}" | tr ' ' '\n' | grep -qFx $i || echo $i
    #done
    return 0
  # Print list of RFCs related to keyword:   RFC_N        RFC_Title
  else
    ARG="$*"
    curl "https://www.rfc-editor.org/search/rfc_search_detail.php?title=${ARG}" 2>/dev/null \
      | sed 's/href="/\n/g; s/.html/.html\n/g' \
      | grep -A 1 --color=auto 'http.*.html' \
      | sed '/boldtext/d; s/"target/<"target/g; s/<[^>]*>//g; /HTML,/d; s/HTML//; /--/d' \
      | grep -v -B 1 html \
      | rev \
      | sed 's/lmth\.//; s/cfr.*//; /--/d' \
      | rev \
      | sed 's/[A-Z]\..*//; /mail-archive/,+1d; s/^[ \t]*//' \
      | sed  's/&nbsp.*//g; s/<a//g; N ; s/\n/:\t/' \
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
}

RFC_get "$1"
