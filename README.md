```

          oooo                                .                oooo        
          `888                              .o8                `888        
 .ooooo.   888 .oo.    .ooooo.   .oooo.   .o888oo      .oooo.o  888 .oo.   
d88' `"Y8  888P"Y88b  d88' `88b `P  )88b    888       d88(  "8  888P"Y88b  
888        888   888  888ooo888  .oP"888    888       `"Y88b.   888   888  
888   .o8  888   888  888    .o d8(  888    888 . .o. o.  )88b  888   888  
`Y8bod8P' o888o o888o `Y8bod8P' `Y888""8o   "888" Y8P 8""888P' o888o o888o 


```

![cheat.sh usage](http://igor.chub.in/download/cheatsh-en.gif)

## Features

* simple curl/browser interface
* available everywhere, no installation needed
* tab completion
* search on a cheat sheet and in all cheat sheets
* syntax highlighting
* uses community driven cheat sheets repositories

Usage examples:

```
    $ curl cheat.sh/rsync
    $ curl cheat.sh/btrfs~volume
    $ curl cheat.sh/~snapshot
    $ curl cheat.sh/scala/Functions
    $ curl cheat.sh/scala/Functions~map
```

## Options

```
    T                   omit terminal sequences (no colors; can be pasted in an editor)
```

## Special URLs

Special URLs:

```
    /:help             # show help page
    /:post             # how to post new cheat sheets
    /:list             # list all known cheat sheets
```

## Tab completion

```
    $ curl cheat.sh/:bash_completion > ~/.bash.d/cheat.sh
    $ . ~/.bash.d/cheat.sh
    $ # add . ~/.bash.d/cheat.sh to ~/.bashrc
```

## Search

To search for a keyword, use the query:

```
    /~keyword
```

In this case search is not recursive — it is conducted only in a pages of the specified level.
For example:

```
    /~snapshot          look for snapshot in the first level cheat sheets 
    /scala/~currying     look for currying in scala cheat sheets
```

For a recursive search in all cheat sheets, use double slash:

```
    /~snapshot/r         look for snapshot in all cheat sheets
```

You can use special search options after the closing slash:

```
    /~shot/bi           case insensitive (i), word boundaries (b)
```

List of search options:

```
    i   case insensitive search
    b   word boundaries
    r   recursive search
```

## Cheat sheets sources

cheat.sh uses several community driven repositories
of cheat sheets:

* [cheat.sheets](https://github.com/chubin/cheat.sheets) [1 contributor][0 stars][May 1, 2017]

External repositories:

* [tldr-pages/tldr](https://github.com/tldr-pages/tldr) [331 contributors][9.222 stars][Dec 8, 2013]
* [chrisallenlane/cheat](https://github.com/chrisallenlane/cheat) [93 contributors][3.144 stars][Jul 28, 2013]
* [a8m/go-lang-cheat-sheet](https://github.com/a8m/go-lang-cheat-sheet) [23 contributors][2.009 stars][Feb 9, 2014]
* [adambard/learnxinyminutes-docs](https://github.com/adambard/learnxinyminutes-docs) [985 contributors][4.405 stars][Jun 23, 2013]

## How to add a cheat sheet

If you want to add a cheat sheet, you have one of the following
ways:

* Add it to one of the external cheat sheets repositories; you should decide on your own what is the best repository for your cheat sheet;
* Add it to the local cheat.sh repository ([cheat.sheets](https://github.com/chubin/cheat.sheets)) on github (fork, commit, pull request);
* Post it on cheat.sh using curl or a web browser ([cheat.sh/:post](http://cheat.sh/:post)).

If you want to change an existing cheat sheet,
you have to find the original repository (when you open a cheat sheet in a browser,
you see the repository's github button in the bottom of the cheat sheet),
the cheat sheet is coming from, and change it there.
After some time the changes will be synchronized on cheat.sh.

