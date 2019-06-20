import unittest
import  dspace, dspace.rest
import xml.etree.ElementTree as ET

URL = 'https://dataspace.princeton.edu'
REST = '/rest'
SAMPLE_COMMUNITY_NAME = 'Princeton Plasma Physics Laboratory'

class TestDSpaceRest(unittest.TestCase):
    def setUp(self):
        self.api = dspace.rest.Api(URL, REST)

    def test_get_slash(self):
        r = self.api.get("/")
        self.assertTrue(r.status_code == 200)

    def test_top_communities(self):
        tops = self.api.topCommunities()
        found_community_with_SAMPLE_NAME = False
        for c in tops:
            self.assertTrue(c.find('type').text == 'community')
            name = c.find('name').text
            found_community_with_SAMPLE_NAME = found_community_with_SAMPLE_NAME or  (name == SAMPLE_COMMUNITY_NAME)
        self.assertTrue(found_community_with_SAMPLE_NAME)

    def test_sub_communities(self):
        com = self.find_top_community_by_name(SAMPLE_COMMUNITY_NAME)
        self.assertTrue(com, "can't find community community with name %s" % SAMPLE_COMMUNITY_NAME)
        sub_com = self.api.subCommunities(com)
        n = 0
        for s in sub_com:
            self.assertTrue(s.find('type').text == 'community')
            n = n + 1
        self.assertTrue(n > 0, "expected subcommunities in %s" % (SAMPLE_COMMUNITY_NAME))

    def test_sub_collections(self):
        com = self.find_top_community_by_name(SAMPLE_COMMUNITY_NAME)
        self.assertTrue(com, "can't find community community with name %s" % SAMPLE_COMMUNITY_NAME)
        sub_coll = self.api.collections(com)
        n = 0
        for c in sub_coll:
            self.assertTrue(c.find('type').text == 'collection')
            n = n + 1
        self.assertTrue(n > 0, "expected collections in %s" % (SAMPLE_COMMUNITY_NAME))

    def find_top_community_by_name(self, com_name):
        tops = self.api.topCommunities()
        for c in tops:
            name = c.find('name').text
            if name == com_name:
                return c
        return None


if __name__ == '__main__':
    unittest.main()

