# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 22:30:03 2018

@author: Zhen
"""
import os
import math
import matplotlib.font_manager as mfm
import matplotlib.pyplot as plt

from Char import Char

font_path = "D:\Coding\Python\Font\FZHTJW.ttf"
prop = mfm.FontProperties(fname=font_path)


if __name__ == '__main__':
    root_path = os.path.dirname(os.getcwd())
    data_path = os.path.join(root_path, 'data', 'PrecookedData')
    
    chars = dict()
    with open(os.path.join(data_path, 'ChineseCharSentiment.csv'),
                               'r', encoding="utf8") as f:
        for line in f:
            char, count, sound, sent = line.strip().split('\t')
            count = int(count)
            sent = float(sent)
            chars[char] = Char(char, count, sound, sentiment=sent)
    
    with open(os.path.join(data_path, 'ChineseCharSentimentFromWords.csv'),
                               'r', encoding="utf8") as f:
        for line in f:
            char, sent_from_words, confidence = line.strip().split('\t')
            sent_from_words = float(sent_from_words)
            confidence = float(confidence)
            if char in chars.keys():
                chars[char].aux = {'sent_from_words': sent_from_words,
                     'confidence': confidence}
                
    fig = plt.figure(figsize=(30,15))
    ax = fig.add_subplot(111)
    ax.set_xlim(left=-1, right=1)
    for char in chars:
        char_info = chars[char]
        if len(char_info.aux) > 0:
            fontsize=2*int(math.ceil(math.log(char_info.count)))
            ax.annotate(char_info.char, 
                        (char_info.aux['sent_from_words'],
                         char_info.aux['confidence']),
                         fontproperties=mfm.FontProperties(fname=font_path,
                                                           size=fontsize))
    plt.savefig('sent.png')