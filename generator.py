import pickle
import sys
import random


finish = [u'.', u'!', u'?']

def weighted_pick(d):
    r = random.uniform(0, sum(d.itervalues()))
    s = 0.0
    for k, w in d.iteritems():
        s += w
        if r < s: return k
    return k


def generate_text(n, one, two, three, reverse_index, index):

    ret = reverse_index[weighted_pick(one)]
    while ret in finish:
        ret = reverse_index[weighted_pick(one)]
    nextprev = index[ret]
    prev = weighted_pick(two[nextprev])
    prevw = reverse_index[prev]
    while n > 0:
        if (nextprev, prev) in three:
             cur = weighted_pick(three[(nextprev, prev)])
        else :
            if prev in two:
                cur = weighted_pick(two[prev])
            else:
                cur = weighted_pick(one)
        curw = reverse_index[cur]
        ret = ret + ' ' + curw
        nextprev = prev
        prev = cur
        n -= 1
    return ret

def start_upper(text):
    for i in xrange(len(text)):
        if text[i] in finish:
            text = text[:i - 1] + text[i: i + 2] + text[i + 2].upper() + text[i+3:]
    return text[0].upper() + text[1:]

with open('oneword.pickle', 'rb') as handle:
    one = pickle.load(handle)
with open('twoword.pickle', 'rb') as handle:
    two = pickle.load(handle)
with open('threeword.pickle', 'rb') as handle:
    three = pickle.load(handle)
with open('index.pickle', 'rb') as handle:
    index = pickle.load(handle)

"""
one = {1: 1, 2: 1, 3: 1, 4: 1}
two = {2: {1: 1}, 1: {3: 1}, 3: {4: 1}}
three = {(2,1): {3: 1}, (1, 3): {4: 1}}
index = {u'the': 1, u'close': 2, u'door': 3, u'now': 4}
#"""

reverse_index = dict((v, k) for k, v in index.items())
print start_upper(generate_text(int(sys.argv[1]), one, two, three, reverse_index, index))
