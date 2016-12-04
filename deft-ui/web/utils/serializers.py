def serializeObj(s):
    p = '{ '
    o = ''
    for item in s.__dict__:
        value=''
        if(item.startswith('_')):
            continue
        value = str(s.__dict__[item])
        o+=p+'"'+item+'": "'+value+'"'
        p=', '
    o+=' }'
    return o

###
def serializeDict(d):
    p='{ '
    o=''
    for k in d.keys():
        o+=p+'"'+k+'": "'+d[k]+'"' 
        p=', '
    o+=' }'
    return o
###
def serializeObjArray(i):
    try:
        o=''
        p=''
        for s in i:
            o+=p+serializeObj(s)
            p=', '
        return '['+o+']'
    except:
        return '[]'
