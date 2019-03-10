#!/usr/bin/env python

import sys
import os

head = '''\
<title></title>
<pre>
'''

foot = '''
</pre>
'''


if __name__ == '__main__':
    if not sys.argv[1:]:
        sys.exit('usage: pnl2html.py <filename.pnl>')

    from panela import panela_colors

    with open(sys.argv[1], 'rb') as pnlfile:
        print(head)
        print("... TODO panela html render ...")
        print(foot)

