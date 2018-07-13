#compdef cht.sh

__CHTSH_LANGS=($(curl -s cheat.sh/:list))
_arguments -C \
  '--help[show this help message and exit]: :->noargs' \
  '--shell[enter shell repl]: :->noargs' \
  '1:Cheat Sheet:->lang' \
  '*::: :->noargs' && return 0

if [[ CURRENT -ge 1 ]]; then
    case $state in
        noargs)
             _message "nothing to complete";;
        lang)
             compadd -X "Cheat Sheets" ${__CHTSH_LANGS[@]};;
        *)
             _message "Unknown state, error in autocomplete";;
    esac

    return
fi

