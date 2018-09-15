# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 12:19:41 2018

@author: Zhen
"""

import os
import math

def count_char(filename):
    freq_dict = dict()    
    with open(filename, 'r', encoding="utf8") as file:
        for line in file:
            k = len(line) - 1
            for c in line[:-1]:
                if c not in freq_dict.keys():
                    freq_dict[c] = 1/k
                else:
                    freq_dict[c] += 1/k
        
    freq_tuple_list = [(k, v) for k,v in freq_dict.items()]
    freq_tuple_list = sorted(freq_tuple_list, key=lambda x: -x[1])
    print(filename)
    print(freq_tuple_list[:50])
    return freq_dict


if __name__ == '__main__':
    NEED_CHECK = False
    DAMP = 0.2
    
    root_path = os.path.dirname(os.getcwd())
    data_input_path = os.path.join(root_path, 'data', 'RawData')
    data_output_path = os.path.join(root_path, 'data', 'PrecookedData')
    
    pos = count_char(os.path.join(data_input_path, 'positive_submit.txt'))
    neg = count_char(os.path.join(data_input_path, 'negative_submit.txt'))
    
    def get_sentiment(c):
        if c not in pos.keys():
            return -1
        if c not in neg.keys():
            return 1
        return (pos[c] - neg[c]) / (pos[c] + neg[c])
    
    def get_weight(c):
        pc = 0 if c not in pos.keys() else pos[c]
        nc = 0 if c not in neg.keys() else neg[c]
        return 1 - math.exp(-DAMP * (pc + nc))
    
    chars = {x[0] for x in pos.keys()}.union({x[0] for x in neg.keys()})
    sent = [(c, get_sentiment(c), get_weight(c)) for c in chars]
    sent = sorted(sent, key=lambda x: x[1]*x[2])
    sent_dict = {x[0]: x[1] for x in sent}
    
    with open(os.path.join(data_output_path, 'ChineseCharSentimentFromWords.csv'),
                           'w', encoding="utf8") as f:
        for s in sent:
            f.write('\t'.join(map(str, s)) + '\n')
        
    
    if NEED_CHECK:    
        print(sent[:100])
        print(sent[-100:])
        print(len(sent))

        