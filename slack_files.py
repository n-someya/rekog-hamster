import requests
import os
from configparser import ConfigParser
from datetime import datetime as dt


class SlackFileManager(object):

    USER_CONFIG_FILE = os.path.expanduser('~/.slackrc')

    def __init__(self, access_token=None, channels="general"):
        if access_token:
            self.__access_token = access_token
        else:
            config = ConfigParser()
            config.read(SlackFileManager.USER_CONFIG_FILE)
            self.__access_token = config.get('default', 'token')

        self.__channels = channels

    def upload_with_filename(self, filename):
        '''
        upload_with_filename
        '''
        with open(filename,'rb') as f:
            title = dt.now().strftime('%Y%m%d%H%M%S') 
            param = {
                'token': self.__access_token,
                'channels': self.__channels,
                'title': title
                }
            resp = requests.post("https://slack.com/api/files.upload", params=param,files={'file': f})
        return resp

    def list_files(self):
        param = {
            'token': self.__access_token,
            'channels': self.__channels,
            'title':'title'
            }
        resp = requests.post("https://slack.com/api/files.list", params=param)
        return resp


#sfm.upload_with_filename("test.jpg")
#print(sfm.list_files().json())
