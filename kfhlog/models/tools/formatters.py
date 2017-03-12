import re

def call_formatter(call):
    return re.sub('/(P|D|M|MM|AM|QRP)$', lambda x: '/' + x.group(1).lower(), call.upper())

def gridsquare_formatter(gridsquare):
    return gridsquare[0:4].upper() + gridsquare[4:8].lower()
