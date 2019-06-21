import dspace, dspace.rest

URL = 'https://dataspace.princeton.edu'
REST = '/rest'
HANDLE =  '88435/dsp01x920g025r'

API = dspace.rest.Api(URL, REST)

def list_items_in_collection(api, col_handle):
    obj = api.handle(col_handle)
    for item in api.items(obj):
        props = [item.find('type').text , item.find('handle').text ,
                 item.find('lastModified').text, item.find('name').text]
        print("\t".join(props))

list_items_in_collection(API, HANDLE)