# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 19:30:14 2018

@author: Zhen
"""

import os
import string
import pandas as pd
from nltk.corpus import sentiwordnet as swn
from nltk.stem import WordNetLemmatizer as WML
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn

from Char import Char


def penn_to_wn(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None

tag_weight = {wn.ADJ: 2.0,
              wn.ADV: 1.5,
              wn.VERB: 1.0,
              wn.NOUN: 0.8}

def meaning_to_score(meaning):
    tagged = pos_tag(word_tokenize(meaning))
    synsets = []
    lemmatzr = WML()
    
    for token in tagged:
        wn_tag = penn_to_wn(token[1])
        if not wn_tag:
            continue    
        lemma = lemmatzr.lemmatize(token[0], pos=wn_tag)
        if wn.synsets(lemma, pos=wn_tag) == []:
            continue
        synsets.append((wn.synsets(lemma, pos=wn_tag)[0], wn_tag))
    
    scores = [(get_score(w.name()), tag_weight[tag]) \
                for w, tag in synsets]
    return average(scores)

def get_score(name):
#    print(name, swn.senti_synset(name).pos_score(),
#            swn.senti_synset(name).neg_score())
    return swn.senti_synset(name).pos_score() \
            - swn.senti_synset(name).neg_score()

def average(lst):
    if len(lst) == 0:
        return 0.0
    else:
        if type(lst[0]) == tuple:
            return sum([x[0]*x[1] for x in lst]) / float(sum([x[1] for x in lst]))
        return sum(lst) / float(len(lst))

def process_sound(s):
    if s == '':
        return s
    s = s.replace('u:','v')
    if s[-1].isdigit():
        s = s[:-1]
    return s


if __name__ == '__main__':
    NEED_CHECK = True
    root_path = os.path.dirname(os.getcwd())
    data_input_path = os.path.join(root_path, 'data', 'RawData')
    data_output_path = os.path.join(root_path, 'data', 'PrecookedData')
    df = pd.read_excel(os.path.join(data_input_path, 'ChineseWordFrequency.xls'))
    print(df.head())
    
    char_info = []
    alphaspace = string.ascii_letters + ' '
    for i in range(len(df)):
        line = df.loc[i]
        c = line.char
        cnt = line.cnt
        try:
            info = line.info.split(' ')
        except:
            continue
        sound = list(set([process_sound(s) for s in info[0].split('/')]))
        meaning = [''.join(filter(alphaspace.__contains__, s.strip())) \
                   for s in ' '.join(info[1:]).split('/')]
        char_info.append(Char(c, cnt, sound, meaning=meaning))
        
    with open(os.path.join(data_output_path, 'ChineseCharSentiment.csv'),
                           'w', encoding="utf8") as f:
        for c in char_info:
            sentiment = average([meaning_to_score(m) for m in c.get_meaning()])
            c.set_sentiment(sentiment)
            f.write(str(c) + '\n')
        
        
    if NEED_CHECK:
        with open(os.path.join(data_output_path, 'ChineseCharSentiment.csv'),
                               'r', encoding="utf8") as f:
            k = 0
            for line in f:
                if k < 100:                
                    print(line)
                k += 1
        
#    test = char_info[:20]
    
#    for c in test:
    #    if len(line[2]) > 1:
    #        print(line)
#        if c.char in ['傻', '疲']:
#            c.parse_sentiment()
#        c.parse_sentiment()
    
#    test.sort()
#    for c in test[:50]:
#        print(c)
#    print('\n\n*****\n\n')
#    for c in test[-50:]:
#        print(c)
    