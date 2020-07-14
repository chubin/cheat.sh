#!/usr/bin/env bash

# Written by Erez Binyamin (github.com/ErezBinyamin)

# Search for an integer sequence
# USAGE:
#	oeis <language> <sequence ID>
#	oeis <sequence ID> <language>
#	oeis <val_a, val_b, val_c, ...>
oeis() (
  local URL='https://oeis.org/search?q='
  local TMP=$(mktemp -d oeis.XXXXXXX)
  local DOC=${TMP}/doc.html
  local MAX_TERMS_LONG=30
  local MAX_TERMS_SHORT=10
  mkdir -p $TMP
  rm -f ${TMP}/authors ${TMP}/bibliograpy ${TMP}/section $TMP/code_snippet
  # -- MAIN --
  # Search sequence by ID (optional language arg)
  # 	. oeis <SEQ_ID>
  # 	. oeis <SEQ_ID> <SECTION>
  # 	. oeis <SECTION> <SEQ_ID>
  isNum='^[0-9]+$'
  # Search for specific sequence (and potentially language or :SECTION (list)
  if [ $# -ge 1 ] \
     && [[ $(echo $1 | tr -d 'aA') =~ $isNum || $(echo $2 | tr -d 'aA') =~ $isNum ]] \
     && [[ ! $(echo $1 | tr -d 'aA') =~ $isNum || ! $(echo $2 | tr -d 'aA') =~ $isNum ]]
  then
    # Arg-Parse ID, Generate URL
    if [[ $(echo $1 | tr -d 'aA') =~ $isNum ]]
    then
      ID=${1^^}
      SECTION=$2
    else
      ID=${2^^}
      SECTION=$1
    fi
    [[ ${ID:0:1} == 'A' ]] && ID=${ID:1}
    ID=$(bc <<< "$ID")
    ID="A$(printf '%06d' ${ID})"
    URL+="id:${ID}&fmt=text"
    curl $URL 2>/dev/null > $DOC
    # :list available language code_snippets
    if [[ ${SECTION^^} == ':LIST' || ${SECTION^^} == ':PROG' ]]
    then
      grep -q '%p' $DOC && echo 'maple' >> $TMP/section
      grep -q '%t' $DOC && echo 'mathematica' >> $TMP/section
      grep '%o' $DOC \
        | grep "${ID} (" \
        | sed "s/^.*${ID} (//; s/).*//" \
        | awk 'NF == 1' \
        >> $TMP/section
      [[ -f $TMP/section && $(wc -c < $TMP/section) -ne 0 ]] \
        && cat ${TMP}/section | sort -u \
        || printf 'No code snippets available.\n'
      rm -rf $TMP
      return 0
    fi
    # Print ID
    printf "ID: ${ID}\n"
    # Print Description (%N)
    grep '%N' $DOC | sed "s/^.*${ID} //"
    printf '\n'
    # Print Sequence (Three sections %S %T nd %U)
    grep '%S' $DOC | sed "s/^.*${ID} //" | tr -d '\n' > $TMP/seq
    grep '%T' $DOC | sed "s/^.*${ID} //" | tr -d '\n' >> $TMP/seq
    grep '%U' $DOC | sed "s/^.*${ID} //" | tr -d '\n' >> $TMP/seq
    cat $TMP/seq \
      | cut -d ',' -f 1-${MAX_TERMS_LONG} \
      | sed 's/,/, /g; s/$/ .../'
    # Generate code snippet (%p, %t, %o) (maple, mathematica, prog sections)
    if [ $# -gt 1 ]
    then
      printf "\n\n"
      # MAPLE section (%p)
      if [[ ${SECTION^^} == 'MAPLE' ]] && grep -q '%p' $DOC
      then
        grep '%p' $DOC | sed "s/^.*${ID} //" > $TMP/code_snippet
      # MATHEMATICA section (%t)
      elif [[ ${SECTION^^} == 'MATHEMATICA' ]] && grep -q '%t' $DOC
      then
        grep '%t' $DOC | sed "s/^.*${ID} //" > $TMP/code_snippet
      # PROG section (%o)
      elif grep -qi '%o' $DOC && grep -qi $SECTION $DOC
      then
        # Print out code sample for specified language
        grep '%o' $DOC \
          | sed "s/%o ${ID} //" \
          | awk -v tgt="${SECTION^^}" -F'[()]' '{act=$2} sub(/^\([^()]+\) */,""){f=(tgt==toupper(act))} f' \
          > ${TMP}/code_snippet
      fi
      # Print code snippet with 4-space indent to enable colorization
      if [[ -f $TMP/code_snippet && $(wc -c < $TMP/code_snippet) -ne 0 ]]
      then
        # Get authors
        grep -o ' _[A-Z].* [A-Z].*_, [A-Z].*[0-9]' ${TMP}/code_snippet \
          | sed 's/,.*//' \
          | sort -u \
          > ${TMP}/authors
        i=1
        # Replace authors with numbers
        while read author
        do
          author=$(<<<"$author" sed 's/[]\\\*\(\.[]/\\&/g')
          sed -i "s|${author}.*[0-9]|[${i}]|" ${TMP}/code_snippet
          author=$(echo $author | tr -d '_\\')
          author_url='https://oeis.org/wiki/User:'"$(echo ${author} | tr ' ' '_')"
          echo "[${i}] [${author}] [${author_url}]" \
           >> ${TMP}/bibliograpy
          let i++
        done <${TMP}/authors
        # Print snippet
        sed 's/^/   /' ${TMP}/code_snippet
      else
        printf "${SECTION^^} unavailable. Use :list to view available languages.\n"
      fi
    fi
  # Search unknown sequence
  elif [ $# -gt 1 ] && ! echo $@ | grep -q -e [a-z] -e [A-Z]
  then
    # Build URL
    URL+="signed:$(echo $@ | tr -sc '[:digit:]-' ',')&fmt=short"
    curl $URL 2>/dev/null > $DOC
    # Sequence IDs
    grep -o '"/A[0-9][0-9][0-9][0-9][0-9][0-9]">A[0-9][0-9][0-9][0-9][0-9][0-9]' $DOC \
      | sed 's/.*>//' \
      > $TMP/id
    readarray -t ID < $TMP/id
    # Descriptions
    grep -A 1 '<td valign=top align=left>' $DOC \
      | sed '/--/d; s/<[^>]*>//g; /^\s*$/d; s/^[ \t]*//' \
      | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g' \
      > $TMP/desc
    readarray -t DESC < $TMP/desc
    # Sequences
    grep 'style="color:black;font-size:120%' $DOC \
      | sed 's/<[^>]*>//g; s/^[ \t]*//' \
      | cut -d ',' -f 1-${MAX_TERMS_SHORT} \
      | sed 's/,/, /g; s/$/ .../' \
      > $TMP/seq
    readarray -t SEQ < $TMP/seq
    # Print all ID, DESC, SEQ
    for i in ${!ID[@]}
    do
      printf "${ID[$i]}: ${DESC[$i]}\n"
      printf "${SEQ[$i]}\n\n"
    done
  else
    printf "
# oeis
#
# The On-Line Encyclopedia of Integer Sequences (OEIS),
# also cited simply as Sloane's, is an online database of integer sequences.

# Find all possible OEIS sequences for some sequence (1,1,1,1...)
curl cheat.sh/oeis/1+1+1+1

# Describe an OEIS sequence (A2)
curl cheat.sh/oeis/A2

# Implementation of the A2 OEIS sequence in Python
curl cheat.sh/oeis/A2/python

# List all available implementations of the A2 OEIS sequence
curl cheat.sh/oeis/A2/:list
"
    rm -rf $TMP
    return 1
  fi
  # Error statements
  grep 'results, too many to show. Please refine your search.' $DOC | sed -e 's/<[^>]*>//g; s/^[ \t]*//'
  grep -o 'Sorry, but the terms do not match anything in the table.' $DOC
  # print bibliography
  printf "\n\n"
  [ -f ${TMP}/bibliograpy ] && cat ${TMP}/bibliograpy
  # Print URL for user
  printf "[${URL}]\n" \
    | rev \
    | sed 's/,//' \
    | rev \
    | sed 's/&.*/]/'
  rm -rf $TMP
  return 0
)

oeis $@
