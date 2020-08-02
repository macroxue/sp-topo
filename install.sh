#!/bin/bash

# 生成编码文本
cat << END > sp-topo.txt
;fcitx 版本 0x03 码表文件
键码=abcdefghijklmnopqrstuvwxyz;,./'
码长=6
规避字符=
拼音=@
拼音长度=12
[数据]
END
sed -e "s/	[0-9]*$//" code.txt >> sp-topo.txt

# 转换成码表格式
txt2mb sp-topo.txt sp-topo.mb

# 拷贝配置和码表
mkdir -p ~/.config/fcitx/table
cp sp-topo.conf sp-topo.mb ~/.config/fcitx/table

# 重启小企鹅
fcitx -r 2> /dev/null
