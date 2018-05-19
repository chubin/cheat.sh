_cht_complete()
{
    local cur prev opts
    _get_comp_words_by_ref -n : cur

    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="$(curl -s cheat.sh/:list)"

    if [ ${COMP_CWORD} = 1 ]; then
	  COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
	  __ltrim_colon_completions "$cur"
    fi
    return 0
}
complete -F _cht_complete cht.sh
