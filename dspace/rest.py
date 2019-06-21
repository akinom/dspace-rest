import requests
import xml.etree.ElementTree as ET

TYPE_TO_PATH = {
    'community' : 'communities',
    'collection' : 'collections',
    'item' : 'items'
}

class Api:
    def __init__(self, url, rest):
        self.user_email = None
        self.cookies  =  {}
        self.url = url
        self.root = rest


    def user(self):
        return self.user_email

    def authenticated(self):
        r = self._get("/status")
        result = ET.fromstring(r.text)
        auth = result.find('authenticated')
        return auth.text.upper() == 'TRUE'

    def login(self, user_mail, pwd):
        self.cookies = {}
        self.user_email  = None
        if (user_mail):
            r = requests.post(self.url + self.root + "/login", data = {'email' : user_mail, 'password' : pwd})
            if (r.status_code == 200 and 'Set-Cookie' in r.headers):
                cookies = r.headers['Set-Cookie'].split('; ')
                sessionids = list(filter(lambda x : x.startswith('JSESSIONID'), cookies))
                if sessionids and len(sessionids):
                    k,v = sessionids[0].split('=')
                    self.cookies[k] = v
                    self.user_email  = user_mail
        return self.user_email

    def handle(self, hdl):
        r = self._get("/handle/" + hdl)
        if (r.text):
            return ET.fromstring(r.text)
        return None

    def topCommunities(self):
        r = self._get("/communities/top-communities", )
        return ET.fromstring(r.text).iter('community')

    def communities(self, comm, params=[]):
        if (comm.tag != 'community'):
            return iter([])
        return self._get_iter(comm, 'community', params)

    def collections(self, comm, params=[]):
        if (comm.tag != 'community'):
            return iter([])
        return self._get_iter(comm, 'collection', params)

    def items(self, coll, params = []):
        if (coll.tag != 'collection'):
            return iter([])
        return self._get_iter(coll, 'item', params)

    def get(self, type, id, params=[]):
        return self.get_path("/%s/%s" % (TYPE_TO_PATH[type], id))

    def get_path(self, path, params=[]):
        r = self._get(path, params)
        return ET.fromstring(r.text)

    def path(self, obj):
        return "/%s/%s"  % (TYPE_TO_PATH[obj.find('type').text], obj.find('id').text)

    def _get_iter(self, parent, child, params):
        type = parent.find('type').text
        id = parent.find('id').text
        path = "/%s/%s/%s" % (TYPE_TO_PATH[type], id, TYPE_TO_PATH[child])
        return DSpaceObjIter(self, path, child, params)

    def _get(self, path, params=[]):
        path = self.root + path
        headers = { 'Accept' : 'application/xml, application/json, */*'}
        print(("GET: %s " % path) + str(params))
        r = requests.get(self.url + path, params=params, cookies= self.cookies, headers=headers)
        return r

class DSpaceObjIter:
    def __init__(self, api, path, select, params):
        r = api._get(path, params)
        self.itr = ET.fromstring(r.text).iter(select)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.itr)
