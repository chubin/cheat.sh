#!/bin/sh

# Convert ANSI (terminal) colours and attributes to HTML

# Licence: LGPLv2
# Author:
#    http://www.pixelbeat.org/docs/terminal_colours/
# Examples:
#    ls -l --color=always | ansi2html.sh > ls.html
#    git show --color | ansi2html.sh > last_change.html
#    Generally one can use the `script` util to capture full terminal output.
# Changes:
#    V0.1, 24 Apr 2008, Initial release
#    V0.2, 01 Jan 2009, Phil Harnish <philharnish@gmail.com>
#                         Support `git diff --color` output by
#                         matching ANSI codes that specify only
#                         bold or background colour.
#                       P@draigBrady.com
#                         Support `ls --color` output by stripping
#                         redundant leading 0s from ANSI codes.
#                         Support `grep --color=always` by stripping
#                         unhandled ANSI codes (specifically ^[[K).
#    V0.3, 20 Mar 2009, http://eexpress.blog.ubuntu.org.cn/
#                         Remove cat -v usage which mangled non ascii input.
#                         Cleanup regular expressions used.
#                         Support other attributes like reverse, ...
#                       P@draigBrady.com
#                         Correctly nest <span> tags (even across lines).
#                         Add a command line option to use a dark background.
#                         Strip more terminal control codes.
#    V0.4, 17 Sep 2009, P@draigBrady.com
#                         Handle codes with combined attributes and color.
#                         Handle isolated <bold> attributes with css.
#                         Strip more terminal control codes.
#    V0.23, 22 Dec 2015
#      http://github.com/pixelb/scripts/commits/master/scripts/ansi2html.sh

gawk --version >/dev/null || exit 1

if [ "$1" = "--version" ]; then
    printf '0.22\n' && exit
fi

if [ "$1" = "--help" ]; then
    printf '%s\n' \
'This utility converts ANSI codes in data passed to stdin
It has 2 optional parameters:
   --bg=dark --palette=linux|solarized|tango|xterm
E.g.: ls -l --color=always | ansi2html.sh --bg=dark > ls.html' >&2
    exit
fi

[ "$1" = "--bg=dark" ] && { dark_bg=yes; shift; }

if [ "$1" = "--palette=solarized" ]; then
   # See http://ethanschoonover.com/solarized
   P0=073642;  P1=D30102;  P2=859900;  P3=B58900;
   P4=268BD2;  P5=D33682;  P6=2AA198;  P7=EEE8D5;
   P8=002B36;  P9=CB4B16; P10=586E75; P11=657B83;
  P12=839496; P13=6C71C4; P14=93A1A1; P15=FDF6E3;
  shift;
elif [ "$1" = "--palette=solarized-xterm" ]; then
   # Above mapped onto the xterm 256 color palette
   P0=262626;  P1=AF0000;  P2=5F8700;  P3=AF8700;
   P4=0087FF;  P5=AF005F;  P6=00AFAF;  P7=E4E4E4;
   P8=1C1C1C;  P9=D75F00; P10=585858; P11=626262;
  P12=808080; P13=5F5FAF; P14=8A8A8A; P15=FFFFD7;
  shift;
elif [ "$1" = "--palette=tango" ]; then
   # Gnome default
   P0=000000;  P1=CC0000;  P2=4E9A06;  P3=C4A000;
   P4=3465A4;  P5=75507B;  P6=06989A;  P7=D3D7CF;
   P8=555753;  P9=EF2929; P10=8AE234; P11=FCE94F;
  P12=729FCF; P13=AD7FA8; P14=34E2E2; P15=EEEEEC;
  shift;
elif [ "$1" = "--palette=xterm" ]; then
   P0=000000;  P1=CD0000;  P2=00CD00;  P3=CDCD00;
   P4=0000EE;  P5=CD00CD;  P6=00CDCD;  P7=E5E5E5;
   P8=7F7F7F;  P9=FF0000; P10=00FF00; P11=FFFF00;
  P12=5C5CFF; P13=FF00FF; P14=00FFFF; P15=FFFFFF;
  shift;
else # linux console
   P0=000000;  P1=AA0000;  P2=00AA00;  P3=AA5500;
   P4=0000AA;  P5=AA00AA;  P6=00AAAA;  P7=AAAAAA;
   P8=555555;  P9=FF5555; P10=55FF55; P11=FFFF55;
  P12=5555FF; P13=FF55FF; P14=55FFFF; P15=FFFFFF;
  [ "$1" = "--palette=linux" ] && shift
fi

[ "$1" = "--bg=dark" ] && { dark_bg=yes; shift; }

# Mac OSX's GNU sed is installed as gsed
# use e.g. homebrew 'gnu-sed' to get it
if ! sed --version >/dev/null 2>&1; then
  if gsed --version >/dev/null 2>&1; then
    alias sed=gsed
  else
    echo "Error, can't find an acceptable GNU sed." >&2
    exit 1
  fi
fi

printf '%s' "<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>
<link rel=\"search\" type=\"application/opensearchdescription+xml\" href=\"/files/opensearch.xml\" title=\"cheat.sh\" />
<link rel=\"stylesheet\" type=\"text/css\" href=\"/files/style.css\" />
<style type=\"text/css\">
.ef0,.f0 { color: #$P0; } .eb0,.b0 { background-color: #$P0; }
.ef1,.f1 { color: #$P1; } .eb1,.b1 { background-color: #$P1; }
.ef2,.f2 { color: #$P2; } .eb2,.b2 { background-color: #$P2; }
.ef3,.f3 { color: #$P3; } .eb3,.b3 { background-color: #$P3; }
.ef4,.f4 { color: #$P4; } .eb4,.b4 { background-color: #$P4; }
.ef5,.f5 { color: #$P5; } .eb5,.b5 { background-color: #$P5; }
.ef6,.f6 { color: #$P6; } .eb6,.b6 { background-color: #$P6; }
.ef7,.f7 { color: #$P7; } .eb7,.b7 { background-color: #$P7; }
.ef8, .f0 > .bold,.bold > .f0 { color: #$P8; font-weight: normal; }
.ef9, .f1 > .bold,.bold > .f1 { color: #$P9; font-weight: normal; }
.ef10,.f2 > .bold,.bold > .f2 { color: #$P10; font-weight: normal; }
.ef11,.f3 > .bold,.bold > .f3 { color: #$P11; font-weight: normal; }
.ef12,.f4 > .bold,.bold > .f4 { color: #$P12; font-weight: normal; }
.ef13,.f5 > .bold,.bold > .f5 { color: #$P13; font-weight: normal; }
.ef14,.f6 > .bold,.bold > .f6 { color: #$P14; font-weight: normal; }
.ef15,.f7 > .bold,.bold > .f7 { color: #$P15; font-weight: normal; }
.eb8  { background-color: #$P8; }
.eb9  { background-color: #$P9; }
.eb10 { background-color: #$P10; }
.eb11 { background-color: #$P11; }
.eb12 { background-color: #$P12; }
.eb13 { background-color: #$P13; }
.eb14 { background-color: #$P14; }
.eb15 { background-color: #$P15; }
"

# The default xterm 256 colour palette
for red in 0 1 2 3 4 5 ; do
  for green in 0 1 2 3 4 5 ; do
    for blue in 0 1 2 3 4 5 ; do
      c=$((16 + ($red * 36) + ($green * 6) + $blue))
      r=$((($red * 40 + 55) * ($red > 0)))
      g=$((($green * 40 + 55) * ($green > 0)))
      b=$((($blue * 40 + 55) * ($blue > 0)))
      printf ".ef%d { color: #%2.2x%2.2x%2.2x; } " $c $r $g $b
      printf ".eb%d { background-color: #%2.2x%2.2x%2.2x; }\n" $c $r $g $b
    done
  done
done
for gray in $(seq 0 23); do
  c=$(($gray+232))
  l=$(($gray*10 + 8))
  printf ".ef%d { color: #%2.2x%2.2x%2.2x; } " $c $l $l $l
  printf ".eb%d { background-color: #%2.2x%2.2x%2.2x; }\n" $c $l $l $l
done

printf '%s' '
.f9 { color: '`[ "$dark_bg" ] && printf "#$P7;" || printf "#$P0;"`' }
.b9 { background-color: #'`[ "$dark_bg" ] && printf $P0 || printf $P15`'; }
.f9 > .bold,.bold > .f9, body.f9 > pre > .bold {
  /* Bold is heavy black on white, or bright white
     depending on the default background */
  color: '`[ "$dark_bg" ] && printf "#$P15;" || printf "#$P0;"`'
  font-weight: '`[ "$dark_bg" ] && printf 'normal;' || printf 'bold;'`'
}
.reverse {
  /* CSS does not support swapping fg and bg colours unfortunately,
     so just hardcode something that will look OK on all backgrounds. */
  '"color: #$P0; background-color: #$P7;"'
}
.underline { text-decoration: underline; }
.line-through { text-decoration: line-through; }
.blink { text-decoration: blink; }

/* Avoid pixels between adjacent span elements.
   Note this only works for lines less than 80 chars
   where we close span elements on the same line.
span { display: inline-block; }
*/
</style>
</head>

<body class="">
<pre>
'

p='\x1b\['        #shortcut to match escape codes

# Handle various xterm control sequences.
# See /usr/share/doc/xterm-*/ctlseqs.txt
sed "
# escape ampersand and quote
s#&#\&amp;#g; s#\"#\&quot;#g;
s#\x1b[^\x1b]*\x1b\\\##g  # strip anything between \e and ST
s#\x1b][0-9]*;[^\a]*\a##g # strip any OSC (xterm title etc.)

s#\r\$## # strip trailing \r

# strip other non SGR escape sequences
s#[\x07]##g
s#\x1b[]>=\][0-9;]*##g
s#\x1bP+.\{5\}##g
# Mark cursor positioning codes \"Jr;c;
s#${p}\([0-9]\{1,2\}\)G#\"J;\1;#g
s#${p}\([0-9]\{1,2\}\);\([0-9]\{1,2\}\)H#\"J\1;\2;#g

# Mark clear as \"Cn where n=1 is screen and n=0 is to end-of-line
s#${p}H#\"C1;#g
s#${p}K#\"C0;#g
# Mark Cursor move columns as \"Mn where n is +ve for right, -ve for left
s#${p}C#\"M1;#g
s#${p}\([0-9]\{1,\}\)C#\"M\1;#g
s#${p}\([0-9]\{1,\}\)D#\"M-\1;#g
s#${p}\([0-9]\{1,\}\)P#\"X\1;#g

s#${p}[0-9;?]*[^0-9;?m]##g

" |

# Normalize the input before transformation
sed "
# escape HTML (ampersand and quote done above)
s#>#\&gt;#g; s#<#\&lt;#g;

# normalize SGR codes a little

# split 256 colors out and mark so that they're not
# recognised by the following 'split combined' line
:e
s#${p}\([0-9;]\{1,\}\);\([34]8;5;[0-9]\{1,3\}\)m#${p}\1m${p}¬\2m#g; t e
s#${p}\([34]8;5;[0-9]\{1,3\}\)m#${p}¬\1m#g;

:c
s#${p}\([0-9]\{1,\}\);\([0-9;]\{1,\}\)m#${p}\1m${p}\2m#g; t c   # split combined
s#${p}0\([0-7]\)#${p}\1#g                                 #strip leading 0
s#${p}1m\(\(${p}[4579]m\)*\)#\1${p}1m#g                   #bold last (with clr)
s#${p}m#${p}0m#g                                          #add leading 0 to norm

# undo any 256 color marking
s#${p}¬\([34]8;5;[0-9]\{1,3\}\)m#${p}\1m#g;

# map 16 color codes to color + bold
s#${p}9\([0-7]\)m#${p}3\1m${p}1m#g;
s#${p}10\([0-7]\)m#${p}4\1m${p}1m#g;

# change 'reset' code to \"R
s#${p}0m#\"R;#g
" |

# Convert SGR sequences to HTML
sed "
# common combinations to minimise html (optional)
:f
s#${p}3[0-7]m${p}3\([0-7]\)m#${p}3\1m#g; t f
:b
s#${p}4[0-7]m${p}4\([0-7]\)m#${p}4\1m#g; t b
s#${p}3\([0-7]\)m${p}4\([0-7]\)m#<span class=\"f\1 b\2\">#g
s#${p}4\([0-7]\)m${p}3\([0-7]\)m#<span class=\"f\2 b\1\">#g

s#${p}1m#<span class=\"bold\">#g
s#${p}4m#<span class=\"underline\">#g
s#${p}5m#<span class=\"blink\">#g
s#${p}7m#<span class=\"reverse\">#g
s#${p}9m#<span class=\"line-through\">#g
s#${p}3\([0-9]\)m#<span class=\"f\1\">#g
s#${p}4\([0-9]\)m#<span class=\"b\1\">#g

s#${p}38;5;\([0-9]\{1,3\}\)m#<span class=\"ef\1\">#g
s#${p}48;5;\([0-9]\{1,3\}\)m#<span class=\"eb\1\">#g

s#${p}[0-9;]*m##g # strip unhandled codes
" |

# Convert alternative character set and handle cursor movement codes
# Note we convert here, as if we do at start we have to worry about avoiding
# conversion of SGR codes etc., whereas doing here we only have to
# avoid conversions of stuff between &...; or <...>
#
# Note we could use sed to do this based around:
#   sed 'y/abcdefghijklmnopqrstuvwxyz{}`~/▒␉␌␍␊°±␤␋┘┐┌└┼⎺⎻─⎼⎽├┤┴┬│≤≥π£◆·/'
# However that would be very awkward as we need to only conv some input.
# The basic scheme that we do in the awk script below is:
#  1. enable transliterate once "T1; is seen
#  2. disable once "T0; is seen (may be on diff line)
#  3. never transliterate between &; or <> chars
#  4. track x,y movements and active display mode at each position
#  5. buffer line/screen and dump when required
sed "
# change 'smacs' and 'rmacs' to \"T1 and \"T0 to simplify matching.
s#\x1b(0#\"T1;#g;
s#\x0E#\"T1;#g;

s#\x1b(B#\"T0;#g
s#\x0F#\"T0;#g
" |
(
gawk '
function dump_line(l,del,c,blanks,ret) {
  for(c=1;c<maxX;c++) {
    if ((c SUBSEP l) in attr || length(cur)) {
      ret = ret blanks fixas(cur,attr[c,l])
      if(del) delete attr[c,l]
      blanks=""
    }
    if ((c SUBSEP l) in dump) {
      ret=ret blanks dump[c,l]
      if(del) delete dump[c,l]
      blanks=""
    } else blanks=blanks " "
  }
  if(length(cur)) ret=ret blanks
  return ret
}

function dump_screen(l,ret) {
  for(l=1;l<=maxY;l++)
    ret=ret dump_line(l,0) "\n"
  return ret fixas(cur, "")
}

function atos(a,i,ret) {
  for(i=1;i<=length(a);i++) if(i in a) ret=ret a[i]
  return ret
}

function fixas(a,s,spc,i,attr,rm,ret) {
  spc=length(a)
  l=split(s,attr,">")
  for(i=1;i<=spc;i++) {
    rm=rm?rm:(a[i]!=attr[i]">")
    if(rm) {
      ret=ret "</span>"
      delete a[i];
    }
  }
  for(i=1;i<l;i++) {
    attr[i]=attr[i]">"
    if(a[i]!=attr[i]) {
      a[i]=attr[i]
      ret = ret attr[i]
    }
  }
  return ret
}

function encode(string,start,end,i,ret,pos,sc,buf) {
   if(!end) end=length(string);
   if(!start) start=1;
   state=3
   for(i=1;i<=length(string);i++) {
     c=substr(string,i,1)
     if(state==2) {
       sc=sc c
       if(c==";") {
          c=sc
          state=last_mode
       } else continue
     } else {
       if(c=="\r") { x=1; continue }
       if(c=="<") {
         # Change attributes - store current active
         # attributes in span array
         split(substr(string,i),cord,">");
         i+=length(cord[1])
         span[++spc]=cord[1] ">"
         continue
       }
       else if(c=="&") {
         # All goes to single position till we see a semicolon
         sc=c
         state=2
         continue
       }
       else if(c=="\b") {
          # backspace move insertion point back 1
          if(spc) attr[x,y]=atos(span)
          x=x>1?x-1:1
          continue
       }
       else if(c=="\"") {
          split(substr(string,i+2),cord,";")
          cc=substr(string,i+1,1);
          if(cc=="T") {
              # Transliterate on/off
              if(cord[1]==1&&state==3) last_mode=state=4
              if(cord[1]==0&&state==4) last_mode=state=3
          }
          else if(cc=="C") {
              # Clear
              if(cord[1]+0) {
                # Screen - if Recording dump screen
                if(dumpStatus==dsActive) ret=ret dump_screen()
                dumpStatus=dsActive
                delete dump
                delete attr
                x=y=1
              } else {
                # To end of line
                for(pos=x;pos<maxX;pos++) {
                  dump[pos,y]=" "
                  if (!spc) delete attr[pos,y]
                  else attr[pos,y]=atos(span)
                }
              }
          }
          else if(cc=="J") {
              # Jump to x,y
              i+=length(cord[2])+1
              # If line is higher - dump previous screen
              if(dumpStatus==dsActive&&cord[1]<y) {
                ret=ret dump_screen();
                dumpStatus=dsNew;
              }
              x=cord[2]
              if(length(cord[1]) && y!=cord[1]){
                y=cord[1]
                if(y>maxY) maxY=y
                # Change y - start recording
                dumpStatus=dumpStatus?dumpStatus:dsReset
              }
          }
          else if(cc=="M") {
              # Move left/right on current line
              x+=cord[1]
          }
          else if(cc=="X") {
              # delete on right
              for(pos=x;pos<=maxX;pos++) {
                nx=pos+cord[1]
                if(nx<maxX) {
                  if((nx SUBSEP y) in attr) attr[pos,y] = attr[nx,y]
                  else delete attr[pos,y]
                  if((nx SUBSEP y) in dump) dump[pos,y] = dump[nx,y]
                  else delete dump[pos,y]
                } else if(spc) {
                  attr[pos,y]=atos(span)
                  dump[pos,y]=" "
                }
              }
          }
          else if(cc=="R") {
              # Reset attributes
              while(spc) delete span[spc--]
          }
          i+=length(cord[1])+2
          continue
       }
       else if(state==4&&i>=start&&i<=end&&c in Trans) c=Trans[c]
     }
     if(dumpStatus==dsReset) {
       delete dump
       delete attr
       ret=ret"\n"
       dumpStatus=dsActive
     }
     if(dumpStatus==dsNew) {
       # After moving/clearing we are now ready to write
       # something to the screen so start recording now
       ret=ret"\n"
       dumpStatus=dsActive
     }
     if(dumpStatus==dsActive||dumpStatus==dsOff) {
       dump[x,y] = c
       if(!spc) delete attr[x,y]
       else attr[x,y] = atos(span)
       if(++x>maxX) maxX=x;
     }
    }
    # End of line if dumping increment y and set x back to first col
    x=1
    if(!dumpStatus) return ret dump_line(y,1);
    else if(++y>maxY) maxY=y;
    return ret
}
BEGIN{
  OFS=FS
  # dump screen status
  dsOff=0    # Not dumping screen contents just write output direct
  dsNew=1    # Just after move/clear waiting for activity to start recording
  dsReset=2  # Screen cleared build new empty buffer and record
  dsActive=3 # Currently recording
  F="abcdefghijklmnopqrstuvwxyz{}`~"
  T="▒␉␌␍␊°±␤␋┘┐┌└┼⎺⎻─⎼⎽├┤┴┬│≤≥π£◆·"
  maxX=80
  delete cur;
  x=y=1
  for(i=1;i<=length(F);i++)Trans[substr(F,i,1)]=substr(T,i,1);
}

{ $0=encode($0) }
1
END {
  if(dumpStatus) {
    print dump_screen();
  }
}'
)

printf '</pre>
</body>
</html>\n'
