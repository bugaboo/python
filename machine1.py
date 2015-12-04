#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import pickle

def parse(folder):
    oneword = {1: 1, 2: 1, 3: 1}
    twoword = {2: {1: 1}, 1: {3: 1}}
    threeword = {2: {(1, 3): 1}}
    index = {u'the': 1, u'close': 2, u'door': 3}
    book = open('1.txt')
#    get_counts(cleantext(book.read().decode('utf8')), oneword, twoword, threeword, index)
    for k, v in twoword.iteritems():
        print k, v
    count = 0
    for root, subdirs, files in os.walk(folder):
        for f in files:
            with open(root + '/' + f) as book:
                print count 
                get_counts(cleantext(book.read().decode('utf8')), oneword, twoword, threeword, index)
                count += 1
    return oneword, twoword, threeword, index
        

def get_counts(text, oneword, twoword, threeword, index):
    nextprev = 1
    index[u'beginning'] = 4
    prev = 4
    for current in text.split():
        if current not in index:
            new_index = max(index.values()) + 1
            index[current] = new_index
        cur_index = index[current]
        if cur_index in oneword:
            oneword[cur_index] += 1
        else:
            oneword[cur_index] = 1
        if prev in twoword:
            if cur_index in twoword[prev]:
                twoword[prev][cur_index] += 1
            else:
                twoword[prev][cur_index] = 1
        else:
            twoword[prev] = {cur_index: 1}
        if nextprev in threeword:
            if (prev, cur_index) in threeword[nextprev]:
                threeword[nextprev][(prev, cur_index)] += 1
            else:
                threeword[nextprev][(prev, cur_index)] = 1
        else:
            threeword[nextprev] = {(prev, cur_index): 1}
        nextprev = prev
        prev = cur_index
        

def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in rep_dict.keys()]), re.M)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)

def cleantext(text):
    text = text.lower().replace(u'’', '\'').replace(u'…', '.').replace('it\'s', 'it is').replace('that\'s', 'that is').replace('there\'s', 'there is')
    text = text.replace('he\'s', 'he is').replace('she\'s', 'she is').replace('let\'s', 'let us').replace('what\'s', 'what is').replace('how\'s', 'how is')
    text = text.replace('where\'s', 'where is').replace('when\'s', 'when is').replace('now\'s', 'now is')
    rules = dict([('!!!', ' !'), ('?!', '?'), ('???', '?'), ('...', '.'), ('.!', '!'), ('.?', '?'), 
    ('?.', '?'), ('!.', '!'), ('.', ' .'), ('!', ' !'), ('?', ' ?'), ('n\'t', ' not'), ('\'s', ''), ('\'re', ' are'), ('\'ve', ' have'),
    ('ain\'t', 'are not'), ('\'d', ' would'), ('\'ll', ' will'), ('i\'m', 'i am'), ('in\'', 'ing')])
    return re.sub('[^a-z0-9\.\?!\s]', '', multiple_replace(text, rules))

class TextGenerator():
    def __init__(self):
        self.words = parse("corpus")



one, two, three, index = parse('corpus')
with open('oneword.pickle', 'wb') as handle:
    pickle.dump(one, handle)
with open('twoword.pickle', 'wb') as handle:
    pickle.dump(two, handle)
with open('threeword.pickle', 'wb') as handle:
    pickle.dump(three, handle)
with open('index.pickle', 'wb') as handle:
    pickle.dump(index, handle)

if (len(sys.argv) > 1):
    f = open(sys.argv[1])
    print cleantext(f.read().decode('utf8'))
