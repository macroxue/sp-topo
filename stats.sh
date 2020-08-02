code_book=${1:-code.txt}

chinese_count=(〇 一 二 三 四 五 六 七 八 九 十)

# Summary
max_len=$(awk '{print length($1)}' $code_book | sort -un | tail -1)
printf "最大码长:$max_len "
for len in $(seq 1 $max_len); do
  count[$len]=$(egrep "^[a-z;,./]{$len}[[:space:]]" $code_book | wc -l)
  printf "${chinese_count[$len]}码:${count[$len]}字 "
done
dup_groups=$(grep -v '1$' $code_book | cut -f1,3 | uniq | wc -l)
dup_chars=$(grep -v '1$' $code_book | wc -l)
printf "重码:$dup_groups组$dup_chars字 "
for d in $(seq 2 20); do
  dup_groups=$(grep $d $code_book | cut -f1,3 | uniq | wc -l)
  if [[ $dup_groups -gt 0 ]]; then
    printf "$d重$dup_groups组 "
  fi
done
echo

# Per-key breakdown
keys="a b c d e f g h i j k l m n o p q r s t u v w x y z ; , . /"

show_header() {
  echo
  printf "           "
  for key in $keys; do
    printf "%3s " $key
  done
  echo " 累计"
}

declare -A row
declare -A column_sum

add_row() {
  row_sum=0
  for key in $keys; do
    count=${row[$key]}
    printf "%4d" $count
    row_sum=$((row_sum+count))
    column_sum[$key]=$((column_sum[$key]+count))
  done
  printf "%5d" $row_sum
  echo
}

clear_column_sum() {
  for key in $keys; do
    column_sum[$key]=0
  done
}

add_column_sum() {
  printf "    累计: "
  row_sum=0
  column_sum=$1
  for key in $keys; do
    printf "%4d" ${column_sum[$key]}
    row_sum=$((row_sum+${column_sum[$key]}))
  done
  printf "%5d" $row_sum
  echo
  clear_column_sum
}

show_header
for len in $(seq 1 $max_len); do
  printf "${chinese_count[$len]}码起始: "
  for key in $keys; do
    pattern=$key
    if [[ $key == '.' ]]; then pattern="\\$key"; fi
    count=$(egrep "^$pattern[a-z;,./]{$((len-1))}[[:space:]]" $code_book | wc -l)
    row[$key]=$count
  done
  add_row
done
add_column_sum

show_header
for len in $(seq 1 $max_len); do
  printf "编码${chinese_count[$len]}位: "
  for key in $keys; do
    pattern=$key
    if [[ $key == '.' ]]; then pattern="\\$key"; fi
    count=$(egrep "^[a-z;,./]{$((len-1))}$pattern" $code_book | wc -l)
    row[$key]=$count
  done
  add_row
done
add_column_sum

show_header
for pos in $(seq 1 $max_len); do
  printf "重码${chinese_count[$pos]}位: "
  for key in $keys; do
    pattern=$key
    if [[ $key == '.' ]]; then pattern="\\$key"; fi
    dup_count=$(grep -v '1$' $code_book | egrep "^.{$((pos-1))}$pattern" | wc -l)
    row[$key]=$dup_count
  done
  add_row
done
add_column_sum
