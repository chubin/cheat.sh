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
    pnlfile = sys.argv[1]
    if not os.path.isfile(pnlfile):
        sys.exit("error: " + pnlfile + " does not exist")

    from panela.panela_colors import Template

    print(head)

    pnl = Template()
    pnl.read(pnlfile)
    pnl.parse()
    pnl.apply_mask()
    print(pnl.show())

    print(foot)

