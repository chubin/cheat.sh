#!/bin/bash
# shellcheck disable=SC1117,SC2001
#
# [X] open section
# [X] one shot mode
# [X] usage info
# [X] dependencies check
# [X] help
# [X] yank/y/copy/c
# [X] Y/C
# [X] eof problem
# [X] more
# [X] stealth mode
#
# here are several examples for the stealth mode:
#
# zip lists
# list permutation
# random list element
# reverse a list
# read json from file
# append string to a file
# run process in background
# count words in text counter
# group elements list

__CHTSH_VERSION=6
__CHTSH_DATETIME="2019-06-05 18:00:46 +0200"

# cht.sh configuration loading
#
# configuration is stored in ~/.cht.sh/ (can be overridden by CHTSH_HOME)
#
CHTSH_HOME=${CHTSH:-"$HOME"/.cht.sh}
[ -z "$CHTSH_CONF" ] && CHTSH_CONF=$CHTSH_HOME/cht.sh.conf
# shellcheck disable=SC1090,SC2002
[ -e "$CHTSH_CONF" ] && source "$CHTSH_CONF"
[ -z "$CHTSH_URL" ] && CHTSH_URL=https://cht.sh

# currently we support only two modes:
# * lite = access the server using curl
# * auto = try standalone usage first
CHTSH_MODE="$(cat "$CHTSH_HOME"/mode 2> /dev/null)"
[ "$CHTSH_MODE" != lite ] && CHTSH_MODE=auto
CHEATSH_INSTALLATION="$(cat "$CHTSH_HOME/standalone" 2> /dev/null)"


export LESSSECURE=1
STEALTH_MAX_SELECTION_LENGTH=5

case "$(uname -s)" in
  Darwin) is_macos=yes ;;
  *) is_macos=no ;;
esac

# for KSH93
# shellcheck disable=SC2034,SC2039,SC2168
if echo "$KSH_VERSION" | grep -q ' 93' && ! local foo 2>/dev/null; then
  alias local=typeset
fi

fatal()
{
  echo "ERROR: $*" >&2
  exit 1
}

_say_what_i_do()
{
  [ -n "$LOG" ] && echo "$(date '+[%Y-%m-%d %H:%M%S]') $*" >> "$LOG"

  local this_prompt="\033[0;1;4;32m>>\033[0m"
  printf "\n${this_prompt}%s\033[0m\n" " $* "
}

cheatsh_standalone_install()
{
  # the function installs cheat.sh with the upstream repositories
  # in the standalone mode
  local installdir; installdir="$1"
  local default_installdir="$HOME/.cheat.sh"

  if [ "$installdir" = help ]; then
    cat <<EOF
Install cheat.sh in the standalone mode.

After the installation, cheat.sh can be used locally, without accessing
the public cheat.sh service, or it can be used in the server mode,
where the newly installed server could be accessed by external clients
in the same fashion as the public cheat.sh server.

During the installation, cheat.sh code as well as the cheat.sh upstream
cheat sheets repositories will be fetched.

It takes approximately 1G of the disk space.

Default installation location:  ~/.cheat.sh/
It can be overridden by a command line parameter to this script:

    ${0##*/} --standalone-install DIR

See cheat.sh/:standalone or https://github.com/chubin/cheat.sh/README.md
for more information:

    cht.sh :standalone
    curl cheat.sh/:standalone

After the installation is finished, the cht.sh shell client is switched
to the auto mode, where it uses the local cheat.sh installation if possible.
You can switch the mode with the --mode switch:

    cht.sh --mode lite      # use https://cheat.sh/ only
    cht.sh --mode auto      # use local installation

For intallation and standalone usage, you need \`git\`, \`python\`,
and \`virtualenv\` to be installed locally.
EOF
    return
  fi

  local _exit_code=0

  local dependencies=(python git virtualenv)
  for dep in "${dependencies[@]}"; do
    command -v "$dep" >/dev/null || \
    { echo "DEPENDENCY: \"$dep\" is needed to install cheat.sh in the standalone mode" >&2; _exit_code=1; }
  done
  [ "$_exit_code" -ne 0 ] && return "$_exit_code"

  while true; do
    echo -n "Where should cheat.sh be installed [$default_installdir]? "; read -r installdir
    [ -n "$installdir" ] || installdir="$default_installdir"

    if [ "$installdir" = y ] \
        || [ "$installdir" = Y ] \
        || [ "$(echo "$installdir" | tr "[:upper:]" "[:lower:]")" = yes ]
    then
      echo Please enter the directory name
      echo If it was the directory name already, please prepend it with \"./\": "./$installdir"
    else
      break
    fi
  done

  if [ -e "$installdir" ]; then
    echo "ERROR: Installation directory [$installdir] exists already"
    echo "Please remove it first before continuing"
    return 1
  fi

  if ! mkdir -p "$installdir"; then
    echo "ERROR: Could not create the installation directory \"$installdir\""
    echo "ERROR: Please check the permissions and start the script again"
    return 1
  fi

  local space_needed=700
  local space_available; space_available=$(($(df -k "$installdir" | awk '{print $4}' | tail -1)/1024))

  if [ "$space_available" -lt "$space_needed" ]; then
    echo "ERROR: Installation directory has no enough space (needed: ${space_needed}M, available: ${space_available}M"
    echo "ERROR: Please clean up and start the script again"
    rmdir "$installdir"
    return 1
  fi

  _say_what_i_do Cloning cheat.sh locally
  local url=https://github.com/chubin/cheat.sh
  rmdir "$installdir"
  git clone "$url" "$installdir" || fatal Could not clone "$url" with git into "$installdir"
  cd "$installdir" || fatal "Cannot cd into $installdir"

  # after the repository cloned, we may have the log directory
  # and we can write our installation log into it
  mkdir -p "$installdir/log/"
  LOG="$installdir/log/install.log"

  # we use tee everywhere so we should set -o pipefail
  set -o pipefail

  # currently the script uses python 2,
  # but cheat.sh supports python 3 too
  # if you want to switch it to python 3
  # set PYTHON2 to NO:
  # PYTHON2=NO
  #
  PYTHON2=YES
  if [[ $PYTHON2 = YES ]]; then
    python="python2"
    pip="pip"
    virtualenv_python3_option=()
  else
    python="python3"
    pip="pip3"
    virtualenv_python3_option=(-p python3)
  fi

  _say_what_i_do Creating virtual environment
  "$python" "$(command -v virtualenv)" "${virtualenv_python3_option[@]}" ve \
      || fatal Could not create virtual environment with "python2 $(command -v virtualenv) ve"

  # rapidfuzz does not support Python 2,
  # so if we are using Python 2, install fuzzywuzzy instead
  if [[ $PYTHON2 = YES ]]; then
    sed -i s/rapidfuzz/fuzzywuzzy/ requirements.txt
    echo "python-Levenshtein" >> requirements.txt
  fi

  _say_what_i_do Installing python requirements into the virtual environment
  ve/bin/"$pip" install -r requirements.txt > "$LOG" \
      || {

    echo "ERROR:"
    echo "---"
    tail -n 10 "$LOG"
    echo "---"
    echo "See $LOG for more"
    fatal Could not install python dependencies into the virtual environment
  }
  echo "$(ve/bin/"$pip" freeze | wc -l) dependencies were successfully installed"

  _say_what_i_do Fetching the upstream cheat sheets repositories
  ve/bin/python lib/fetch.py fetch-all | tee -a "$LOG"

  _say_what_i_do Running self-tests
  (
    cd tests || exit

    if CHEATSH_TEST_STANDALONE=YES \
       CHEATSH_TEST_SKIP_ONLINE=NO \
       CHEATSH_TEST_SHOW_DETAILS=NO \
       PYTHON=../ve/bin/python bash run-tests.sh | tee -a "$LOG"
    then
      printf "\033[0;32m%s\033[0m\n" "SUCCESS"
    else
      printf "\033[0;31m%s\033[0m\n" "FAILED"
      echo "Some tests were failed. Run the tests manually for further investigation:"
      echo "  cd $PWD; bash run-tests.sh)"
    fi
  )

  mkdir -p "$CHTSH_HOME"
  echo "$installdir" > "$CHTSH_HOME/standalone"
  echo auto > "$CHTSH_HOME/mode"

  _say_what_i_do Done

  local v1; v1=$(printf "\033[0;1;32m")
  local v2; v2=$(printf "\033[0m")

  cat <<EOF | sed "s/{/$v1/; s/}/$v2/"

{      _      }
{     \\ \\   }     The installation is successfully finished.
{      \\ \\  }
{      / /    }   Now you can use cheat.sh in the standalone mode,
{     /_/     }   or you can start your own cheat.sh server.


Now the cht.sh shell client is switched to the auto mode, where it uses
the local cheat.sh installation if possible.
You can switch the mode with the --mode switch:

    cht.sh --mode lite      # use https://cheat.sh/ only
    cht.sh --mode auto      # use local installation

You can add your own cheat sheets repository (config is in \`etc/config.yaml\`),
or create new cheat sheets adapters (in \`lib/adapters\`).

To update local copies of cheat sheets repositores on a regular basis,
add the following line to your user crontab (crontab -e):

    10 * * * * $installdir/ve/bin/python $installdir/lib/fetch.py update-all

All cheat sheets will be automatically actualized each hour.

If you are running a server reachable from the Internet, it can be instantly
notified via a HTTP request about any cheat sheets changes. For that, please
open an issue on the cheat.sh project repository [github.com/chubin/cheat.sh]
with the ENTRY-POINT from the URL https://ENTRY-POINT/:actualize specified
EOF
}

chtsh_mode()
{
  local mode="$1"

  local text; text=$(
    echo "  auto    use the standalone installation first"
    echo "  lite    use the cheat sheets server directly"
  )

  if [ -z "$mode" ]; then
    echo "current mode: $CHTSH_MODE ($(printf "%s" "$text" | grep "$CHTSH_MODE" | sed "s/$CHTSH_MODE//; s/^ *//; s/ \+/ /"))"
    if [ -d "$CHEATSH_INSTALLATION" ]; then
      echo "cheat.sh standalone installation: $CHEATSH_INSTALLATION"
    else
      echo 'cheat.sh standalone installation not found; falling back to the "lite" mode'
    fi
  elif [ "$mode" = auto ] || [ "$mode" = lite ]; then
    if [ "$mode" = "$CHTSH_MODE" ]; then
      echo "The configured mode was \"$CHTSH_MODE\"; nothing changed"
    else
      mkdir -p "$CHTSH_HOME"
      echo "$mode" > "$CHTSH_HOME/mode"
      echo "Configured mode: $mode"
    fi
  else
    echo "Unknown mode: $mode"
    echo Supported modes:
    echo "  auto    use the standalone installation first"
    echo "  lite    use the cheat sheets server directly"
  fi
}

get_query_options()
{
  local query="$*"
  if [ -n "$CHTSH_QUERY_OPTIONS" ]; then
    case $query in
      *\?*)   query="$query&${CHTSH_QUERY_OPTIONS}";;
      *)      query="$query?${CHTSH_QUERY_OPTIONS}";;
    esac
  fi
  printf "%s" "$query"
}

do_query()
{
  local query="$*"
  local b_opts=
  local uri="${CHTSH_URL}/\"\$(get_query_options $query)\""

  if [ -e "$HOME/.cht.sh/id" ]; then
    b_opts="-b \"\$HOME/.cht.sh/id\""
  fi

  eval curl "$b_opts" -s "$uri" > "$TMP1"

  if [ -z "$lines" ] || [ "$(wc -l "$TMP1" | awk '{print $1}')" -lt "$lines" ]; then
    cat "$TMP1"
  else
    ${PAGER:-$defpager} "$TMP1"
  fi
}

prepare_query()
{
  local section="$1"; shift
  local input="$1"; shift
  local arguments="$1"

  local query
  if [ -z "$section" ] || [ x"${input}" != x"${input#/}" ]; then
    query=$(printf %s "$input" | sed 's@ @/@; s@ @+@g')
  else
    query=$(printf %s "$section/$input" | sed 's@ @+@g')
  fi

  [ -n "$arguments" ] && arguments="?$arguments"
  printf %s "$query$arguments"
}

get_list_of_sections()
{
  curl -s "${CHTSH_URL}"/:list | grep -v '/.*/' | grep '/$' | xargs
}

gen_random_str()
(
  len=$1
  if command -v openssl >/dev/null; then
    openssl rand -base64 $((len*3/4)) | awk -v ORS='' //
  else
    rdev=/dev/urandom
    for d in /dev/{srandom,random,arandom}; do
      test -r "$d" && rdev=$d
    done
    if command -v hexdump >/dev/null; then
      hexdump -vn $((len/2)) -e '1/1 "%02X" 1 ""' "$rdev"
    elif command -v xxd >/dev/null; then
      xxd -l $((len/2)) -ps "$rdev" | awk -v ORS='' //
    else
      cd /tmp || { echo Cannot cd into /tmp >&2; exit 1; }
      s=
      # shellcheck disable=SC2000
      while [ "$(echo "$s" | wc -c)" -lt "$len" ]; do
        s="$s$(mktemp -u XXXXXXXXXX)"
      done
      printf "%.${len}s" "$s"
    fi
  fi
)

if [ "$CHTSH_MODE" = auto ] && [ -d "$CHEATSH_INSTALLATION" ]; then
  curl() {
    # ignoring all options
    # currently the standalone.py does not support them anyway
    local opt
    while getopts "b:s" opt; do
      :
    done
    shift $((OPTIND - 1))

    local url; url="$1"; shift
    PYTHONIOENCODING=UTF-8 "$CHEATSH_INSTALLATION/ve/bin/python" "$CHEATSH_INSTALLATION/lib/standalone.py" "${url#"$CHTSH_URL"}" "$@"
  }
elif [ "$(uname -s)" = OpenBSD ] && [ -x /usr/bin/ftp ]; then
  # any better test not involving either OS matching or actual query?
  curl() {
    local opt args="-o -"
    while getopts "b:s" opt; do
      case $opt in
        b) args="$args -c $OPTARG";;
        s) args="$args -M -V";;
        *) echo "internal error: unsupported cURL option '$opt'" >&2; exit 1;;
      esac
    done
    shift $((OPTIND - 1))
    /usr/bin/ftp "$args" "$@"
  }
else
  command -v curl   >/dev/null || { echo 'DEPENDENCY: install "curl" to use cht.sh' >&2; exit 1; }
  _CURL=$(command -v curl)
  if [ x"$CHTSH_CURL_OPTIONS" != x ]; then
    curl() {
      $_CURL "${CHTSH_CURL_OPTIONS}" "$@"
    }
  fi
fi

if [ "$1" = --read ]; then
  read -r a || a="exit"
  printf "%s\n" "$a"
  exit 0
elif [ x"$1" = x--help ] || [ -z "$1" ]; then

  n=${0##*/}
  s=$(echo "$n" | sed "s/./ /"g)

  cat <<EOF
Usage:

    $n [OPTIONS|QUERY]

Options:

    QUERY                   process QUERY and exit

    --help                  show this help
    --shell [LANG]          shell mode (open LANG if specified)

    --standalone-install [DIR|help]
                            install cheat.sh in the standalone mode
                            (by default, into ~/.cheat.sh/)

    --mode [auto|lite]      set (or display) mode of operation
                            * auto - prefer the local installation
                            * lite - use the cheat sheet server

EOF
  exit 0
elif [ x"$1" = x--shell ]; then
  shell_mode=yes
  shift
elif [ x"$1" = x--standalone-install ]; then
  shift
  cheatsh_standalone_install "$@"
  exit "$?"
elif [ x"$1" = x--mode ]; then
  shift
  chtsh_mode "$@"
  exit "$?"
fi

prompt="cht.sh"
opts=""
input=""
for o; do
  if [ x"$o" != x"${o#-}" ]; then
    opts="${opts}${o#-}"
  else
    input="$input $o"
  fi
done
query=$(echo "$input" | sed 's@ *$@@; s@^ *@@; s@ @/@; s@ @+@g')

if [ "$shell_mode" != yes ]; then
  curl -s "${CHTSH_URL}"/"$(get_query_options "$query")"
  exit 0
else
  new_section="$1"
  valid_sections=$(get_list_of_sections)
  valid=no; for q in $valid_sections; do [ "$q" = "$new_section/" ] && { valid=yes; break; }; done

  if [ "$valid" = yes ]; then
    section="$new_section"
    # shellcheck disable=SC2001
    this_query="$(echo "$input" | sed 's@ *[^ ]* *@@')"
    this_prompt="\033[0;32mcht.sh/$section>\033[0m "
  else
    this_query="$input"
    this_prompt="\033[0;32mcht.sh>\033[0m "
  fi
  if [ -n "$this_query" ] && [ -z "$CHEATSH_RESTART" ]; then
    printf "$this_prompt$this_query\n"
    curl -s "${CHTSH_URL}"/"$(get_query_options "$query")"
  fi
fi

if [ "$is_macos" != yes ]; then
  command -v xsel >/dev/null ||   echo 'DEPENDENCY: please install "xsel" for "copy"' >&2
fi
command -v rlwrap >/dev/null || { echo 'DEPENDENCY: install "rlwrap" to use cht.sh in the shell mode' >&2; exit 1; }

mkdir -p "$HOME/.cht.sh/"
lines=$(tput lines)

if command -v less >/dev/null; then
  defpager="less -R"
elif command -v more >/dev/null; then
  defpager="more"
else
  defpager="cat"
fi

cmd_cd() {
  if [ $# -eq 0 ]; then
    section=""
  else
    new_section=$(echo "$input" | sed 's/cd  *//; s@/*$@@; s@^/*@@')
    if [ -z "$new_section" ] || [ ".." = "$new_section" ]; then
      section=""
    else
      valid_sections=$(get_list_of_sections)
      valid=no; for q in $valid_sections; do [ "$q" = "$new_section/" ] && { valid=yes; break; }; done
      if [ "$valid" = no ]; then
        echo "Invalid section: $new_section"
        echo "Valid sections:"
        echo "$valid_sections" \
            | xargs printf "%-10s\n" \
            | tr ' ' .  \
            | xargs -n 10 \
            | sed 's/\./ /g; s/^/  /'
      else
        section="$new_section"
      fi
    fi
  fi
}

cmd_copy() {
  if [ -z "$DISPLAY" ]; then
    echo copy: supported only in the Desktop version
  elif [ -z "$input" ]; then
    echo copy: Make at least one query first.
  else
    curl -s "${CHTSH_URL}"/"$(get_query_options "$query"?T)" > "$TMP1"
    if [ "$is_macos" != yes ]; then
      xsel -bi < "$TMP1"
    else
      pbcopy < "$TMP1"
    fi
    echo "copy: $(wc -l "$TMP1" | awk '{print $1}') lines copied to the selection"
  fi
}

cmd_ccopy() {
  if [ -z "$DISPLAY" ]; then
    echo copy: supported only in the Desktop version
  elif [ -z "$input" ]; then
    echo copy: Make at least one query first.
  else
    curl -s "${CHTSH_URL}"/"$(get_query_options "$query"?TQ)" > "$TMP1"
    if [ "$is_macos" != yes ]; then
      xsel -bi < "$TMP1"
    else
      pbcopy < "$TMP1"
    fi
    echo "copy: $(wc -l "$TMP1" | awk '{print $1}') lines copied to the selection"
  fi
}

cmd_exit() {
  exit 0
}

cmd_help() {
  cat <<EOF
help    - show this help
hush    - do not show the 'help' string at start anymore
cd LANG - change the language context
copy    - copy the last answer in the clipboard (aliases: yank, y, c)
ccopy   - copy the last answer w/o comments (cut comments; aliases: cc, Y, C)
exit    - exit the cheat shell (aliases: quit, ^D)
id [ID] - set/show an unique session id ("reset" to reset, "remove" to remove)
stealth - stealth mode (automatic queries for selected text)
update  - self update (only if the scriptfile is writeable)
version - show current cht.sh version
/:help  - service help
QUERY   - space separated query staring (examples are below)
              cht.sh> python zip list
              cht.sh/python> zip list
              cht.sh/go> /python zip list
EOF
}

cmd_hush() {
  mkdir -p "$HOME/.cht.sh/" && touch "$HOME/.cht.sh/.hushlogin" && echo "Initial 'use help' message was disabled"
}

cmd_id() {
  id_file="$HOME/.cht.sh/id"

  if [ id = "$input" ]; then
    new_id=""
  else
    new_id=$(echo "$input" | sed 's/id  *//; s/ *$//; s/ /+/g')
  fi
  if [ "$new_id" = remove ]; then
    if [ -e "$id_file" ]; then
      rm -f -- "$id_file" && echo "id is removed"
    else
      echo "id was not set, so you can't remove it"
    fi
    return
  fi
  if [ -n "$new_id" ] && [ reset != "$new_id" ] && [ "$(/bin/echo -n "$new_id" | wc -c)" -lt 16 ]; then
    echo "ERROR: $new_id: Too short id. Minimal id length is 16. Use 'id reset' for a random id"
    return
  fi
  if [ -z "$new_id" ]; then
    # if new_id is not specified check if we have some id already
    # if yes, just show it
    # if not, generate a new id
    if [ -e "$id_file" ]; then
      awk '$6 == "id" {print $NF}' <"$id_file" | tail -n 1
      return
    else
      new_id=reset
    fi
  fi
  if [ "$new_id" = reset ]; then
    new_id=$(gen_random_str 12)
  else
    echo WARNING: if someone gueses your id, he can read your cht.sh search history
  fi
  if [ -e "$id_file" ] && grep -q '\tid\t[^\t][^\t]*$' "$id_file" 2> /dev/null; then
    sed -i 's/\tid\t[^\t][^\t]*$/ id '"$new_id"'/' "$id_file"
  else
    if ! [ -e "$id_file" ]; then
      printf '#\n\n' > "$id_file"
    fi
    printf ".cht.sh\tTRUE\t/\tTRUE\t0\tid\t$new_id\n" >> "$id_file"
  fi
  echo "$new_id"
}

cmd_query() {
  query=$(prepare_query "$section" "$input")
  do_query "$query"
}

cmd_stealth() {
  if [ "$input" != stealth ]; then
    arguments=$(echo "$input" | sed 's/stealth //; s/ /\&/')
  fi
  trap break INT
  if [ "$is_macos" = yes ]; then
    past=$(pbpaste)
  else
    past=$(xsel -o)
  fi
  printf "\033[0;31mstealth:\033[0m you are in the stealth mode; select any text in any window for a query\n"
  printf "\033[0;31mstealth:\033[0m selections longer than $STEALTH_MAX_SELECTION_LENGTH words are ignored\n"
  if [ -n "$arguments" ]; then
    printf "\033[0;31mstealth:\033[0m query arguments: ?$arguments\n"
  fi
  printf "\033[0;31mstealth:\033[0m use ^C to leave this mode\n"
  while true; do
    if [ "$is_macos" = yes ]; then
      current=$(pbpaste)
    else
      current=$(xsel -o)
    fi
    if [ "$past" != "$current" ]; then
      past=$current
      current_text="$(echo $current | tr -c '[a-zA-Z0-9]' ' ')"
      if [ "$(echo "$current_text" | wc -w)" -gt "$STEALTH_MAX_SELECTION_LENGTH" ]; then
        echo "\033[0;31mstealth:\033[0m selection length is longer than $STEALTH_MAX_SELECTION_LENGTH words; ignoring"
        continue
      else
        printf "\n\033[0;31mstealth: \033[7m $current_text\033[0m\n"
        query=$(prepare_query "$section" "$current_text" "$arguments")
        do_query "$query"
      fi
    fi
    sleep 1;
  done
  trap - INT
}

cmd_update() {
  [ -w "$0" ] || { echo "The script is readonly; please update manually: curl -s ${CHTSH_URL}/:cht.sh | sudo tee $0"; return; }
  TMP2=$(mktemp /tmp/cht.sh.XXXXXXXXXXXXX)
  curl -s "${CHTSH_URL}"/:cht.sh > "$TMP2"
  if ! cmp "$0" "$TMP2" > /dev/null 2>&1; then
    if grep -q ^__CHTSH_VERSION= "$TMP2"; then
      # section was vaildated by us already
      args=(--shell "$section")
      cp "$TMP2" "$0" && echo "Updated. Restarting..." && rm "$TMP2" && CHEATSH_RESTART=1 exec "$0" "${args[@]}"
    else
      echo "Something went wrong. Please update manually"
    fi
  else
    echo "cht.sh is up to date. No update needed"
  fi
  rm -f "$TMP2" > /dev/null 2>&1
}

cmd_version() {
  insttime=$(ls -l -- "$0" | sed 's/  */ /g' | cut -d ' ' -f 6-8)
  echo "cht.sh version $__CHTSH_VERSION of $__CHTSH_DATETIME; installed at: $insttime"
  TMP2=$(mktemp /tmp/cht.sh.XXXXXXXXXXXXX)
  if curl -s "${CHTSH_URL}"/:cht.sh > "$TMP2"; then
    if ! cmp "$0" "$TMP2" > /dev/null 2>&1; then
      echo "Update needed (type 'update' for that)".
    else
      echo "Up to date. No update needed"
    fi
  fi
  rm -f "$TMP2" > /dev/null 2>&1
}

TMP1=$(mktemp /tmp/cht.sh.XXXXXXXXXXXXX)
trap 'rm -f $TMP1 $TMP2' EXIT
trap 'true' INT

if ! [ -e "$HOME/.cht.sh/.hushlogin" ] && [ -z "$this_query" ]; then
  echo "type 'help' for the cht.sh shell help"
fi

while true; do
  if [ "$section" != "" ]; then
    full_prompt="$prompt/$section> "
  else
    full_prompt="$prompt> "
  fi

  input=$(
    rlwrap -H "$HOME/.cht.sh/history" -pgreen -C cht.sh -S "$full_prompt" bash "$0" --read | sed 's/ *#.*//'
  )

  cmd_name=${input%% *}
  cmd_args=${input#* }
  case $cmd_name in
    "")             continue;;   # skip empty input lines
    '?'|h|help)     cmd_name=help;;
    hush)           cmd_name=hush;;
    cd)             cmd_name="cd";;
    exit|quit)      cmd_name="exit";;
    copy|yank|c|y)  cmd_name=copy;;
    ccopy|cc|C|Y)   cmd_name=ccopy;;
    id)             cmd_name=id;;
    stealth)        cmd_name=stealth;;
    update)         cmd_name=update;;
    version)        cmd_name=version;;
    *)              cmd_name="query"; cmd_args="$input";;
  esac
  "cmd_$cmd_name" $cmd_args 
done
