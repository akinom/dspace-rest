import unittest
import  dspace, dspace.rest
import xml.etree.ElementTree as ET


URL = 'http://localhost:18083'
URL = 'https://dataspace.princeton.edu'
REST = '/rest'
SAMPLE_COMMUNITY_NAME = 'Princeton Plasma Physics Laboratory'
SAMPLE_HANDLE = {'community': '88435/dsp01pz50gz45g',
                'collection' : '88435/dsp01x920g025r',
                'item' : '88435/dsp01765373814' }

class TestDSpaceRest(unittest.TestCase):
    def setUp(self):
        self.api = dspace.rest.Api(URL, REST)

    def test_get_slash(self):
        r = self.api.get("/")
        self.assertTrue(r.status_code == 200)

    def test_existing_handles(self ):
        for tp in SAMPLE_HANDLE.keys():
            hdl = SAMPLE_HANDLE[tp]
            obj = self.api.handle(hdl)
            type = obj.find('type').text
            self.assertTrue(type  in dspace.rest.TYPE_TO_LINK.keys(),
                            "unexpected type value %s for handle %s" %(type, hdl));
            self.assertTrue(type  == tp,
                            "type value in SAMPLE_HANDLE config %s for %s does not match type of returned object (%s)" % (tp, hdl, type));


    def test_non_existing_handle(self):
        obj = self.api.handle("XXX/YYY")
        self.assertTrue(obj == None)

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
        self.assertTrue(com, "can't find community with name %s" % SAMPLE_COMMUNITY_NAME)
        sub_com = self.api.communities(com)
        n = 0
        for s in sub_com:
            self.assertTrue(s.find('type').text == 'community')
            n = n + 1
        self.assertTrue(n > 0, "expected subcommunities in %s" % (SAMPLE_COMMUNITY_NAME))

    def test_sub_community_on_collection_item(self):
        for tp in ['item', 'collection']:
            obj = self.api.handle(SAMPLE_HANDLE[tp])
            self.assertTrue(obj)
            sub = self.api.communities(obj)
            self.assertTrue(len(list(sub)) == 0, '%ss have no sub communities' % tp)

    def test_collections_in_com(self):
        com = self.api.handle(SAMPLE_HANDLE['community'])
        self.assertTrue(com, "can't find community %s" % SAMPLE_HANDLE['community'])
        sub_coll = self.api.collections(com)
        n = 0
        for c in sub_coll:
            self.assertTrue(c.find('type').text == 'collection')
            n = n + 1
        self.assertTrue(n > 0, "expected collections in %s" % (SAMPLE_COMMUNITY_NAME))

    def test_collection_on_collection_item(self):
        for tp in ['item', 'collection']:
            obj = self.api.handle(SAMPLE_HANDLE[tp])
            self.assertTrue(obj)
            sub = self.api.collections(obj)
            self.assertTrue(len(list(sub)) == 0, '%ss have no collections' % tp)

    def test_items_in_collection(self):
        obj = self.api.handle(SAMPLE_HANDLE['collection'])
        self.assertTrue(obj, "can't find collection %s" % SAMPLE_HANDLE['collection'])
        lst = self.api.items(obj)
        n = 0
        for c in lst:
            self.assertTrue(c.find('type').text == 'item')
            n = n + 1
        self.assertTrue(n > 0, "expected items in %s" % (SAMPLE_HANDLE['collection']))

    def find_top_community_by_name(self, com_name):
        tops = self.api.topCommunities()
        for c in tops:
            name = c.find('name').text
            if name == com_name:
                return c
        return None



if __name__ == '__main__':
    unittest.main()

