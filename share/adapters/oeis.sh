#!/usr/bin/env bash

# Written by Erez Binyamin (github.com/ErezBinyamin)

# Search for an integer sequence
oeis() {
  local URL='https://oeis.org'
  local TMP=/tmp/oeis
  local DOC=/tmp/oeis/doc.html
  mkdir -p $TMP
  # Search sequence by ID
  if [ $# -eq 1 ]
  then
    # Generate URL
    [[ ${1:0:1} == 'A' ]] && ID=${1:1} || ID=${1}
    ID=$(bc <<< "$ID")
    ID="A$(printf '%06d' ${ID})"
    URL+="/${ID}"
    curl $URL 2>/dev/null > $DOC
    # ID
    printf "ID: ${ID}\n"
    # Description
    grep -A 1 '<td valign=top align=left>' $DOC \
      | sed '/<td valign=top align=left>/d; /--/d; s/^[ \t]*//; s/<[^>]*>//g;' \
      | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g'
    printf "\n"
    # Sequence
    grep -o '<tt>.*, .*[0-9]</tt>' $DOC \
      | sed 's/<[^>]*>//g' \
      | grep -v '[a-z]' \
      | grep -v ':'
    printf "\n"
    # Code
    if grep -q 'MAPLE' $DOC
    then
        GREP_REGEX='MAPLE.*CROSSREFS'
        grep -q 'PROG' $DOC && GREP_REGEX='MAPLE.*PROG'
        grep -q 'MATHEMATICA' $DOC && GREP_REGEX='MAPLE.*MATHEMATICA'
        cat $DOC \
          | tr '\n' '`' \
          | grep -o "${GREP_REGEX}" \
          | tr '`' '\n' \
          | sed 's/^[ \t]*//; s/<[^>]*>//g; /^\s*$/d;' \
          | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g' \
          | sed 's/MAPLE/(MAPLE)/; /MATHEMATICA/d; /PROG/d; /CROSSREFS/d' \
          | pygmentize -f terminal256 -g -l python -P style=monokai
        printf "\n"
    fi
    if grep -q 'MATHEMATICA' $DOC
    then
        GREP_REGEX='MATHEMATICA.*CROSSREFS'
        grep -q 'PROG' $DOC && GREP_REGEX='MATHEMATICA.*PROG'
        cat $DOC \
          | tr '\n' '`' \
          | grep -o "${GREP_REGEX}" \
          | tr '`' '\n' \
          | sed 's/^[ \t]*//; s/<[^>]*>//g; /^\s*$/d;' \
          | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g' \
          | sed 's/MATHEMATICA/(MATHEMATICA)/; /PROG/d; /CROSSREFS/d' \
          | pygmentize -f terminal256 -g -l mathematica -P style=monokai
        printf "\n"
    fi
    # PROG section language support
    cat $DOC \
      | tr '\n' '`' \
      | grep -o "PROG.*CROSSREFS" \
      | tr '`' '\n' \
      | sed 's/^[ \t]*//; s/<[^>]*>//g; /^\s*$/d;' \
      | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g' \
      | sed '/PROG/d; /CROSSREFS/d' > ${TMP}/lang
    langs=("Axiom" "MAGMA" "PARI" "Python" "Sage" "Haskell" "Julia" "GAP" "Scala")
    for L in ${langs[@]}
    do
        echo "foo" | pygmentize -l ${L,,} &>/dev/null && PYG="${L,,}" || PYG="c"
        if grep -q "(${L})" $DOC
        then
              awk -v tgt="${L}" -F'[()]' '/^\(/{f=(tgt==$2)} f' ${TMP}/lang \
              | pygmentize -f terminal256 -g -P style=monokai -l ${PYG}
              printf "\n"
        fi
    done
  # Search unknown sequence
  else
    # Build URL
    URL+="/search?q=signed%3A$(echo $@ | tr ' ' ',')"
    curl $URL 2>/dev/null > $DOC
    # Sequence IDs
    grep -o '=id:.*&' $DOC \
      | sed 's/=id://; s/&//' > $TMP/id
    # Descriptions
    grep -A 1 '<td valign=top align=left>' $DOC \
      | sed '/<td valign=top align=left>/d; /--/d; s/^[ \t]*//; s/<[^>]*>//g' \
      | sed 's/&nbsp;/ /g; s/\&amp;/\&/g; s/&gt;/>/g; s/&lt;/</g; s/&quot;/"/g' > $TMP/nam
    # Sequences
    grep -o '<tt>.*<b.*</tt>' $DOC \
      | sed 's/<[^>]*>//g' > $TMP/seq
    # Print data for all
    readarray -t ID < $TMP/id
    readarray -t NAM < $TMP/nam
    readarray -t SEQ < $TMP/seq
    for i in ${!ID[@]}
    do
      printf "${ID[$i]}: ${NAM[$i]}\n"
      echo ${SEQ[$i]}
      printf "\n"
    done
  fi
}

oeis $@
