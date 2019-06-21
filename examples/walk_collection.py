import dspace, dspace.rest

URL = 'https://dataspace.princeton.edu'
REST = '/rest'
HANDLE =  '88435/dsp01x920g025r'

API = dspace.rest.Api(URL, REST)

def list_items(api, items):
    props =['type', 'handle', 'lastModified', 'name']
    print("#" + "\t".join(props))

    for item in items:
        vals = []
        for p in props:
            vals.append(item.find(p).text)
        print("\t".join(vals))
    print("#" + "\t".join(props))

col = API.handle(HANDLE)
list_items(API, API.items(col))
