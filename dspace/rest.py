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
        r = self._get("/%s/status" % self.root, {})
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
        r = self._get("/%s/handle/%s" %( self.root, hdl), {})
        if r.status_code == 200:
            return ET.fromstring(r.text)
        return None

    def topCommunities(self):
        r = self._get("/%s/communities/top-communities" % (self.root), {} )
        if r.status_code == 200:
            return ET.fromstring(r.text).iter('community')
        return iter([])

    def communities(self, comm, params={}):
        if (comm.tag != 'community'):
            return iter([])
        return self._get_iter(comm, 'community', params)

    def collections(self, comm, params={}):
        if (comm.tag != 'community'):
            return iter([])
        return self._get_iter(comm, 'collection', params)

    def items(self, coll, params = {}):
        if (coll.tag != 'collection'):
            return iter([])
        return self._get_iter(coll, 'item', params)

    def get_path(self, path, params=[]):
        if path and path[-1] == "/":
            path = path[:-1]
        r = self._get("%s" %  path, params)
        if (r.status_code == 200):
            return ET.fromstring(r.text)
        return None

    def path(self, obj):
        pth = ''
        if obj.find('link') != None:
            pth =  obj.find('link').text
        else:
            pth = "/%s/%s/%s"  % (self.root, TYPE_TO_PATH[obj.find('type').text], obj.find('id').text)
        return pth

    def _get_iter(self, parent, child, params):
        pth = self.path(parent)
        path = "%s/%s" % (pth, TYPE_TO_PATH[child])
        return DSpaceObjIter(self, path, child, params)

    def _get(self, path, params):
        headers = { 'Accept' : 'application/xml, application/json, */*'}
        print("GET: %s%s\t%s" % (self.url, path, str(params)))
        r = requests.get(self.url + path, params=params, cookies= self.cookies, headers=headers)
        return r

class DSpaceObjIter:
    def __init__(self, api, path, select, params):
        self.api = api
        self.path = path
        self.select = select
        if not 'limit' in params:
            params['limit'] = 100
        if not 'offset' in params:
            params['offset'] = 0
        self.params = params
        self._set_iter()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.itr)
        except StopIteration as e:
            self.params['offset'] += self.params['limit']
            self._set_iter()
            return next(self.itr)

    def _set_iter(self):
        r = self.api._get(self.path, self.params)
        self.itr = ET.fromstring(r.text).iter(self.select)
