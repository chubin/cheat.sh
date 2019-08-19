 唯一のチートシート https://cheat.sh/ が必要です

世界の最高のコミュニティ駆動チートシートリポジトリへの統一されたアクセス。

理想的なチートシートのようなものがあるとすぐに想像してみましょう。 どのように見える？ どのような機能が必要ですか？

    簡潔に – 簡潔にする必要があります。 それはあなたが必要とするものだけを含んでいなければなりません。
    速く – それを即座に使用することが可能でなければなりません。
    包括的 – あなたが持つ可能性があるすべての質問に対する回答を含める必要があります。
    普遍的な – 準備ができていなくても、必要に応じてどこでもすぐに利用できるはずです。
    邪魔になりません – あなたの主な仕事からあなたをそらすことはありません。
    先入観 – それはあなたがその科目を学ぶのに役立ちます。
    目立たない – 完全に気付かれないで使用することが可能でなければならない。

そんなことは存在しない。
特徴

チート.sh

    単純なカール/ブラウザインターフェイスを備えています。
    55のプログラミング言語、いくつかのDBMS、および1000以上の最も重要なUNIX / Linuxコマンドをカバーしています。
    世界で最も優れたコミュニティ主導のチートシートリポジトリへのアクセスと、StackOverflowへのアクセスを提供します。
    あらゆる場所で利用でき、インストールは必要ありません。
    ultrafastは、原則として100ミリ秒以内に回答を返します。
    便利で便利なコマンドラインクライアントcht.shがありますが、これは必須ではありません。
    ブラウザを開いて精神的なコンテキストを切り替えることなく、コードエディタから直接使用することができます。
    特殊モード（ステルスモード）をサポートしています。このモードでは、鍵に触れたり、音を出させたりすることなく、完全に目に見えない状態で使用できます。

使用法

コマンドラインからUNIX / Linuxコマンドのチートシートを取得するには、 curlまたは他のHTTP / HTTPSクライアントを使用して、クエリのコマンド名を指定してサービスをクエリします。

```
    curl cheat.sh/tar
    curl cht.sh/curl
    curl https://cheat.sh/rsync
    curl https://cht.sh/tr
```

ご覧のとおり、HTTPSとHTTPの両方を使用してサービスにアクセスし、長い（cheat.sh）サービス名と短い（cht.sh）サービス名の両方にアクセスできます。

ここで、 tar 、 curl 、 rsync 、 trはUNIX / Linuxコマンドの名前です。あなたはチートシートを入手したいと思っています。

必要なコマンドの名前がわからない場合は、 ~KEYWORD記法を使用して検索することができます。 たとえば、ファイルシステム/ボリューム/その他のsnapshotsを作成する方法を知るには：

```
    curl cht.sh/~snapshot
```

プログラミング言語チートシートは、ルート名前空間には直接配置されず、専用の特別な名前空間に配置されます。

```
    curl cht.sh/go/Pointers
    curl cht.sh/scala/Functions
    curl cht.sh/python/lambda
```

利用可能なプログラミング言語チートシートのリストを取得するには、特別なクエリを実行します。list：

```
    curl cht.sh/go/:list
```

（ほぼ）それぞれのプログラミング言語には、 :learnという名前の特別なページがあります。これは、言語の基礎を説明しています（ 「Learn X in Y」プロジェクトからの直接マッピングです）。 あなたが言語を学び始めたばかりの方は、良い出発点になるかもしれません。

いくつかのプログラミング言語のクエリ用のチートシートがない場合（ほとんどの場合そうです）、利用可能なチートシートとStackOverflowでの回答に基づいてオンザフライで生成されます。 もちろん、返されたチートシートが100％ヒットしたという保証はありませんが、ほとんど常にあなたが探しているものです。

これらの（そしてあなた自身の）クエリを試して、その印象をどのように見えるかを見てみましょう：

```
    curl cht.sh/go/reverse+a+list
    curl cht.sh/python/random+list+elements
    curl cht.sh/js/parse+json
    curl cht.sh/lua/merge+tables
    curl cht.sh/clojure/variadic+function
```

いくつかのクエリの答えが気に入らない場合は、別のパラメータを選択することができます：追加のパラメータ/1 、 /2などをつけてクエリを繰り返します：

```
    curl cht.sh/python/random+string
    curl cht.sh/python/random+string/1
    curl cht.sh/python/random+string/2
```

チートシートは照会されたプログラミング言語のコードとしてフォーマットされています（少なくともこれを行うために最善を尽くしています）。この言語のプログラムに直接貼り付けることができます。 テキストコメントがある場合は、言語構文に従って書式設定されます。

```
    $ curl cht.sh/lua/table+keys
    -- lua: retrieve list of keys in a table

    local keyset={}
    local n=0

    for k,v in pairs(tab) do
      n=n+1
      keyset[n]=k
    end

    --[[
       [ Note that you cannot guarantee any order in keyset. If you want the
       [ keys in sorted order, then sort keyset with table.sort(keyset).
       [ 
       [ [lhf] [so/q/12674345] [cc by-sa 3.0]
       ]]
```

答えにテキストコメントが必要ない場合は、特別なオプションを使用してコメントを削除できます?Q ：

```
    $ curl cht.sh/lua/table+keys?Q
    local keyset={}
    local n=0

    for k,v in pairs(tab) do
      n=n+1
      keyset[n]=k
    end
```

構文強調表示が必要ない場合は、 ?Tを使ってスイッチをオフにし?T 。 オプションを一緒に組み合わせることができます：

```
    curl cht.sh/go/reverse+a+list?Q
    curl cht.sh/python/random+list+elements?Q
    curl cht.sh/js/parse+json?Q
    curl cht.sh/lua/merge+tables?QT
    curl cht.sh/clojure/variadic+function?QT
```

下記および/:help記載されているすべてのオプションの完全なリスト

あなた自身の質問をお試しください。 次のルールに従ってください。

    より具体的になるようにしてください（ /python/append+fileは/python/fileや/python/appendよりも優れてい/python/append ）。
    可能であれば実践的な質問をする（しかし理論的な質問も可能である）。
    プログラミング言語に関する質問のみを行います。 セクション名としてプログラミング言語の名前を指定します。
    空白ではなく+区切ります。
    とにかく無視される特殊文字は使用しないでください。

以下のプログラミング言語のクエリについての詳細を読む。
コマンドラインクライアント、cht.sh

cheat.shサービスには独自のコマンドラインクライアント（ cht.sh ）があり、 curlを使ってサービスを直接照会するのに比べ、いくつかの便利な機能があります。

    永続的なクエリコンテキストとreadlineサポートを備えた特別なシェルモード。
    クエリの履歴。
    クリップボードの統合。
    シェルのタブ補完のサポート（bash、fish、zsh）;
    ステルスモード。

クライアントをインストールするには：

```
    curl https://cht.sh/:cht.sh > ~/bin/cht.sh
    chmod +x ~/bin/cht.sh
```

さて、あなたはcurl代わりにcht.shを使い、より自然な方法であなたのクエリを+代わりにスペースで書くことができます：

```
    $ cht.sh go reverse a list
    $ cht.sh python random list elements
    $ cht.sh js parse json
```

特別なシェルモードでクライアントを起動する方がさらに便利です：

```
    $ cht.sh --shell
    cht.sh> go reverse a list
```

すべてのクエリがほぼ同じ言語であると想定されている場合は、クエリのコンテキストを変更して、プログラミング言語の名前を繰り返すことができます。

```
    $ cht.sh --shell
    cht.sh> cd go
    cht.sh/go> reverse a list
```

このコンテキストでクライアントを起動することさえできます：

```
    $ cht.sh --shell go
    cht.sh/go> reverse a list
    ...
    cht.sh/go> join a list
    ...
```

コンテキストを変更したい場合は、 cdコマンドで行うことができます。あるいは、他の言語のクエリを1つだけ実行する場合は、 /ください：

```
    $ cht.sh --shell go
    ...
    cht.sh/go> /python dictionary comprehension
    ...
```

最後の回答をクリップボードにcopyする場合は、 c （ copy ）コマンドまたはC （コメントなしのccopy ）コマンドを使用できます。

```
    cht.sh/python> append file
    #  python - How do you append to a file?

    with open("test.txt", "a") as myfile:
        myfile.write("appended text")
    cht.sh/python> C
    copy: 2 lines copied to the selection
```

他の内部cht.shコマンドのhelpを入力してください。

```
	cht.sh> help
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
```

cht.shクライアントの設定ファイルは~/.cht.sh/cht.sh.confます。 これを使用して、各クエリで使用するクエリオプションを指定します。 たとえば、構文の強調表示をオフに切り替えるには、次の内容のファイルを作成します。

```
QUERY_OPTIONS="T"
```

または、特殊な構文強調表示テーマを使用する場合は、次のようにします。

```
QUERY_OPTIONS="style=native"
```

（ curl cht.sh/:styles-demoサポートされているすべてのスタイルが表示されます）。
タブ補完

cht.shタブ補完のサポートをcht.shにするには、 ~/.bashrc ： :bash_completionスクリプトを追加してください：

    $ curl https://cheat.sh/:bash_completion > ~/.bash.d/cht.sh
    $ . ~/.bash.d/cht.sh
    $ # and add . ~/.bash.d/cht.sh to ~/.bashrc

ステルスモード

実際のチートシートの重要な特性の1つは、それが完全に気付かれずに使用できるということです。

cheat.shはまったく気付かれずに使えます。 cheat.shクライアント、 cht.shには、 ステルスモードと呼ばれる特別なモードがあります。これは、キーボードに触れてチートシートを開く必要がないことを利用しています。

このモードでは、マウスでテキストを選択すると（そしてX Window Systemの選択バッファやクリップボードに追加されるとすぐに）、それはcheat.shのクエリ文字列として使用され、特派員のチートシートは自動的に表示されます。

インタビュー担当者が共有文書（Google Docsなど）を使っていくつかの質問をし、そこにコーディング回答を書くことになっているオンラインインタビューをしていることを想像してみましょう。面接官にあなたがそれを正しく聞いたことを示すために）

ステルスモードのcht.shを使用しているときは、何らかの質問のためにチートシートを見るために必要なのは、マウスを使って質問を選択することだけです。 答えにテキストを入れたくない場合は、コードだけが必要です。ステルスモードを開始するときには、 Qオプションを使用してください。

```
You: Hi!                                            | $ cht.sh --shell python
She: Hi!                                            | cht.sh/python> stealth Q
She: Are you ready for a small interview?           | stealth: you are in the stealth mode; select any text
She: Just a couple of questions                     | stealth: selections longer than 5 words are ignored
She: We will talk about python                      | stealth: query arguments: ?Q
She: Let's start from something simple.             | stealth: use ^C to leave this mode
She: Do you know how to reverse a list in python?   |
You: Sure                                           |
You: (selecting "reverse a list")                   | stealth: reverse a list
                                                    | reverse_lst = lst[::-1]
You: lst[::-1]?                                     |
She: Good.                                          |
She: Do you know how to chain a list of lists?      |
You: (selecting "chain a list of lists")            | stealth: chain a list of lists
                                                    | import itertools
                                                    | a = [["a","b"], ["c"]]
                                                    | print list(itertools.chain.from_iterable(a))
You: May I use external modules?                    |
She: What module do you want to use?                |
You: itertools                                      |
She: Yes, you may use it                            |
You: Ok, then:                                      |
You: itertools.chain.from_iterable(a)               |
She: Good. Let's try something harder.              |
She: What about quicksort implementation?           |
You: (selecting "quicksort implementation")         | stealth: quicksort implementation
You: Let me think about it.                         | (some big and clumsy lowlevel implementation shown)
You: Well...(starting typing it in)                 | def sort(array=[12,4,5,6,7,3,1,15]):
                                                    |     less = []
She: (seeing your ugly pascal style)                |     equal = []
She: Could you write it more concise?               |     greater = []
                                                    |     if len(array) > 1:
You: What do you mean?                              |         pivot = array[0]
                                                    |         for x in array:
She: I mean,                                        |             if x < pivot: less.append(x)
She: do you really need all these ifs and fors?     |             if x == pivot: equal.append(x)
She: Could you may be just use filter instead?      |             if x > pivot: greater.append(x)
                                                    |         return sort(less)+equal+sort(greater)
You: quicksort with filter?                         |     else:
                                                    |         return array
She: Yes                                            |
You: (selecting "quicksort with filter")            | stealth: quicksort with filter
You: Ok, I will try.                                | return qsort(filter(lt, L[1:]))+[pivot] \
You: Something like this?                           |     +qsort(filter(ge, L[1:]))
You: qsort(filter(lt, L[1:]))+[pivot] \             |
       + qsort(filter(ge, L[1:]))                   |
                                                    |
She: Yes! Perfect! Exactly what I wanted to see!    |
                                                    |
```

もちろん、それはちょうど楽しいことです。あなたが行ったときに何が起こるかを知っているので、コーディングのインタビューで決して欺くべきではありません。

エディターの統合

エディタから直接cheat.shを使うことができます（ VimとEmacsは現在サポートされています）。 あなたのブラウザを開き、グーグルで、スタックオーバーフローをブラウズし、最終的に必要なコードスニペットをクリップボードにコピーして後でエディタに貼り付けるのではなく、エディタを離れずに同じことを達成することができます。

これはVimのように見えます：

    プログラムの編集中に質問がある場合は、バッファに直接質問を入力して<leader>KKを押してください。 ポケットベルであなたの質問に対する答えが得られます。 （ <leader>KBすると、別のバッファで回答が得られます）。

    答えが気に入ったらバッファやページャから手作業で貼り付けてください。怠け者の場合は<leader>KPを使って質問の下/下に貼り付けることができます。 コメントなしで回答が必要な場合は、 <leader>KCが最後のクエリを再生してそれらを切り替えます。

シンセシス （Vim用）などの静的解析プラグインを使用している場合は、警告とエラーメッセージをcheat.shクエリとして使用できます：カーソルを問題の行に置き、 <leader>KE ：警告の説明を開きます新しいバッファに入れます。
ヴィム

    cheat.sh-vim – Vimのサポート

ここにVimの設定例を示します：

```
" some configuration above ...

let mapleader=" "

call vundle#begin()
Bundle 'gmarik/vundle'
Bundle 'scrooloose/syntastic'
Bundle 'dbeniamine/cheat.sh-vim'
call vundle#end()

let g:syntastic_javascript_checkers = [ 'jshint' ]
let g:syntastic_ocaml_checkers = ['merlin']
let g:syntastic_python_checkers = ['pylint']
let g:syntastic_shell_checkers = ['shellcheck']

" some configuration below ...
```

この例では、いくつかのVimプラグインが使用されています：

    gmarik / vundle – Vimプラグインマネージャ
    scrooloose / syntastic – 構文チェックプラグイン
    cheat.sh-vim – Vimのサポート

Syntasticは警告とエラー（code analysysツールで見つかった： jshint 、 jshint 、 pylint 、 shellcheckt etc.), and cheat.sh-vim`を表示すると、エディタに書き込まれたプログラミング言語のクエリに関するエラーと警告と回答の説明が表示されます。

cheat.sh Vimプラグインの最も重要な機能が表示されているデモをご覧ください（5分）：

または、スクロールしたり一時停止したりする場合は、YouTubeでも同じです：

Emacs

    cheat-sh.el – Emacsのサポート（cheat.sh/：emacsでも利用可能）
    cheat.sh/：emacs-ivy – ivyユーザーのEmacsサポート

特別ページ

いくつかの特別なページがあり（その名前は常にコロンで始まります）、チートシートではなく特別な意味を持っています。

入門：

```
    :help               description of all special pages and options
    :intro              cheat.sh introduction, covering the most important usage questions
    :list               list all cheat sheets (can be used in a subsection too: /go/:list)
```

コマンドライン・クライアントcht.shとシェルは次のものをサポートしています。

```
    :cht.sh             code of the cht.sh client
    :bash_completion    bash function for tab completion
    :bash               bash function and tab completion setup
    :fish               fish function and tab completion setup
    :zsh                zsh function and tab completion setup
```

エディターのサポート：

    :vim                cheat.sh support for Vim
    :emacs              cheat.sh function for Emacs
    :emacs-ivy          cheat.sh function for Emacs (uses ivy)

その他のページ：

```
    :post               how to post new cheat sheet
    :styles             list of color styles
    :styles-demo        show color styles usage examples
```

サーチ

キーワードを検索するには、次のクエリを使用します。

```
    /~keyword
```

この場合、検索は再帰的ではなく、指定されたレベルのページでのみ実行されます。 例えば：

```
    /~snapshot          look for snapshot in the first level cheat sheets
    /scala/~currying     look for currying in scala cheat sheets
```

すべてのチートシートで再帰的検索を行うには、二重スラッシュを使用します。

    /~snapshot/r         look for snapshot in all cheat sheets

スラッシュの後に特殊な検索オプションを使用することができます。

    /~shot/bi           case insensitive (i), word boundaries (b)

検索オプションのリスト：

```
    i   case insensitive search
    b   word boundaries
    r   recursive search
```

プログラミング言語チートシート

プログラミング言語に関連するチートシートは、プログラミング言語に従って名前が付けられた名前空間（サブディレクトリ）に編成されています。

サポートされているプログラミング言語ごとに、独自のsheet、 hello 、 :list 、 :learnいくつかの特別なチートシートがあり:learn 。 それはルアのように見えます：

```
    lua
    lua/hello
    lua/:list
    lua/:learn
```

いくつかの言語には、1行のチートシート、1 1line ：

    perl/1line

    helloは、あなたがどのように言語を使い始めることができるかを記述します – 必要に応じてインストールし、プログラムをビルドして実行し、言語で書かれた “Hello world”プログラムを表示します。
    :listには言語に関連するすべてのトピックが表示されます
    :learnは、言語を使い始めるのに最適なx-in-minutes言語のチートシートを表示します。
    1lineはこの言語の1ライナーの集合です
    weirdnessなことはこの言語の奇妙なものの例の集まりです

現時点では、cheat.shは以下の55のプログラミング言語（アルファベット順にソートされています）をカバーしています：
接頭辞 	言語 	基本 	ワンライナー 	奇妙さ 	スタックオーバーフロー
arduino/ 	Arduino 				✓
assembly/ 	アセンブリ 				✓
awk/ 	AWK 	✓ 			✓
bash/ 	バッシュ 	✓ 			✓
basic/ 	ベーシック 				✓
bf/ 	頭痛 	✓ 			✓
c/ 	C 	✓ 			✓
chapel/ 	チャペル 	✓ 			✓
clean/ 	クリーン 				✓
clojure/ 	Clojure 	✓ 			✓
coffee/ 	CoffeeScript 	✓ 			✓
cpp/ 	C ++ 	✓ 			✓
csharp/ 	C＃ 	✓ 			✓
d/ 	D 	✓ 			✓
dart/ 	ダーツ 	✓ 			✓
delphi/ 	デフ 				✓
dylan/ 	ディラン 	✓ 			✓
eiffel/ 	エッフェル 				✓
elixir/ 	エリクシール 	✓ 			✓
elisp/ 	ELisp 	✓ 			✓
elm/ 	エルム 	✓ 			✓
erlang/ 	アーラン 	✓ 			✓
factor/ 	因子 	✓ 			✓
fortran/ 	Fortran 	✓ 			✓
forth/ 	四方 	✓ 			✓
fsharp/ 	F＃ 	✓ 			✓
go/ 	行こう 	✓ 			✓
groovy/ 	Groovy 	✓ 			✓
haskell/ 	ハスケル 	✓ 			✓
java/ 	Java 	✓ 			✓
js/ 	JavaScript 	✓ 	✓ 	✓ 	✓
julia/ 	ジュリア 	✓ 			✓
kotlin/ 	コトリン 	✓ 			✓
lisp/ 	Lisp 	✓ 			✓
lua/ 	ルア 	✓ 			✓
matlab/ 	MATLAB 	✓ 			✓
ocaml/ 	OCaml 	✓ 			✓
perl/ 	Perl 	✓ 	✓ 		✓
perl6/ 	Perl 6 	✓ 	✓ 		✓
php/ 	PHP 	✓ 			✓
pike/ 	パイク 				✓
python/ 	Python 	✓ 			✓
python3/ 	Python 3 	✓ 			✓
r/ 	R 	✓ 			✓
racket/ 	ラケット 	✓ 			✓
ruby/ 	ルビー 	✓ 			✓
rust/ 	錆 	✓ 			✓
scala/ 	スカラ 	✓ 			✓
scheme/ 	スキーム 	✓ 			✓
swift/ 	迅速 	✓ 			✓
tcsh/ 	Tcsh 	✓ 			✓
tcl/ 	Tcl 	✓ 			✓
objective-c/ 	目標-C 	✓ 			✓
vb/ 	VisualBasic 	✓ 			✓
vbnet/ 	VB.Net 	✓ 			✓
チートシートのソース

さらに別の平凡なチートシートリポジトリを作成するのではなく、既存のよく開発されたよく管理されたチートシートリポジトリにアクセスする統一メカニズムの作成に力を注いでいます。

cheat.shは世界中の何千ものユーザー、開発者、作者によって管理されている選択されたコミュニティ駆動のチートシートリポジトリと情報ソースを使用します（貢献者のユーザー列数/星数が表示されます）。
カンニングペーパー 	リポジトリ 	ユーザー 	作成日
UNIX / Linux、プログラミング 	カンニングペーパー 	6/54 	2017年5月1日
UNIX / Linuxコマンド 	tldr-pages / tldr 	541/17360 	2013年12月8日
UNIX / Linuxコマンド 	クリサンレン/チート 	105/4193 	2013年7月28日
プログラミング言語 	adambard / learnxinyminutes-docs 	1096/5285 	2013年6月23日
行こう 	a8m / go-lang-cheat-sheet 	29/3034 	2014年2月9日
Perl 	pkrumnis / perl1line.txt 	4/165 	2011年11月4日
プログラミング言語 	スタックオーバーフロー 	9M 	2008年9月15日

チートシートソースの分布を反映するパイダイアグラム（リポジトリから生成されたチート.shのチートシートの数による）：

貢献する方法
チートシートの編集方法

cheat.shチートシートを編集する場合は、アップストリームレポジトリで編集する必要があります。 チートシートを開くと、ブラウザにソースリポジトリの名前が表示されます。 ページ下部に2つのgithubボタンがあります：2番目のボタンは、現在のチートシートに属するリポジトリのボタンです。

チートシートをブラウザで直接編集できます（githubアカウントが必要です）。 右上に編集ボタンがあります。 それをクリックすると、エディタが開きます。 そこではチートシートを変更します（ボンネットの下：アップストレームリポジトリはフォークされ、変更はフォークされたリポジトリでコミットされ、上流のリポジトリ所有者へのプルリクエストが送信されます）。

チートシートを追加する方法

チートシートを追加する場合は、次のいずれかの方法があります。

    それを外部のチートシートレポジトリの1つに追加します。 自分のチートシートに最適なリポジトリが何であるかを決める必要があります。
    github（fork、commit、pull request）のローカルcheat.shリポジトリ（ cheat.sheets ）に追加します。
    curlやウェブブラウザ（ cheat.sh/：post ）を使ってcheat.shに投稿してください。

既存のチートシートを変更したい場合は、元のリポジトリを見つける必要があります（ブラウザでチートシートを開くと、チートシートの下部にリポジトリのgithubボタンが表示されます）、チートシートは、それを変更してください。 しばらくすると、変更はcheat.shで同期されます。
チートシートリポジトリを追加する方法

cheat.shにチートシートリポジトリを追加する場合は、問題を開いてください：

    新しいリポジトリを追加する

リポジトリの名前を指定し、簡単な説明をしてください。

