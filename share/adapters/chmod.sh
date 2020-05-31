#!/usr/bin/env bash

# Contributed by Erez Binyamin (github.com/ErezBinyamin)

# Translate between chmod string and number
# Inspired by http://permissions-calculator.org/
# Contrib to chubin - cheat.sh
chmod_calc(){
  p_s=""
  p_n=""
  R=()
  W=()
  X=()
  S=()
  setuid=' '
  setgid=' '
  sticky=' '
  # If permission number is given calc string
  if [[ $1 =~ ^-?[0-9]+$ && ${#1} -ge 2 && ${#1} -le 4 ]]
  then
    p_n=$1
    for (( i=0; i<${#1}; i++ ))
    do
      num=$(echo "obase=2;${1:$i:1}" | bc | xargs printf '%03d')
      if [[ ${#1} -eq 4 && $i -eq 0 ]]
      then
        [ ${num:0:1} -eq 1 ] && setuid='X' || setuid=' '
        [ ${num:1:1} -eq 1 ] && setgid='X' || setgid=' '
        [ ${num:2:1} -eq 1 ] && sticky='X' || sticky=' '
      else
        [ ${num:0:1} -eq 1 ] && p_s+='r' || p_s+='-'
        [ ${num:1:1} -eq 1 ] && p_s+='w' || p_s+='-'
        if [[ $sticky == 'X' ]]
        then
          [ ${num:2:1} -eq 1 ] && p_s+='s' || p_s+='S'
        else
          [ ${num:2:1} -eq 1 ] && p_s+='x' || p_s+='-'
        fi
        [ ${num:0:1} -eq 1 ] && R+=('X') || R+=(' ')
        [ ${num:1:1} -eq 1 ] && W+=('X') || W+=(' ')
        [ ${num:2:1} -eq 1 ] && X+=('X') || X+=(' ')
      fi
    done
  # If permission string is given calc number
  elif [[ ${#1} -le 9 && $(( ${#1} % 3 )) -eq 0 && $1 =~ ^[r,w,x,s,S,-]+$ ]]
  then
    p_s=$1
    [[ ${p_s,,} =~ 's' ]] && p_n+="1" || p_n+="0"
    [[ ${p_s,,} =~ 's' ]] && sticky='X'
    for (( i=0; i<${#1}; i+=0 ))
    do
      num=0
      [[ ${1:$i:1} == 'r' ]] && R+=('X') || R+=(' ')
      [[ ${1:$((i++)):1} == 'r' ]] && let num++
      num=$(( num << 1 ))
      [[ ${1:$i:1} == 'w' ]] && W+=('X') || W+=(' ')
      [[ ${1:$((i++)):1} == 'w' ]] && let num++
      num=$(( num << 1 ))
      [[ 'xs' =~ ${1:$i:1} ]] && X+=('X') || X+=(' ')
      [[ 'Ss' =~ ${1:$i:1} ]] && S+=('X') || S+=(' ')
      [[ 'xs' =~ ${1:$((i++)):1} ]] && let num++
      p_n+="$num"
    done
  else
    printf "Invalid permissions string: $1"
    return 1
  fi
  # Print Final results table
  printf "
Linux Permissions String:\t${p_s}
Linux Permissions Number:\t${p_n}

Special\t\tOwner\t\tGroup\t\tPublic

Setuid     [$setuid]\tRead    [${R[0]}]\tRead    [${R[1]}]\tRead    [${R[2]}]
Setgid     [$setgid]\tWrite   [${W[0]}]\tWrite   [${W[1]}]\tWrite   [${W[2]}]
Sticky bit [$sticky]\tExecute [${X[0]}]\tExecute [${X[1]}]\tExecute [${X[2]}]

"
}

chmod_calc $@
