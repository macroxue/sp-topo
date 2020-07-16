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
...

END
sed -e "s/\(.*\)	\(.*\)	[1-9][0-9]*$/\2	\1/" code.txt | sed -e "s/  *//" >> $dict

# 拷贝配置和字典
mkdir -p ~/.config/fcitx/rime
cp *.yaml ~/.config/fcitx/rime
