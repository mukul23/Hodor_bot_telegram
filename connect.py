#!/usr/bin/env python
import urllib
import json
import time

import authkeys

class Updates():
    def __init__(self):
        self.token = authkeys.token()
        self.offset = 0
        self.manager()

    def manager(self):
        updated_data = self.update()
        message_list = self.json_to_list(updated_data)


    def json_to_list(self, json_data):
        messages = len(json_data['result'])

        for msg in json_data['result']:
            self.offset = msg['update_id']
            chat_id = msg['message']['chat']['id']
            try:
                text = msg['message']['text']
                message = Hodor.randomMessage(text)
            except KeyError:
                message = "Hodor????"
            self.send_message(chat_id,message)
        self.offset = self.offset+1


    def send(self, chatid, message):
        encode_dictonary = {'chat_id': str(chatid), 'text'=message}
        encoded = urllib.urlencode(encode_dictonary)
        send_message_url = r"https://api.telegram.org/bot"+self.token+r"/sendMessage?"+encoded
        m = urllib.urlopen(send_message_url)
        m.close()


    def update(self):
        update_url  = r"https://api.telegram.org/bot"self.token+r"/getUpdates?offset="
        update_url = update_url + str(self.offset)
        r = urllib.urlopen(call_url)
        response = json.loads(r)
        return response
        
