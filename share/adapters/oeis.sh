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
  # Get short description of a sequence
  get_desc() {
    grep -A 1 '<td valign=top align=left>' $DOC \
      | sed '/<td valign=top align=left>/d; /--/d; s/^[ \t]*//; s/<[^>]*>//g;' \
      | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g'
    return $?
  }
  # Print out the first MAX_TERMS terms of a sequence
  get_seq() {
    local MAX_TERMS=${1}
    grep -o '<tt>.*, .*[0-9]</tt>' $DOC \
      | sed 's/<[^>]*>//g' \
      | grep -v '[a-z]' \
      | grep -v ':' \
      | cut -d ',' -f 1-${MAX_TERMS}
    return $?
  }
  # Sample code parser INPUT arg: is grep regex <FROM*TO>
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
  # Search sequence by ID
  if [ $# -lt 3 ]
  then
    # Arg-Parse ID, Generate URL
    echo $1 | grep -q -e [a-z] -e [B-Z] && ID=$2 || ID=$1
    echo $1 | grep -q -e [a-z] -e [B-Z] && LANG=$1 || LANG=$2
    [[ ${ID:0:1} == 'A' ]] && ID=${ID:1}
    ID=$(bc <<< "$ID")
    ID="A$(printf '%06d' ${ID})"
    URL+="/${ID}"
    curl $URL 2>/dev/null > $DOC
    # Print ID
    printf "ID: ${ID}\n"
    # Print Description
    get_desc
    printf "\n"
    # Print Sequence sample limited by $MAX_TERMS
    get_seq ${MAX_TERMS}
    printf "\n"
    # Print Code Sample
    if [[ ${LANG^^} == 'MAPLE' ]] && grep -q 'MAPLE' $DOC
    then
      GREP_REGEX='MAPLE.*CROSSREFS'
      grep -q 'PROG' $DOC && GREP_REGEX='MAPLE.*PROG'
      grep -q 'MATHEMATICA' $DOC && GREP_REGEX='MAPLE.*MATHEMATICA'
      parse_code "${GREP_REGEX}" \
        | sed 's/MAPLE/(MAPLE)/; /MATHEMATICA/d; /PROG/d; /CROSSREFS/d'
    fi
    if [[ ${LANG^^} == 'MATHEMATICA' ]] && grep -q 'MATHEMATICA' $DOC
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
    awk -v tgt="${LANG^^}" -F'[()]' '/^\(/{f=(tgt==$2)} f' ${TMP}/prog > ${TMP}/code_snippet
    L="${LANG:0:1}"
    LANG="${LANG:1}"
    LANG="${L^^}${LANG,,}"
    [ $(wc -c < $TMP/code_snippet) -eq 0 ] && awk -v tgt="${LANG}" -F'[()]' '/^\(/{f=(tgt==$2)} f' ${TMP}/prog > ${TMP}/code_snippet
    cat ${TMP}/code_snippet
  # Search unknown sequence
  else
    # Build URL
    URL+="/search?q=signed%3A$(echo $@ | grep -v [a-z] | grep -v [A-Z] | tr ' ' ',')"
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
