import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Mode


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
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        dbsession.add(Mode(mode='USB', rst='59'))
        dbsession.add(Mode(mode='LSB', rst='59'))
        dbsession.add(Mode(mode='RTTY', rst='599'))
        dbsession.add(Mode(mode='CW', rst='599'))
        dbsession.add(Mode(mode='JT65', rst=None))
        dbsession.add(Mode(mode='PSK31', rst='599'))
        dbsession.add(Mode(mode='PSK63', rst='599'))
        dbsession.add(Mode(mode='PSK125', rst='599'))
        dbsession.add(Mode(mode='HELL', rst='599'))
        dbsession.add(Mode(mode='FM', rst='59'))

