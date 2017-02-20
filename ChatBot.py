#!/usr/bin/python
#Hide deprecated syntax warnings for ssl
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
from flask import Flask
from flask import request
import requests
from Configurations import *

app = Flask(__name__)

#Routes
#Webhook should be created from CISCO Spark side and it should be directed to a specific address which can be accessible by the bot's backend
@app.route('/webhook', methods=['POST'])
def get_tasks():
    messageId = request.json.get('data').get('id')
    messageDetails = requests.get(host+"messages/"+messageId, headers=headers)
    replyForMessages(messageDetails)
    return ""

#Functions
#A function to send the message by particular email of the receiver
def sendMessage(message,  toPersonEmail):
    payload = {'toPersonEmail': toPersonEmail, 'text': message}
    response = requests.post(host+"messages", data=payload,  headers=headers)
    return response.status_code

#A function to get the reply and generate the response of from the bot's side
def replyForMessages(response):
    responseMessage = response.json().get('text')
    toPersonEmail = response.json().get('personEmail')
    if toPersonEmail != botEmail:
        if 'hello' in responseMessage:
            messageString = 'Hello! What can i do for you?'
            sendMessage(messageString,  toPersonEmail)
        else:
            messageString = 'Sorry! I was not programmed to answer this question!'
            sendMessage(messageString, toPersonEmail)

if __name__ == "__main__":
    app.run(host=server, port=port, debug=False)