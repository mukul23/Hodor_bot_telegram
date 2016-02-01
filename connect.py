#!/usr/bin/env python
import urllib
import json
import time

import authkeys
import Hodor

class Updates():
    def __init__(self):
        self.token = authkeys.token()
        self.offset = ""
        self.manager()

    def manager(self):
        updated_data = self.update()
        message_list = self.json_to_list(updated_data)
        time.sleep(5)
        self.recurser()

    def recurser(self):
        self.manager()

    def json_to_list(self, json_data):
        messages = len(json_data['result'])

        for msg in json_data['result']:
            self.offset = msg['update_id']
            chat_id = msg['message']['chat']['id']
            try:
                text = msg['message']['text']
                print "{} : {}".format(self.offset, text)
                message = Hodor.randomMessage(text)
            except KeyError:
                message = "Hodor???????"
            self.send(chat_id,message)
        #hail marry
        if json_data['result']:
            self.offset = self.offset+1


    def send(self, chatid, message):
        encode_dictonary = {'chat_id': str(chatid), 'text':message}
        encoded = urllib.urlencode(encode_dictonary)
        send_message_url = r"https://api.telegram.org/bot"+self.token+r"/sendMessage?"+encoded
        m = urllib.urlopen(send_message_url)
        m.close()


    def update(self):
        update_url  = r"https://api.telegram.org/bot"+self.token+r"/getUpdates?offset="
        call_url = update_url + str(self.offset)
        r = urllib.urlopen(call_url)
        response = json.loads(r.read())
        return response


run = Updates()
