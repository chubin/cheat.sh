#!/usr/bin/env bash

# Contributed by Erez Binyamin (github.com/ErezBinyamin)

# Translate between chmod string and number
# Contrib to chubin - cheat.sh
chmod_calc(){
  p_s=""
  p_n=""
  R=()
  W=()
  X=()
  # If permission number is given calc string
  if [[ $1 =~ ^-?[0-9]+$ ]]
  then
    p_n=$1
    for (( i=0; i<${#1}; i++ ))
    do
      num=$(echo "obase=2;${1:$i:1}" | bc | xargs printf '%03d')
      [ ${num:0:1} -eq 1 ] && p_s+='r' || p_s+='-'
      [ ${num:1:1} -eq 1 ] && p_s+='w' || p_s+='-'
      [ ${num:2:1} -eq 1 ] && p_s+='x' || p_s+='-'
      [ ${num:0:1} -eq 1 ] && R+=('X') || R+=(' ')
      [ ${num:1:1} -eq 1 ] && W+=('X') || W+=(' ')
      [ ${num:2:1} -eq 1 ] && X+=('X') || X+=(' ')
    done
  # If permission string is given calc number
  else
    p_s=$1
    for (( i=0; i<${#1}; i+=0 ))
    do
      num=0
      [[ ${1:$i:1} == 'r' ]] && R+=('X') || R+=(' ')
      [[ ${1:$((i++)):1} == 'r' ]] && let num++
      num=$(( num << 1 ))
      [[ ${1:$i:1} == 'w' ]] && W+=('X') || W+=(' ')
      [[ ${1:$((i++)):1} == 'w' ]] && let num++
      num=$(( num << 1 ))
      [[ ${1:$i:1} == 'x' ]] && X+=('X') || X+=(' ')
      [[ ${1:$((i++)):1} == 'x' ]] && let num++
      p_n+="$num"
    done
  fi
  printf "
Linux Permissions String:\t${p_s}
Linux Permissions Number:\t${p_n}

Owner\t\tGroup\t\tPublic

Read    [${R[0]}]\tRead    [${R[1]}]\tRead    [${R[2]}]
Write   [${W[0]}]\tWrite   [${W[1]}]\tWrite   [${W[2]}]
Execute [${X[0]}]\tExecute [${X[1]}]\tExecute [${X[2]}]
"
}

chmod_calc $@
