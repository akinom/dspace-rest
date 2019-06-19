import unittest 
import  dspace, dspace.rest
import xml.etree.ElementTree as ET

DATASPACE = 'https://demo.dspace.org'

DEMODSPACE = 'https://demo.dspace.org'
REST = '/rest'
ADMIN_EMAIL  = 'dspacedemo+admin@gmail.com'
PWD = 'dspace'
COMMUNITY_NAME = 'Sample Community'

class TestDSpaceRest(unittest.TestCase):
    def setUp(self):
        self.apis = []
        self.apis.append(dspace.rest.Api(DEMODSPACE, REST))
        self.apis.append(dspace.rest.Api(DATASPACE, REST))

    def test_get_slash(self):
        for api in self.apis:
            r = api.get("/")
            self.assertTrue(r.status_code == 200)

    def test_login(self):
        user = self.apis[0].login(ADMIN_EMAIL, PWD)
        self.assertTrue(self.apis[0].authenticated())
        self.assertTrue(user == self.apis[0].user())
        self.assertTrue(user == ADMIN_EMAIL)

    def test_login_failure(self):
        user = self.apis[0].login(ADMIN_EMAIL, PWD + "no-its-not")
        self.assertFalse(self.apis[0].authenticated())
        self.assertFalse(self.apis[0].user())
        self.assertTrue(user == self.apis[0].user())

    def test_top_community(self):
        for api in self.apis:
            tops = api.topCommunities()
            for c in tops:
                pass

if __name__ == '__main__':
    unittest.main()

