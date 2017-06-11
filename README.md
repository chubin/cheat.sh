
![cheat.sh logo](http://cheat.sh/files/big-logo.png)

Unified read, search and write access to the popular cheat sheets repositories.

## Features

* simple curl/browser interface
* available everywhere, no installation needed
* selected popular well maintained community driven cheat sheets repositories
* search (on a cheat sheet and in all cheat sheets)
* tab completion
* syntax highlighting
* editors integration

## Usage

To read a cheat sheet:

```
    curl cheat.sh/sudo
```

Here `sudo` is the name of the cheat sheet you are looking for.

If you don't know the name of the topic you need,
you can search for it using the ~KEYWORD notation.
For example, to see how you can make snapshots, you make the following query

```
    ~snapshot
```

and get the list of snapshot creation examples commands.

Programming languages cheat sheets are located in correspondent namespaces,
named after the name of the language:

```
    scala/Functions
```

Read more about the programming languages cheat sheets below.

There are several special pages (their name are always starting with a colon),
that are not cheat sheets and have special meaning. For example:

```
    :help           
    :list           list all cheat sheets
    /perl/:list     list all perl cheat sheets
```

cheat.sh supports tab completion in a shell and in a browser.
All major shells are supported. Read more on it in the *Tab completion* section.

cheat.sh uses syntax highlighting by default.
You can switch it off, or choose other color scheme for it.
Use URL options for that. More on it in the *Options* section below.


Usage examples:

```
    $ curl cheat.sh/cpio
    $ curl cheat.sh/~snapshot
    $ curl cheat.sh/go/range
    $ curl cheat.sh/rust/hello
    $ curl cheat.sh/rust/hello?T
```

![cheat.sh usage](http://igor.chub.in/download/cheatsh-en.gif)

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

## Special pages

Special pages:

```
    :help               this page
    :list               list all cheat sheets
    :post               how to post new cheat sheet
    :bash_completion    bash function for tab completion
    :bash               bash function and tab completion setup
    :fish               fish function and tab completion setup
    :zsh                zsh function and tab completion setup
    :emacs              cheat.sh function for Emacs
    :emacs-ivy          cheat.sh function for Emacs (uses ivy)
    :styles             list of color styles
    :styles-demo        show color styles usage examples
```

## Tab completion

Tab completion is a very important part of cheat.sh.
Having more than a thousand cheat sheets, it's very hard to learn all their names.

If you want to use the `cheat.sh` shell functions, it's enough to include `:bash` (`:zsh` or `:fish`)
in `~/.bashrc`:

```
    $ curl cheat.sh/:bash > ~/.bash.d/cheat.sh
    $ . ~/.bash.d/cheat.sh
    $ # add . ~/.bash.d/cheat.sh to ~/.bashrc
```

If you want to use cheat.sh with curl 
and don't create any special functions, include `:bash_completion`:

```
    $ curl cheat.sh/:bash_completion > ~/.bash.d/cheat.sh
    $ . ~/.bash.d/cheat.sh
    $ # add . ~/.bash.d/cheat.sh to ~/.bashrc
```

## Editors integration

### Emacs

* [cheat-sh.el](https://github.com/davep/cheat-sh.el) — Emacs support (available also at cheat.sh/:emacs)
* cheat.sh/:emacs-ivy — Emacs support for ivy users

[![asciicast](https://asciinema.org/a/123734.png)](https://asciinema.org/a/123734)

## Options

    ?OPTIONS

```
    q                  quiet mode, don't show github/twitter buttons
    T                  text only, no ANSI sequences (can be pasted in an editor)
    style=STYLE        color style
```

Options can be combined together in this way:

```
    $ curl cheat.sh/for?qT\&style=bw
```

(note the `\` before `&`: it is escaping `&`, which has in shell special meaning). 

## Programming languages cheat sheets

Cheat sheets related to programming languages
are organized in namespaces (subdirectories), that are named according
to the programming languages.

For each supported programming language
there are several special cheat sheets: its own sheet, `hello`, `:list` and `:learn`.
Say for lua it will look like:

```
    lua
    lua/hello
    lua/:list
    lua/:learn
```

Some languages has the one-liners-cheat sheet, `1line`:

```
    perl/1line
```
* `hello` describes how you can start with the language — install it if needed, build and run its programs, and it shows the "Hello world" program written in the language;
* `:list` shows all topics related to the language
* `:learn` shows a learn-x-in-minutes language cheat sheet perfect for getting started with the language.
* `1line` is a collection of one-liners in this language
* `weirdness` is a collection of examples of weird things in this language

![cheat.sh usage](http://cheat.sh/files/supported-languages.png)

At the moment, cheat.sh covers the 8 following programming languages (alphabetically sorted):

|Prefix     |Language  |Basics|One-liners|Weirdness|
|-----------|----------|------|----------|---------|
|`go/`      |Go        |✓     |          |         |
|`haskell/` |Haskell   |✓     |          |         |
|`js/`      |JavaScript|✓     |✓         |✓        |
|`lua/`     |Lua       |✓     |          |         |
|`ocaml/`   |OCaml     |✓     |          |         |
|`perl/`    |Perl      |✓     |✓         |         |
|`php/`     |PHP       |✓     |          |         |
|`python/`  |Python    |✓     |          |         |
|`rust/`    |Rust      |✓     |          |         |
|`scala/`   |Scala     |✓     |          |         |

## Cheat sheets sources

Instead of creating yet another mediocre cheat sheet repository,
we are concentrating our efforts on creation of a unified
mechanism to access selected existing well developed and good maintained
cheat sheet repositories covering topics of our interest:
programming and operating systems usage.

cheat.sh uses several community driven repositories
of cheat sheets
(in the popularity column number of contributors/number of stars are shown):

|Cheat sheets           |Repository                                            | Popularity | Creation Date |
|-----------------------|------------------------------------------------------|------------|---------------|
|UNIX/Linux, programming|[cheat.sheets](https://github.com/chubin/cheat.sheets)| 2/20       | May 1, 2017   |
|UNIX/Linux commands    |[tldr-pages/tldr](https://github.com/tldr-pages/tldr) | 336/9449   | Dec 8, 2013   |
|UNIX/Linux commands    |[chrisallenlane/cheat](https://github.com/chrisallenlane/cheat)|93/3231|Jul 28, 2013|
|Programming languages  |[adambard/learnxinyminutes-docs](https://github.com/adambard/learnxinyminutes-docs)|999/4513|Jun 23, 2013|
|Go                     |[a8m/go-lang-cheat-sheet](https://github.com/a8m/go-lang-cheat-sheet)|23/2086|Feb 9, 2014|
|Perl                   |[pkrumnis/perl1line.txt](https://github.com/pkrumins/perl1line.txt)|4/151|Nov 4, 2011|

Pie diagram reflecting cheat sheets sources distribution (by number of cheat sheets on cheat.sh originating from a repository):

![cheat.sh cheat sheets repositories](http://cheat.sh/files/stat-2017-06-05.png)

## How to conribute

### How to edit a cheat sheet

If you want to edit a cheat.sh cheat sheet, you should edit it in the upstream repository.
You will find the name of the source repository in a browser, when you open a cheat sheet.
There are two github buttons in the bottom of the page: the second one is the button
of the repository, whom belongs the current cheat sheet.

You can edit the cheat sheet directly in your browser (you need a github account for it).
There is a edit button in the top right corner. If you click on it, an editor will be open.
There you will change the cheat sheet (under the hood: the upstrem repository is forked, your changes are
commited in the forked repository, a pull request to the upstream repository owner is sent).

![cheat.sh cheat sheets repositories](http://cheat.sh/files/edit-cheat-sheet.png)

### How to add a cheat sheet

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

### How to add a cheat sheet repository

If you want to add a cheat sheet repository to cheat.sh, please open an issue:

* [Add a new repository](https://github.com/chubin/cheat.sh/issues/new)

Please specify the name of the repository, and give its short description.

