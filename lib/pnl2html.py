#!/usr/bin/env python

import sys
import os

head = '''\
<!doctype html>
<title>cheat.sh - pnl2html</title>
<style>
body {
  color: white;
  background-color: black;
}
</style>
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
    pnl.render_html()

    #pnl.apply_mask()
    #print(pnl.show())


    print(foot)

