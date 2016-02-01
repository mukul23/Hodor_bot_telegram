#!/usr/bin/env python

import random

def randomMessage(text):
    text_len = len(text.split())
    repeat = (random.randint(1,text_len)+random.randint(0,5))
    punctuation = punctuations()
    hodor = "hodor "*repeat
    msg = "Hodor "+hodor.strip()+punctuation
    return msg

def punctuations():
    letter = random.randint(0,300)
    repetation = random.randint(2,5)
    punc = ""
    if letter < 150:
        punc = '!'*repetation
    if letter > 150 and letter < 290:
        punc = '.'*repetation
    else:
        punc = '?'*(repetation-1)
    return punc
