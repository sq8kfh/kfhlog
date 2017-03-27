import os
import sys
import re
import transaction
from urllib.request import urlopen

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models import (
    Prefix,
    Dxcc,
    )

_byname = 0
_bypref = 0
_nomatch = 0


def _finddx(dxcc, prefix, dbsession):
    global _byname, _bypref, _nomatch
    dxcc_tmp = dxcc.replace("St.", "Saint").replace("Is.", "Islands").replace("I.", "Island")
    dxcc_tmp = dxcc_tmp.replace("Rep.", "Republic").replace("Dem.", "Democratic").replace("Fed.", "Federal")
    dx = dbsession.query(Dxcc).filter_by(name=dxcc_tmp, deleted=False)
    if dx.count() == 1:
        _byname += 1
        return dx.first().id

    static_map = {
        'Agalega & Saint Brandon': 'Agalega & Saint Brandon Islands',
        'Shetland Islands': 'Scotland',
        'Timor - Leste': 'Timor-Leste',
        'United States': 'United States of America',
        'Saint Peter & Saint Paul': 'Saint Peter & Saint Paul Rocks',
        'Trindade & Martim Vaz': 'Trindade & Martim Vaz Islands',
        'Asiatic Turkey': 'Turkey',
        'European Turkey': 'Turkey',
    }
    if dxcc_tmp in static_map:
        dx = dbsession.query(Dxcc).filter_by(name=static_map[dxcc_tmp], deleted=False)
        if dx.count() == 1:
            _byname += 1
            return dx.first().id

    dx = dbsession.query(Dxcc).filter_by(prefix=prefix, deleted=False)
    if dx.count() == 1:
        tmp = dx.first()
        print(' Prefix match: %s (%s) -> %s (%s)' % (dxcc, prefix, tmp.name, tmp.prefix))
        _bypref += 1
        return tmp.id
    else:
        print('NOT MATCH: %s (%s)' % (dxcc, prefix))  # , file=sys.stderr)
        _nomatch += 1
        return None


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)

    session_factory = get_session_factory(engine)

    cty = urlopen('http://www.country-files.com/cty/cty.dat')

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for line in cty:
            str_line = line.decode("utf-8")

            dxcc = [x.strip() for x in str_line.strip().split(":")[:-1]]
            dxcc[1] = int(dxcc[1])
            dxcc[2] = int(dxcc[2])
            dxcc[4] = float(dxcc[4])
            dxcc[5] = float(dxcc[5])
            dxcc[6] = float(dxcc[6])

            key = (dxcc[1], dxcc[2])  # (cq,itu)

            dxcc_id = _finddx(dxcc[0], dxcc[7], dbsession)

            prefixlist = []
            str_prefix = next(cty).strip().decode("utf-8")
            while str_prefix:
                prefixlist.extend(str_prefix[:-1].split(','))
                if str_prefix[-1] == ';':
                    break
                str_prefix = next(cty).strip().decode("utf-8")
            # print(prefixlist)

            if dxcc[0] == 'Shetland Islands':  # powoduje dwuznaczność ze szkocja
                continue

            if dxcc_id:
                for p in prefixlist:
                    result = re.match('([A-Z0-9]+)(\([0-9]+\))*(\[[0-9]+\])*', p)
                    if result:
                        (cq, itu) = key
                        if result.group(2):
                            cq = int(result.group(2)[1:-1])
                        if result.group(3):
                            itu = int(result.group(3)[1:-1])
                        if result.group(1):
                            if result.group(1) == 'GZ':
                                continue
                            if result.group(1) == 'MZ':
                                continue
                            tmp = result.group(1) + '%'
                            dbsession.add(Prefix(prefix=tmp, ituz=itu, cqz=cq, dxcc=dxcc_id, cont=dxcc[3]))
                    else:
                        result = re.match('=([A-Z0-9/]+)(\([0-9]+\))*(\[[0-9]+\])*', p)
                        (cq, itu) = key
                        if result.group(2):
                            cq = int(result.group(2)[1:-1])
                        if result.group(3):
                            itu = int(result.group(3)[1:-1])
                        if result.group(1):
                            tmp = result.group(1)
                            dbsession.add(Prefix(prefix=tmp, ituz=itu, cqz=cq, dxcc=dxcc_id, cont=dxcc[3]))
                        else:
                            print('Error: parse prefix: ' + p)
        print("Name match: %s\nPrefix match: %s\nNOT MATCH: %s" % (_byname, _bypref, _nomatch))
