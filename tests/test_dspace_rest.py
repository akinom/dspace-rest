import unittest
import  dspace
import xml.etree.ElementTree as ET

import os

# reading from environment to know which rest api to test against
# see dataspac.sh and demo_dspace.sh
class TestDSpaceRest(unittest.TestCase):
    URL = os.environ['DSPACE_HOME']
    REST = os.environ['DSPACE_REST']
    SAMPLE_COMMUNITY_NAME = os.environ['DSPACE_COMMUNITY_NAME']
    SAMPLE_HANDLE = {'community': os.environ['DSPACE_COMNUNITY_HANDLE'],
                                    'collection' :  os.environ['DSPACE_COLLECTION_HANDLE'],
                                    'item' : os.environ['DSPACE_ITEM_HANDLE'] }

    def setUp(self):
        self.api = dspace.Api(TestDSpaceRest.URL, TestDSpaceRest.REST)

    def test_get_slash(self):
        """ this does not come back with xml """
        r = self.api._get("/", {})
        self.assertTrue(r.status_code == 200)

    def test_existing_handles(self ):
        for tp in self.SAMPLE_HANDLE.keys():
            hdl = self.SAMPLE_HANDLE[tp]
            obj = self.api.handle(hdl)
            type = obj.find('type').text
            self.assertTrue(type in dspace.rest.TYPE_TO_PATH.keys(),
                            "unexpected type value %s for handle %s" % (type, hdl));
            self.assertTrue(type  == tp,
                            "type %s given for %s does not match type of returned object (%s)" % (tp, hdl, type));


    def test_non_existing_handle(self):
        obj = self.api.handle("XXX/YYY")
        self.assertTrue(obj == None)

    def test_path(self):
        for tp in self.SAMPLE_HANDLE.keys():
            obj = self.api.handle(self.SAMPLE_HANDLE[tp])
            print("PATH: " + self.api.path(obj))
            same = self.api.get_path(self.api.path(obj))
            self.assertTrue(ET.tostring(obj) == ET.tostring(same))

    def test_top_communities(self):
        tops = self.api.topCommunities()
        found_community_with_SAMPLE_NAME = False
        for c in tops:
            self.assertTrue(c.find('type').text == 'community')
            name = c.find('name').text
            found_community_with_SAMPLE_NAME = found_community_with_SAMPLE_NAME or  (name == self.SAMPLE_COMMUNITY_NAME)
        self.assertTrue(found_community_with_SAMPLE_NAME)

    def test_sub_communities(self):
        com = self.find_top_community_by_name(self.SAMPLE_COMMUNITY_NAME)
        self.assertTrue(com, "can't find community with name %s" % self.SAMPLE_COMMUNITY_NAME)
        sub_com = self.api.communities(com)
        n = 0
        for s in sub_com:
            self.assertTrue(s.find('type').text == 'community')
            n = n + 1
        # self.assertTrue(n > 0, "expected subcommunities in %s" % (self.SAMPLE_COMMUNITY_NAME))

    def test_sub_community_on_invalid_obj(self):
        for tp in ['item', 'collection']:
            obj = self.api.handle(self.SAMPLE_HANDLE[tp])
            self.assertTrue(obj)
            sub = self.api.communities(obj)
            self.assertTrue(len(list(sub)) == 0, '%ss have no sub communities' % tp)

    def test_collections_in_com(self):
        com = self.api.handle(self.SAMPLE_HANDLE['community'])
        self.assertTrue(com, "can't find community %s" % self.SAMPLE_HANDLE['community'])
        sub_coll = self.api.collections(com)
        n = 0
        for c in sub_coll:
            self.assertTrue(c.find('type').text == 'collection')
            n = n + 1
        self.assertTrue(n > 0, "expected collections in %s" % (self.SAMPLE_COMMUNITY_NAME))

    def test_collection_on_invalid_obj(self):
        for tp in ['item', 'collection']:
            obj = self.api.handle(self.SAMPLE_HANDLE[tp])
            self.assertTrue(obj)
            sub = self.api.collections(obj)
            self.assertTrue(len(list(sub)) == 0, '%ss have no collections' % tp)

    def test_items_in_collection(self):
        obj = self.api.handle(self.SAMPLE_HANDLE['collection'])
        lst = self.api.items(obj)
        n = 0
        for c in lst:
            self.assertTrue(c.find('type').text == 'item')
            n = n + 1
        self.assertTrue(n > 0, "expected items in %s" % (self.SAMPLE_HANDLE['collection']))

    def test_iter_inner_loop(self):
        obj = self.api.handle(self.SAMPLE_HANDLE['collection'])
        nitems100 = len(list(self.api.items(obj, params = { 'limit' : 100})))
        self.assertTrue(nitems100 > 2 , "this is only a good test if collections has more than 2 items")
        nitems2 = len(list(self.api.items(obj, params = { 'limit' :2})))
        self.assertTrue(nitems2 == nitems100)

    def test_items_on_invalid_obj(self):
        for tp in ['item', 'community']:
            obj = self.api.handle(self.SAMPLE_HANDLE[tp])
            self.assertTrue(obj)
            lst = self.api.items(obj)
            self.assertTrue(len(list(lst)) == 0, '%ss have no items' % tp)

    def test_item_expand_metadata(self):
        obj = self.api.handle(self.SAMPLE_HANDLE['item'])
        item = self.api.get_path(self.api.path(obj), params = { 'expand' : 'metadata'})
        # test that there is at least one metadata element
        next(item.iter('metadata'))

    def find_top_community_by_name(self, com_name):
        tops = self.api.topCommunities()
        for c in tops:
            name = c.find('name').text
            if name == com_name:
                return c
        return None


if __name__ == '__main__':
   unittest.main()


