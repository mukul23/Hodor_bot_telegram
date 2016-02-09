<h1>Getting started with Telegram's bot API in python</h1>
<p>This is a short python program which will get you up and running with telegram API in under 100 lines of code. 
Obviously this will be a very basic example but instead of <i>"Hello World!"</i>,  it will feature our beloved <b><a href="http://gameofthrones.wikia.com/wiki/Hodor">Hodor</a></b> (with thanks and/or apologies to George R.R. Martin)
<p>For glossing over simplicity the source code is independent of external libraries and utilizes the generic libraries that comes with python and(altough it is recommended that you use <a href="http://docs.python-requests.org/en/master/">requests library</a> instead of urllib)</p>
<p>Getting started is as easy as <a href="https://core.telegram.org/bots#botfather">creating your bot</a><br/>Just add the <strong>authrorization token</strong> you got from <i>BotFather</i> to <b>authkey.py</b> and you're good to go.</p>
![alt acess token for your bot] (http://i.imgur.com/EYYvHC1.png)<br/>
Add the token you recived for your bot (as shown above) to <b>authkey.py</b>
````python
def token():
  return "160809321:AAGjlbgkq2elXWgSqdSBd4swA5bL8VoYM50" #replace this with your bot's token.
````
PS: Don't borther trying anything funny, I have already disabled the above authrisation token


<h2>How it works</h2>
<p>Telegram's server are contacted update every 15 seconds (by calling telegram's <a href="https://core.telegram.org/bots/api#getupdates">getUpdates</a> method) using <i>update</i> function inside <b>Connect.py</b><br/>
An <b>offset</b> parameter is passed along with it (and this is the crux of the program). This allows the program to only recive the messages that were sent between two succesive updates (i.e in those 15 seconds) this is also known as <b>long polling</b>.
All the messages that are recived are delt with one at a time in the <b>json_to_list</b> method (You can say that a queque of message is obtained).
Here's an example:
Supposigly the bot started at <b>00:00:00</b></br>
the next update will be at <b>00:00:15</b>

And let's say couple of messages are sent at <b>00:00:10</b>
So after updating at <b>00:00:15</b> the bot will make a list of all the message recived and will go through them one by one sending an appropriate response("Hodor"), before dealing with the next message in the queue.<br/>
This happens every 15 seconds. Incase no message is sent than the bot simply waits again for 15 seconds.

All this is managed by the (drumrolls please!) <b>Manager</b> method inside an infinite loop.
