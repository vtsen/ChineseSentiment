# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 20:58:44 2018

@author: Zhen
"""



class Char(object):
    def __init__(self, char, count, sound, meaning='', sentiment=None):
        self.char = char
        self.count = count
        self.sound = sound
        self.meaning = meaning
        self.sentiment = sentiment
        self.aux = []
        
    def get_meaning(self):
        return self.meaning
    
    def set_sentiment(self, s):
        self.sentiment = s

    def __str__(self):
        return '\t'.join(map(str,[self.char, self.count, self.sound, self.sentiment]))
    
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        if self.sentiment is None or other.sentiment is None:
            return False
        return self.sentiment < other.sentiment