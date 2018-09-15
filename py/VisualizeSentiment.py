# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 20:56:20 2018

@author: Zhen
"""

fig = plt.figure(figsize=(30,15))
        ax = fig.add_subplot(111)
        ax.set_xlim(left=-1, right=1)
        for s in sent:
            ax.annotate(s[0], (s[1], s[2]), fontproperties=prop)
#                        fontsize=math.ceil(-10*math.log(max(0.0001,1-s[2]))))
        plt.savefig('sent.png')