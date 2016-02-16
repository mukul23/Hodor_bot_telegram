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
        while True:
            time.sleep(15) #Update interval
            updated_data = self.update() #Checking for new messages
            if not updated_data: #in case there's an IO error
                continue
            message_list = self.process_json(updated_data) #anatomy of the json response
            continue


    def process_json(self, json_data):
        messages = len(json_data['result']) #nubmer of new messages since the last update

        for msg in json_data['result']:  #going through each new message one at a time.
            self.offset = msg['update_id'] #keeping track of the update ID
            chat_id = msg['message']['chat']['id'] #chat ID the user (for the current update_id)
            try:
                '''Added try and chatch because
                 the following Keys will not be avilable if user sends a image/sticker/video etc
                 (Anything except text-messages)'''
                text = msg['message']['text']
                print "{} : {}".format(self.offset, text)
                message = Hodor.randomMessage(text) #getting a random `HODOR` message
            except KeyError:
                message = "Hodor???????"
            self.send(chat_id,message) #calling the send function to send the message to the cuurent chat_id and update_id
        #hail marry
        if json_data['result']: #Updating the offset for the next update query
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
        try:
            r = urllib.urlopen(call_url)
            response = json.loads(r.read())
        except IOError:
            time.sleep(2)
            print "Bypassing [IOError]"
            return []
        return response


run = Updates()

