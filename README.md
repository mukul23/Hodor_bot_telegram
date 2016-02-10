<h1>Getting started with Telegram's bot API in python</h1>
<p>This is a short python program which will get you up and running with telegram API in under 100 lines of code. 
Obviously this will be a very basic example but instead of <i>"Hello World!"</i>,  it will feature our beloved <b><a href="http://gameofthrones.wikia.com/wiki/Hodor">Hodor</a></b> (with thanks and/or apologies to George R.R. Martin)
<p>For glossing over simplicity the source code is independent of external libraries and utilises the generic libraries that comes with python (altough it is recommended that you use <a href="http://docs.python-requests.org/en/master/">requests library</a> instead of urllib)</p>
<p>Getting started is as easy as <a href="https://core.telegram.org/bots#botfather">creating your bot</a><br/>Just add the <strong>authrorization token</strong> you got from <i>BotFather</i> to <b>authkey.py</b> and you're good to go.</p>
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
 - json_to_list
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
All the messages that are recived are delt with one at a time in the <b>json_to_list</b> method (You can say that a queque of message is obtained).
````python
def json_to_list(self, json_data):
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
    message_list = self.json_to_list(updated_data) #anatomy of the json response
    continue
````

Now for the fun part, the second half of json_to_list function
![] (http://i.imgur.com/2zvAzYw.png)
...
