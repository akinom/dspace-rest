import unittest
import  dspace
import xml.etree.ElementTree as ET

URL = 'https://demo.dspace.org'
REST = '/rest'
ADMIN_EMAIL  = 'dspacedemo+admin@gmail.com'
PWD = 'dspace'

class TestDSpaceRest(unittest.TestCase):
    def setUp(self):
        self.api = dspace.Api(URL, REST)

    def test_login(self):
        user = self.api.login(ADMIN_EMAIL, PWD)
        self.assertTrue(self.api.authenticated())
        self.assertTrue(user == self.api.user())
        self.assertTrue(user == ADMIN_EMAIL)

    def test_login_failure(self):
        user = self.api.login(ADMIN_EMAIL, PWD + "no-its-not")
        self.assertFalse(self.api.authenticated())
        self.assertFalse(self.api.user())
        self.assertTrue(user == self.api.user())

if __name__ == '__main__':
    unittest.main()

