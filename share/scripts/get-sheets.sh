#!/bin/sh

## this doesn't error check, if it breaks and destroys things I'm sorry

mkdir cheatsheets
cd cheatsheets
mkdir cheat tldr spool
git clone --recursive https://github.com/adambard/learnxinyminutes-docs
git clone --recursive https://github.com/chrisallenlane/cheat cheat-temp
mv cheat-temp/cheat/cheatsheets/* cheat
rm -rf cheat-temp
git clone --recursive http://github.com/tldr-pages/tldr tldr-temp
mv tldr-temp/pages/* tldr
rm -rf tldr-temp
git clone --recursive https://github.com/chubin/cheat.sheets.git
mv cheat.sheets/sheets .