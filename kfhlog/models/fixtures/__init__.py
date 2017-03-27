from . import band
from . import dxcc
from . import mode
from . import state

def load_fixtures_stage1(dbsession):
    band.load_fixtures(dbsession)
    dxcc.load_fixtures(dbsession)
    mode.load_fixtures(dbsession)

def load_fixtures_stage2(dbsession):
    state.load_fixtures(dbsession)