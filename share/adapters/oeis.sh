#!/usr/bin/env bash

# Written by Erez Binyamin (github.com/ErezBinyamin)

# Search for an integer sequence
# USAGE:
#	oeis <language> <sequence ID>
#	oeis <sequence ID> <language>
#	oeis <val_a, val_b, val_c, ...>
oeis() (
  local URL='https://oeis.org'
  local TMP=/tmp/oeis
  local DOC=/tmp/oeis/doc.html
  local MAX_TERMS=10
  mkdir -p $TMP
  # -- get_desc --
  # @return print description of OEIS sequence
  get_desc() {
    grep -A 1 '<td valign=top align=left>' $DOC \
      | sed '/<td valign=top align=left>/d; /--/d; s/^[ \t]*//; s/<[^>]*>//g;' \
      | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g'
    return $?
  }
  # -- get_seq --
  # @param  MAX_TERMS
  # @return Print the first MAX_TERMS terms of a sequence
  get_seq() {
    local MAX_TERMS=${1}
    grep -o '<tt>.*, .*[0-9]</tt>' $DOC \
      | sed 's/<[^>]*>//g' \
      | grep -v '[a-z]' \
      | grep -v ':' \
      | cut -d ',' -f 1-${MAX_TERMS}
    return $?
  }
  # -- parse_code --
  # @param  GREP_REGEX
  # @return Code snippet that corresponds to GREP_REGEX
  parse_code() {
    local GREP_REGEX="${1}"
    cat $DOC \
      | tr '\n' '`' \
      | grep -o "${GREP_REGEX}" \
      | tr '`' '\n' \
      | sed 's/^[ \t]*//; s/<[^>]*>//g; /^\s*$/d;' \
      | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g'
    return $?
  }
  # -- MAIN --
  # Search sequence by ID (optional language arg)
  # 	. oeis <SEQ_ID>
  # 	. oeis <SEQ_ID> <LANGUAGE>
  # 	. oeis <LANGUAGE> <SEQ_ID>
  isNum='^[0-9]+$'
  if [ $# -lt 3 ] && [[ ${1:1} =~ $isNum || ${2:1} =~ $isNum || ${1} =~ $isNum || ${2} =~ $isNum ]] && ! echo $1 | grep -q '[0-9]' || ! echo $2 | grep -q '[0-9]'
  then
    # Arg-Parse ID, Generate URL
    if echo ${1^^} | grep -q '[B-Z]'
    then
      ID=${2^^}
      LANGUAGE=$1
    else
      ID=${1^^}
      LANGUAGE=$2
    fi
    [[ ${ID:0:1} == 'A' ]] && ID=${ID:1}
    ID=$(bc <<< "$ID")
    ID="A$(printf '%06d' ${ID})"
    URL+="/${ID}"
    curl $URL 2>/dev/null > $DOC
    # Print ID, description, and sequence
    printf "ID: ${ID}\n"
    get_desc
    printf "\n"
    get_seq ${MAX_TERMS}
    printf "\n"
    # Print Code Sample
    if [[ ${LANGUAGE^^} == 'MAPLE' ]] && grep -q 'MAPLE' $DOC
    then
      GREP_REGEX='MAPLE.*CROSSREFS'
      grep -q 'PROG' $DOC && GREP_REGEX='MAPLE.*PROG'
      grep -q 'MATHEMATICA' $DOC && GREP_REGEX='MAPLE.*MATHEMATICA'
      parse_code "${GREP_REGEX}" \
        | sed 's/MAPLE/(MAPLE)/; /MATHEMATICA/d; /PROG/d; /CROSSREFS/d'
    fi
    if [[ ${LANGUAGE^^} == 'MATHEMATICA' ]] && grep -q 'MATHEMATICA' $DOC
    then
      GREP_REGEX='MATHEMATICA.*CROSSREFS'
      grep -q 'PROG' $DOC && GREP_REGEX='MATHEMATICA.*PROG'
      parse_code "${GREP_REGEX}" \
        | sed 's/MATHEMATICA/(MATHEMATICA)/; /PROG/d; /CROSSREFS/d'
    fi
    # PROG section contains more code samples (Non Mathematica or Maple)
    parse_code "PROG.*CROSSREFS" \
      | sed '/PROG/d; /CROSSREFS/d' > ${TMP}/prog
    # Print out code sample for specified language
    rm -f ${TMP}/code_snippet
    awk -v tgt="${LANGUAGE^^}" -F'[()]' '/^\(/{f=(tgt==$2)} f' ${TMP}/prog > ${TMP}/code_snippet
    L="${LANGUAGE:0:1}"
    LANGUAGE="${LANGUAGE:1}"
    LANGUAGE="${L^^}${LANGUAGE,,}"
    [ $(wc -c < $TMP/code_snippet) -eq 0 ] && awk -v tgt="${LANGUAGE}" -F'[()]' '/^\(/{f=(tgt==$2)} f' ${TMP}/prog > ${TMP}/code_snippet
    cat ${TMP}/code_snippet
  # Search unknown sequence
  else
    # Build URL
    URL+="/search?q=signed%3A$(echo $@ | tr -sc '[:digit:]-' ',')"
    curl $URL 2>/dev/null > $DOC
    # Sequence IDs
    grep -o '=id:.*&' $DOC \
      | sed 's/=id://; s/&//' > $TMP/id
    # Descriptions
    get_desc > $TMP/desc
    # Sequences
    get_seq ${MAX_TERMS} > $TMP/seq
    # Print data for all
    readarray -t ID < $TMP/id
    readarray -t DESC < $TMP/desc
    readarray -t SEQ < $TMP/seq
    for i in ${!ID[@]}
    do
      printf "${ID[$i]}: ${DESC[$i]}\n"
      echo ${SEQ[$i]}
      printf "\n"
    done
  fi
)

oeis $@
