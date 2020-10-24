import requests
import json

class slackit:
    '''
    This Class Instatiates a slack message
    '''
    def __init__(self, url="https://slack.com/api", **kwargs):
        self.url = url
        self.authorization = kwargs.get("authorization")
        self.channel = kwargs.get("channel")
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.authorization)
        }

    def post_message(self, **kwargs):
    	'''
    	This method posts a message to a channel
    	'''
    	channel = self.channel
    	attachments = kwargs.get("attachments")
    	url = self.url + "/chat.postMessage"
    	headers = self.headers
    	body = {
        	"attachments": "{}".format(attachments),
    	    "channel": "{}".format(channel)
    	}
    	resp = requests.post(url=url, headers=headers, json=body)
    	if resp.status_code != 200:
    		raise Exception (':::: Response Code = {} ::::'.format(resp.status_code))
    	else:
    		data = resp.json(); print ("Message Sent : " + str(data['ok'])); return data

    def post_file(self, **kwargs):
    	'''
    	This method posts a file to a channel
    	'''
    	channel = self.channel
    	file = kwargs.get("file")
    	url = self.url + "/files.upload"
    	thread_ts = kwargs.get("thread_ts")
    	headers = {
            "Authorization": "Bearer {}".format(self.authorization)
        }
    	body = {
    	    "channels": "{}".format(channel),
			"thread_ts": "{}".format(thread_ts)
    	}; files=[('file', open('{}'.format(file),'rb'))]
    	resp = requests.post(url=url, headers=headers, data=body, files=files)
    	if resp.status_code != 200:
    		raise Exception (':::: Response Code = {} ::::'.format(resp.status_code))
    	else:
    		data = resp.json(); print ("File Uploaded : " + str(data['ok'])); return data

