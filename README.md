<h1>Getting started with Telegram's bot API in python</h1>
<p>This is a short python program which will get you up and running with telegram API in under 100 lines of code. 
Obviously this will be a very basic example but instead of <i>"Hello World!"</i>,  it will feature our beloved <b><a href="http://gameofthrones.wikia.com/wiki/Hodor">Hodor</a></b> (with thanks and/or apologies to George R.R. Martin)
<p>For glossing over simplicity the source code is independent of external libraries and utilises the generic libraries that comes with python (altough it is recommended that you use <a href="http://docs.python-requests.org/en/master/">requests library</a> instead of urllib)</p>
<p>Getting started is as easy as <a href="https://core.telegram.org/bots#botfather">creating your bot</a><br/>Just add the <strong>authrorization token</strong> you got from <i>BotFather</i> to <b>authkey.py</b> and you're good to go.</p>
But don't let the name decive you... Though the bot example here is basic you can do a lot of cool stuff with it, including and espically IoT stuff and what not, you're only limited by your imagination.
(How cool it would be controling your <a href='https://s-media-cache-ak0.pinimg.com/originals/4d/32/f1/4d32f142871c29466f303c2c80f24ed4.gif'>raspberry pi with telegram</a>)

![alt acess token for your bot] (http://i.imgur.com/EYYvHC1.png)<br/>
Add the token you recived for your bot (as shown above) to <b>authkey.py</b>
````python
def token():
  return "160809321:AAGjlbgkq2elXWgSqdSBd4swA5bL8VoYM50" #replace this with your bot's token.
````
PS: I'll save the trouble for the deamon at the back of your head; the authrisation token is expired.


<h2>How it works</h2>
The program consists of just 4 methods.
 - Manager
 - process_json
 - send
 - update

<p><i>Update</i> function connects with Telegram's server for update every 15 seconds (by calling telegram's <a href="https://core.telegram.org/bots/api#getupdates">getUpdates</a> method)

````python
def update(self):
  update_url  = r"https://api.telegram.org/bot"+self.token+r"/getUpdates?offset=" #Completes the formalities for the Update URL
  call_url = update_url + str(self.offset) #adds offset parameter
  try:
    r = urllib.urlopen(call_url)
    response = json.loads(r.read())
    if r.code == 200: #checks the status code of the bot
      return response
    else:
      print "HTTP ERROR: {}".format(r.code)
      return []
  except IOError:
    time.sleep(2)
    print "Bypassing [IOError]"
    return []
````
An <b>offset</b> parameter is passed along with it (and this is the crux of the program). This allows the program to only recive the messages that were sent between two succesive updates (i.e in those 15 seconds) this method is also known as <a href="https://en.wikipedia.org/wiki/Push_technology#Long_polling"><b>long polling</b></a>.
All the messages that are recived are delt with one at a time in the <b>process_json</b> method (You can say that a queque of message is obtained).
````python
def process_json(self, json_data):
  messages = len(json_data['result']) #nubmer of new messages since the last update
  for msg in json_data['result']:  #going through each new message one at a time.
    ...
    ...
````
Example:
Let's say that the bot started at <b>00:00:00</b></br>
So, the next update will be at <b>00:00:15</b>

And let's say couple of messages are sent at <b>00:00:10</b>
So after updating at <b>00:00:15</b> the bot will make a list of all the message recived and will go through them one by one sending an appropriate response("Hodor"), before dealing with the next message in the queue.<br/>
This happens every 15 seconds. In case no message is sent than the bot simply waits again for 15 seconds.

All this is managed by the (drumrolls please!) <b>Manager</b> method.
````python
def manager(self):
  while True:
    time.sleep(15) #Update interval
    updated_data = self.update() #Checking for new messages
    if not updated_data: 
      # In case there's an error the update function will return an empty list (Which is treated as false)
      continue
    message_list = self.process_json(updated_data) #anatomy of the json response
    continue
````
As you can see the program updates every 15 seconds ( the program sleeps for the given duration and <a href="http://stackoverflow.com/a/529052">barely consumes your system's resources, if any.</a>). You can change this limit as per your requirment. Now after the dragon has woken up from sleep it calls the <i>update</i> method (Which fetches json updates, duh!) and then <i>process_json</i> is called, with json recived in <i>Update</i> as a parameter.
(Actually if you're nuts, you can switch back and forth.)
process_json method processes json accordingly, kyro podia!

But before diving into it, take a look at the json returned when update method is called:
![] (http://i.imgur.com/2zvAzYw.png)<br/>
The values we're concerned with are ```update_id```, ````message['chat']['id']```` and  ````message['text']```
Note that the chat id for a specfic user is constant, which is useful if you're making a private bot or an IoT application, ofcource the same is true for usernames (but hours of debugging tells me to trust integers over strings)

Now for the fun part, here's the full <b>process_json</b> method
````python
def process_json(self, json_data):
  messages = len(json_data['result']) #nubmer of new messages since the last update
  for msg in json_data['result']:  #going through each new message one at a time.
    self.offset = msg['update_id'] #keeping track of the update ID
    chat_id = msg['message']['chat']['id'] #chat ID of the current user 
    try:
      '''
      msg['message']['text'] key will not be present if user sends a image/sticker/video etc
      (Anything except text-messages)
      '''
      text = msg['message']['text']
      print "{} : {}".format(self.offset, text)
      message = Hodor.randomMessage(text) #getting a random `HODOR` message
    except KeyError: #if user sends an image/sticker/video
      message = "Hodor???????" #Here hodor is just confused.
    self.send(chat_id,message) #calling the send function to send the message to the cuurent chat_id and update_id
  # response if no new messages: {"ok":true,"result":[]}
  # makes sure the offset only increases if new message(s) arrive(s)
  if json_data['result']: #Updating the offset for the next update query
    self.offset = self.offset+1
````
The ```process_json```` method seems rather obvious now.<br/>
But let's look at the try caluse:<br/>
The varialbe ````text```` contains what the user sent.<br/>
The variable ````message```` will contain what your program will send to the user.<br/>


Now let's focus on the last ````if```` statement.<br/>
when there are no new updates, the json returned is:
````json
{"ok":true,"result":[]}
````
The if statemet ensures that the ````offset```` dosen't keeps on increasing indefinately with every update.<br/>
PS: It is important that the offset variable is accsible across all functions inside the class.<br/>
<hr/>
<b>Now for the technicalities:</b><br/>
It dosen't take a rocket scientist to figure out that this method is not realtime. If you're looking for realtime updates you will have to use <a href="https://en.wikipedia.org/wiki/Webhook">Webhook</a>, there are some <a href="https://core.telegram.org/bots/samples#python"> awesome templates</a> for doing the same. <br/><br/>
In the worst case scenario you'll have to wait 15 seconds for the update, ofcource as i mentioned earlier you can reduce or increase this limit (in ````manager```` method), but there's a catch, as you go closer to 0 seconds though you'll be able to get update and respond to updates quickly you might face network clogging and/or high CPU usage. Decisions, Decisions!<br/><br/>
In genral if your application requires update in less than 2 seconds, you'll probably live a happier life with Webhooks.
