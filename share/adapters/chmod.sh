#!/usr/bin/env bash

# Contributed by Erez Binyamin (github.com/ErezBinyamin)

GRC_STYLESHEET="${BASH_SOURCE[0]}"; GRC_STYLESHEET=${GRC_STYLESHEET%.sh}.grc

# Translate between chmod string and number
# Inspired by http://permissions-calculator.org/
# Contrib to chubin - cheat.sh
chmod_calc(){
  p_s=""
  p_n=""
  R=()
  W=()
  X=()
  setuid=' '
  setgid=' '
  sticky=' '
  # If permission number is given -> calc string
  if [[ $1 =~ ^-?[0-9]+$ && ${#1} -ge 1 && ${#1} -le 4 ]]
  then
    p_n=$(printf "%04s\n" "$1" | tr ' ' '0')
    echo $p_n | grep -q '[8-9]' && return 1
    for (( i=0; i<${#p_n}; i++ ))
    do
      num=$(echo "obase=2;${p_n:$i:1}" | bc | xargs printf '%03d')
      # If 4 digit input -> process specials
      if [ $i -eq 0 ]
      then
        [ ${num:0:1} -eq 1 ] && setuid='X' || setuid=' '
        [ ${num:1:1} -eq 1 ] && setgid='X' || setgid=' '
        [ ${num:2:1} -eq 1 ] && sticky='X' || sticky=' '
      else
        # Build p_s string
        [ ${num:0:1} -eq 1 ] && p_s+='r' || p_s+='-'
        [ ${num:1:1} -eq 1 ] && p_s+='w' || p_s+='-'
        # Use sS or tT instead of x- according to specials
        if [[ $i -eq 1 && $setuid == 'X' ]]
        then
          [ ${num:2:1} -eq 1 ] && p_s+='s' || p_s+='S'
        elif [[ $i -eq 2 && $setgid == 'X' ]]
        then
          [ ${num:2:1} -eq 1 ] && p_s+='s' || p_s+='S'
        elif [[ $i -eq 3 && $sticky == 'X' ]]
        then
          [ ${num:2:1} -eq 1 ] && p_s+='t' || p_s+='T'
        else
          [ ${num:2:1} -eq 1 ] && p_s+='x' || p_s+='-'
        fi
        # Populate arrays for the table
        [ ${num:0:1} -eq 1 ] && R+=('X') || R+=(' ')
        [ ${num:1:1} -eq 1 ] && W+=('X') || W+=(' ')
        [ ${num:2:1} -eq 1 ] && X+=('X') || X+=(' ')
      fi
    done
  # If permission string is given -> calc number
  elif [[ $1 =~ ^[r,s,S,t,T,w,x,-]+$ ]]
  then
    # FULL STRING
    if [[ ${#1} -eq 9 ]]
    then
      p_s=$1
      num=0
      # Process specials
      [[ 'sS' =~ ${p_s:2:1} ]] && setuid='X' && num=$((num+4))
      [[ 'sS' =~ ${p_s:5:1} ]] && setgid='X' && num=$((num+2))
      [[ 'tT' =~ ${p_s:8:1} ]] && sticky='X' && num=$((num+1))
      [ ${num} -gt 0 ] && p_n+="$num"
      # Calculate rest of p_n number while populating arrays for table
      for (( i=0; i<${#p_s}; i+=0 ))
      do
        num=0
        [[ "r-" =~ ${p_s:$i:1} ]] || return 1
        [[ ${p_s:$i:1} == 'r' ]] && R+=('X') || R+=(' ')
        [[ ${p_s:$((i++)):1} == 'r' ]] && let num++
        num=$(( num << 1 ))
        [[ "w-" =~ ${p_s:$i:1} ]] || return 1
        [[ ${p_s:$i:1} == 'w' ]] && W+=('X') || W+=(' ')
        [[ ${p_s:$((i++)):1} == 'w' ]] && let num++
        num=$(( num << 1 ))
        if [ $i -lt 6 ]
        then
          [[ "sSx-" =~ ${p_s:$i:1} ]] || return 1
          [[ "sx" =~ ${p_s:$i:1} ]] && X+=('X') || X+=(' ')
          [[ "sx" =~ ${p_s:$((i++)):1} ]] && let num++
        else
          [[ "tTx-" =~ ${p_s:$i:1} ]] || return 1
          [[ "tx" =~ ${p_s:$i:1} ]] && X+=('X') || X+=(' ')
          [[ "tx" =~ ${p_s:$((i++)):1} ]] && let num++
        fi
        p_n+="$num"
      done
    # PARTIAL STRING
    elif [[ $1 =~ ^[r,s,t,w,x]+$ ]]
    then
      p_s='---------'
      p_n0=0
      p_n1=0
      p_n2=0
      p_n3=0
      R=(' ' ' ' ' ')
      W=(' ' ' ' ' ')
      X=(' ' ' ' ' ')
      if [[ $1 =~ 'r' ]]
      then
        p_s=$(echo $p_s | sed 's/./r/1; s/./r/4; s/./r/7;')
        let p_n1+=4
        let p_n2+=4
        let p_n3+=4
        R=('X' 'X' 'X')
      fi
      if [[ $1 =~ 'w' ]]
      then
        p_s=$(echo $p_s | sed 's/./w/2')
        let p_n1+=2
        W=('X' ' ' ' ')
      fi
      if [[ $1 =~ 'x' ]]
      then
        p_s=$(echo $p_s | sed 's/./x/3; s/./x/6; s/./x/9;')
        let p_n1+=1
        let p_n2+=1
        let p_n3+=1
        X=('X' 'X' 'X')
      fi
      if [[ $1 =~ 's' ]]
      then
        [[ ${p_s:2:1} == 'x' ]] && p_s=$(echo $p_s | sed 's/./s/3') || p_s=$(echo $p_s | sed 's/./S/3')
        [[ ${p_s:5:1} == 'x' ]] && p_s=$(echo $p_s | sed 's/./s/6') || p_s=$(echo $p_s | sed 's/./S/6')
        let p_n0+=6
        setuid='X'
        setgid='X'
      fi
      if [[ $1 =~ 't' ]]
      then
        let p_n0+=1
        [[ ${p_s:8:1} == 'x' ]] && p_s=$(echo $p_s | sed 's/./t/9') || p_s=$(echo $p_s | sed 's/./T/9')
        sticky='X'
      fi
      p_n="${p_n0}${p_n1}${p_n2}${p_n3}"
    else
      return 1
    fi
  else
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

" | grcat "$GRC_STYLESHEET"
}

chmod_calc $@
[ $? -ne 0 ] && printf "Invalid permissions string: $@\n"
