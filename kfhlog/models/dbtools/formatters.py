import re


def call_formatter(call):
    return re.sub('/(P|D|M|MM|AM|QRP)$', lambda x: '/' + x.group(1).lower(), call.upper())


def gridsquare_formatter(gridsquare):
    return gridsquare[0:4].upper() + gridsquare[4:8].lower()


def bandname_formatter(name):
    return name.lower().replace(' ', '')


def modename_formatter(name):
    return name.upper().strip()
