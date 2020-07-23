#!/bin/bash

dict=double_pinyin_ding_zi.dict.yaml

# 生成字典
cat << END > $dict
# Rime dictionary: double_pinyin_ding_zi
# encoding: utf-8
#
# 双拼拓扑形字典

---
name: double_pinyin_ding_zi
version: "0.1"
sort: by_weight
use_preset_vocabulary: true
max_phrase_length: 2
columns:
  - text
  - code
  - weight
...

b	b	1
p	p	1
m	m	1
f	f	1
d	d	1
t	t	1
l	l	1
n	n	1
g	g	1
k	k	1
h	h	1
j	j	1
q	q	1
x	x	1
r	r	1
z	z	1
c	c	1
s	s	1
y	y	1
w	w	1
END
sed -e "s/\(.*\)	\(.*\)	[1-9][0-9]*$/\2	\1/" code.txt | sed -e "s/  *//" | \
  sed -e "s/$/	100/" >> $dict

# 拷贝配置和字典
mkdir -p ~/.config/fcitx/rime
cp *.yaml ~/.config/fcitx/rime
