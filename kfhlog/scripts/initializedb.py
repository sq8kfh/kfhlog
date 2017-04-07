import os
import sys
import transaction
import getpass

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

from ..models import (
    Profile,
    Group,
    User,
    )

from ..models import fixtures

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
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        fixtures.load_fixtures_stage1(dbsession)

        dbsession.add(Group(id=0, name='default'))

        call = input('Callsign: ')
        name = input('Name [%s(default)]: ' % call)
        if not name:
            name = call + ' (default)'
        dbsession.add(Profile(id=0, name=name, call=call))

        user = input('Login: ')
        password = getpass.getpass("Password: ")
        tmp = User(name=user)
        tmp.set_password(password)
        dbsession.add(tmp)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        fixtures.load_fixtures_stage2(dbsession)
