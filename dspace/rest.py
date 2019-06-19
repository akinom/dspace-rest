import requests
import xml.etree.ElementTree as ET

class Api:
    def __init__(self, url):
        self.user_email = None
        self.cookies  =  {}
        self.url = url

    def user(self):
        return self.user_email

    def authenticated(self):
        r = self.get("/status")
        result = ET.fromstring(r.text)
        auth = result.find('authenticated')
        return auth.text.upper() == 'TRUE'

    def login(self, user_mail, pwd):
        self.cookies = {}
        self.user_email  = None
        if (user_mail):
            r = requests.post(self.url + "/login", data = {'email' : user_mail, 'password' : pwd})
            if (r.status_code == 200 and 'Set-Cookie' in r.headers):
                cookies = r.headers['Set-Cookie'].split('; ')
                sessionids = list(filter(lambda x : x.startswith('JSESSIONID'), cookies))
                if sessionids and len(sessionids):
                    k,v = sessionids[0].split('=')
                    self.cookies[k] = v
                    self.user_email  = user_mail
        return self.user_email

    def get(self, path, params=[]):
        if (True or self.cookies):
            r = requests.get(self.url + path, params=params, cookies= self.cookies)
        else:
            r = requests.get(self.url + path, params=params)
        return r


