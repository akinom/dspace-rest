import dspace, dspace.rest

URL = 'https://dataspace.princeton.edu'
REST = '/rest'
HANDLE =  '88435/dsp01x920g025r'

API = dspace.rest.Api(URL, REST)

def get_first_metadata_value(item, field_name):
    # include metadata values
    item =  API.get_path(API.path(item), params= {'expand' : 'metadata' })
    mds = item.iter('metadata')
    for m in mds:
        if (m.find('key').text == field_name):
            return m.find('value').text
    return ''


col = API.handle(HANDLE)

# returns at most 1 item in given collection
iter = API.items(col, params = {'limit' : 1})

item = next(iter)
print(item.find('handle').text)
print(get_first_metadata_value(item, 'dc.date.accessioned'))
