#!/bin/bash

cat header.txt > sp-topo.txt
sed -e "s/	[0-9]*$//" code.txt >> sp-topo.txt
txt2mb sp-topo.txt sp-topo.mb
cp sp-topo.mb ~/.config/fcitx/table
fcitx -r 2> /dev/null
