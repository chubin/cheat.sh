#!/usr/bin/env bash

# Written by Erez Binyamin (github.com/ErezBinyamin)

# Search for an integer sequence
# USAGE:
#	oeis <language> <sequence ID>
#	oeis <sequence ID> <language>
#	oeis <val_a, val_b, val_c, ...>
oeis() (
  local URL='https://oeis.org/search?q='
  local TMP=/tmp/oeis
  local DOC=/tmp/oeis/doc.html
  local MAX_TERMS=10
  mkdir -p $TMP
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
    URL+="id:${ID}&fmt=text"
    curl $URL 2>/dev/null > $DOC
    # Print Code Sample
    if [[ ${LANGUAGE^^} == ':LIST' ]]
    then
      rm -f ${TMP}/list
      grep -q '%p' $DOC && echo 'maple' >> $TMP/list
      grep -q '%t' $DOC && echo 'mathematica' >> $TMP/list
      grep '%o' $DOC \
        | grep "${ID} (" \
        | sed "s/^.*${ID} (//; s/).*//" >> $TMP/list
      [[ -f $TMP/list && $(wc -c < $TMP/list) -ne 0 ]] && cat ${TMP}/list | sort -u || printf 'No code snippets available.\n'
      return 0
    fi
    # Print ID
    printf "ID: ${ID}\n"
    # Print Description (%N)
    grep '%N' $DOC | sed "s/^.*${ID} //"
    printf '\n'
    # Print Sequence (Three sections %S %T nd %U)
    grep '%S' $DOC | sed "s/^.*${ID} //"
    grep '%T' $DOC | sed "s/^.*${ID} //"
    grep '%U' $DOC | sed "s/^.*${ID} //"
    printf '\n'
    # Generate code snippet (%p, %t, %o)
    if [ $# -gt 1 ]
    then
      # MAPLE section (%p)
      if [[ ${LANGUAGE^^} == 'MAPLE' ]] && grep -q '%p' $DOC
      then
        grep '%p' $DOC | sed "s/^.*${ID} //" > $TMP/code_snippet
      # MATHEMATICA section (%t)
      elif [[ ${LANGUAGE^^} == 'MATHEMATICA' ]] && grep -q '%t' $DOC
      then
        grep '%t' $DOC | sed "s/^.*${ID} //" > $TMP/code_snippet
      # PROG section (%o)
      elif grep -qi '%o' $DOC && grep -qi $LANGUAGE $DOC
      then
        # Print out code sample for specified language
        grep '%o' $DOC \
          | sed "s/^.*${ID} //" \
          | awk -v tgt="${LANGUAGE^^}" -F'[()]' '{act=$2} sub(/^\([^()]+\) */,""){f=(tgt==toupper(act))} f' ${TMP}/prog \
          > ${TMP}/code_snippet
      fi
      # Print code snippet with 4-space indent to enable colorization
      if [[ -f $TMP/code_snippet && $(wc -c < $TMP/code_snippet) -ne 0 ]]
      then
        cat ${TMP}/code_snippet | sed 's/^/   /'
      else
        printf "${LANGUAGE^^} unavailable. Use :list to view available languages.\n"
      fi
    fi
  # Search unknown sequence
  else
    # Build URL
    URL+="signed:$(echo $@ | tr -sc '[:digit:]-' ',')&fmt=short"
    curl $URL 2>/dev/null > $DOC
    # Sequence IDs
    grep -o '"/A[0-9][0-9][0-9][0-9][0-9][0-9]">A[0-9][0-9][0-9][0-9][0-9][0-9]' $DOC \
      | sed 's/.*>//' \
      > $TMP/id
    # Descriptions
    grep -A 1 '<td valign=top align=left>' $DOC \
      | sed '/--/d; s/<[^>]*>//g; /^\s*$/d; s/^[ \t]*//' \
      | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g' \
      > $TMP/desc
    # Sequences
    grep 'style="color:black;font-size:120%' $DOC \
      | sed 's/<[^>]*>//g; s/^[ \t]*//' \
      > $TMP/seq

    readarray -t ID < $TMP/id
    readarray -t DESC < $TMP/desc
    readarray -t SEQ < $TMP/seq
    for i in ${!ID[@]}
    do
      printf "${ID[$i]}: ${DESC[$i]}\n"
      printf "${SEQ[$i]}\n\n"
    done
  fi
  grep 'results, too many to show. Please refine your search.' /tmp/oeis/doc.html | sed -e 's/<[^>]*>//g; s/^[ \t]*//'
  # Print URL for user
  printf "\n[${URL}]\n" \
    | rev \
    | sed 's/,//' \
    | rev \
    | sed 's/&.*/]/'
)

oeis $@
