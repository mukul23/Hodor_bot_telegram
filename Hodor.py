#!/usr/bin/env python

import random

def randomMessage(text):
    text = text.split()
    repeat = (random.randint(1,50)/random.randint(1,5))-1
    hodor = "hodor "*repeat
    msg = "Hodor "+hodor.strip()+"."
    return msg
