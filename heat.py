#!/usr/bin/python -OOS
# coding=utf-8

import argparse
parser = argparse.ArgumentParser(
        description='Generate heat map for Chinese input method')
parser.add_argument('-c', '--code_file',
        help='file encoding Chinese characters',
        default='code.txt')
parser.add_argument('-t', '--text_file',
        help='use this text file to generate heat map',
        default='test.txt')
parser.add_argument('-b', '--show_bigram',
        help='show bigram table for the keys',
        action='store_true')
parser.add_argument('-p', '--phrase_length',
        help='allow phrases up to this length to be used',
        type=int, default=1)
parser.add_argument('-m', '--min_length',
        help='minimum code length',
        type=int, default=2)
args = parser.parse_args()

with open(args.code_file) as f:
    lines = f.readlines()

code_book = {}
for line in lines:
    line = line.strip()
    # Skip empty line or comment.
    if line == '' or line[0] == '#':
        continue
    # Skip a line that doesn't define a character.
    item = line.split()
    if len(item) < 2:
        continue
    if item[1] not in code_book or len(item[0]) < len(code_book[item[1]]):
        code_book[item[1]] = item[0]

with open('char_freq.txt') as f:
    lines = f.readlines()[:5000]

sum_freq = 0
sum_keys = 0
for line in lines:
    item = line.split()
    if item[0] in code_book.keys():
        char_freq = int(item[1])
        sum_freq += char_freq
        sum_keys += max(len(code_book[item[0]]), args.min_length) * char_freq
print '理论码长：%.2f' % (float(sum_keys) / sum_freq)

with open(args.text_file) as f:
    lines = f.readlines()

freq = {'.': 0, ',': 0, ';': 0, '/': 0}
bigram = {}
total_keys = 0
total_chars = 0
left_hand_keys = 'qwertasdfgzxcvb'
last_hand = 0  # 0=left, 1=right
last_key = ''
same_hand_count = 0
missing_chars = []
phrase_freq = {}
punctuations = ',.，。、·‘’“”—《》【】？！；（）－：　￣…．∶°±×'
alphanums = 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
alphanums += 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
alphanums += '１２３４５６７８９０'
for line in lines:
    chars = []
    for c in line.decode('utf-8', 'replace'):
        chars += [c.encode('utf-8')]

    i = 0
    while i < len(chars):
        c = chars[i]
        if ord(c[0]) < 128 or c in punctuations or c in alphanums:
            i += 1
            continue

        if not code_book.has_key(c):
            missing_chars += [c]
            i += 1
            continue

        max_phrase = chars[i : i + args.phrase_length]
        for j in range(len(max_phrase)):
            phrase_len = len(max_phrase) - j
            phrase = ''.join(max_phrase[:phrase_len])
            if not code_book.has_key(phrase):
                continue
            if len(phrase) > 3:  # byte length of unicode
                if phrase_freq.has_key(phrase):
                    phrase_freq[phrase] += 1
                else:
                    phrase_freq[phrase] = 1
            code = code_book[phrase]
            i += phrase_len
            total_chars += phrase_len
            break

        while len(code) < args.min_length:
            code += '_'

        for key in code:
            total_keys += 1
            if freq.has_key(key):
                freq[key] += 1
            else:
                freq[key] = 1
            combo = last_key, key
            if args.show_bigram:
                if bigram.has_key(combo):
                    bigram[combo] += 1
                else:
                    bigram[combo] = 1
            this_hand = 0 if key in left_hand_keys else 1
            if this_hand == last_hand:
                same_hand_count += 1
            last_hand = this_hand
            last_key = key

def show_freq(keys):
    for key in keys:
        f = freq[key] if key in freq.keys() else 0
        print '%c%4.1f ' % (key, f*100.0/total_keys),

def sum_freq(keys):
    sum = 0
    for key in keys:
        f = freq[key] if key in freq.keys() else 0
        sum += f
    return sum*100.0 / total_keys

if len(missing_chars) > 0:
    print '缺字：', ''.join(missing_chars)
for phrase in phrase_freq.keys():
    print phrase, phrase_freq[phrase]
print '字数: %d  按键: %d  每字按键: %.2f  同手连击: %.2f%%' % (
        total_chars, total_keys, float(total_keys)/total_chars,
        100.0*same_hand_count/total_keys)
print
show_freq('qwertyuiop')
print '   %4.1f=%4.1f+%4.1f' % (
        sum_freq('qwertyuiop'), sum_freq('qwert'), sum_freq('yuiop'))
show_freq('asdfghjkl;')
print '   %4.1f=%4.1f+%4.1f' % (
        sum_freq('asdfghjkl;'), sum_freq('asdfg'), sum_freq('hjkl;'))
show_freq('zxcvbnm,./')
print '   %4.1f=%4.1f+%4.1f' % (
        sum_freq('zxcvbnm,./'), sum_freq('zxcvb'), sum_freq('nm,./'))
print
print '%5.1f  %5.1f  %5.1f  %5.1f  %5.1f  %5.1f  %5.1f  %5.1f  %5.1f  %5.1f' % (
        sum_freq('qaz'),
        sum_freq('wsx'),
        sum_freq('edc'),
        sum_freq('rfvtgb'),
        sum_freq('qwertasdfgzxcvb'),
        sum_freq('yuiophjkl;nm,./'),
        sum_freq('yhnujm'),
        sum_freq('ik,'),
        sum_freq('ol.'),
        sum_freq('p;/'))

if args.show_bigram:
    keys = 'qwertasdfgzxcvbyuiophjkl;nm,./'
    print
    print '  %00',
    for k2 in keys:
        print '%5s' % k2,
    print
    for k1 in keys:
        print '%5s' % k1,
        for k2 in keys:
            combo = k1, k2
            count = bigram[combo] if bigram.has_key(combo) else 0
            percent = count*10000.0 / total_keys
            print '%5.1f' % percent,
        print

