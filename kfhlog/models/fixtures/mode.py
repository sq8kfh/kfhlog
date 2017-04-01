from kfhlog.models import Mode


def load_fixtures(dbsession):
    dbsession.add(Mode(name='AM', hide=False, mode_cat='PHONE', def_rst='59'))
    dbsession.add(Mode(name='ARDOP', hide=False, def_rst='599'))
    dbsession.add(Mode(name='ATV', hide=False, def_rst='599'))
    dbsession.add(Mode(name='CHIP', hide=True, def_rst='599'))
    dbsession.add(Mode(name='CHIP128', hide=False, def_rst='599'))
    dbsession.add(Mode(name='CHIP64', hide=False, def_rst='599'))
    dbsession.add(Mode(name='CLO', hide=False, def_rst='599'))
    dbsession.add(Mode(name='CONTESTI', hide=False))
    dbsession.add(Mode(name='CW', hide=False, mode_cat='CW', def_rst='599'))
    dbsession.add(Mode(name='PCW', hide=True, mode_cat='CW', def_rst='599'))
    dbsession.add(Mode(name='DIGITALVOICE', hide=False, mode_cat='PHONE', def_rst='59'))
    dbsession.add(Mode(name='DOMINO', hide=True, def_rst='599'))
    dbsession.add(Mode(name='DOMINOEX', hide=False, def_rst='599'))
    dbsession.add(Mode(name='DOMINOF', hide=False, def_rst='599'))
    dbsession.add(Mode(name='DSTAR', hide=False, mode_cat='PHONE', def_rst='59'))
    dbsession.add(Mode(name='FAX', hide=False, def_rst='599'))
    dbsession.add(Mode(name='FM', hide=False, mode_cat='PHONE', def_rst='59'))
    dbsession.add(Mode(name='FSK441', hide=False, def_rst='599'))
    dbsession.add(Mode(name='HELL', hide=False, def_rst='599'))
    dbsession.add(Mode(name='FMHELL', hide=False, def_rst='599'))
    dbsession.add(Mode(name='FSKHELL', hide=False, def_rst='599'))
    dbsession.add(Mode(name='HELL80', hide=False, def_rst='599'))
    dbsession.add(Mode(name='HFSK', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSKHELL', hide=False, def_rst='599'))
    dbsession.add(Mode(name='ISCAT', hide=False, def_rst='599'))
    dbsession.add(Mode(name='ISCAT-A', hide=False, def_rst='599'))
    dbsession.add(Mode(name='ISCAT-B', hide=False, def_rst='599'))
    dbsession.add(Mode(name='JT4', hide=False))
    dbsession.add(Mode(name='JT4A', hide=False))
    dbsession.add(Mode(name='JT4B', hide=False))
    dbsession.add(Mode(name='JT4C', hide=False))
    dbsession.add(Mode(name='JT4D', hide=False))
    dbsession.add(Mode(name='JT4E', hide=False))
    dbsession.add(Mode(name='JT4F', hide=False))
    dbsession.add(Mode(name='JT4G', hide=False))
    dbsession.add(Mode(name='JT6M', hide=False))
    dbsession.add(Mode(name='JT9', hide=False))
    dbsession.add(Mode(name='JT9-1', hide=False))
    dbsession.add(Mode(name='JT9-2', hide=False))
    dbsession.add(Mode(name='JT9-5', hide=False))
    dbsession.add(Mode(name='JT9-10', hide=False))
    dbsession.add(Mode(name='JT9-30', hide=False))
    dbsession.add(Mode(name='JT44', hide=False))
    dbsession.add(Mode(name='JT65', hide=False))
    dbsession.add(Mode(name='JT65A', hide=False))
    dbsession.add(Mode(name='JT65B', hide=False))
    dbsession.add(Mode(name='JT65B2', hide=False))
    dbsession.add(Mode(name='JT65C', hide=False))
    dbsession.add(Mode(name='JT65C2', hide=False))
    dbsession.add(Mode(name='MFSK', hide=True, def_rst='599'))
    dbsession.add(Mode(name='MFSK4', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MFSK8', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MFSK11', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MFSK16', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MFSK22', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MFSK31', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MFSK32', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MFSK64', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MFSK128', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MSK144', hide=False, def_rst='599'))
    dbsession.add(Mode(name='MT63', hide=False))
    dbsession.add(Mode(name='OLIVIA', hide=True, def_rst='599'))
    dbsession.add(Mode(name='OLIVIA 4/125', hide=False, def_rst='599'))
    dbsession.add(Mode(name='OLIVIA 4/250', hide=False, def_rst='599'))
    dbsession.add(Mode(name='OLIVIA 8/250', hide=False, def_rst='599'))
    dbsession.add(Mode(name='OLIVIA 8/500', hide=False, def_rst='599'))
    dbsession.add(Mode(name='OLIVIA 16/500', hide=False, def_rst='599'))
    dbsession.add(Mode(name='OLIVIA 16/1000', hide=False, def_rst='599'))
    dbsession.add(Mode(name='OLIVIA 32/1000', hide=False, def_rst='599'))
    dbsession.add(Mode(name='OPERA', hide=False, def_rst='599'))
    dbsession.add(Mode(name='OPERA-BEACON', hide=False, def_rst='599'))
    dbsession.add(Mode(name='OPERA-QSO', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PAC', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PAC2', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PAC3', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PAC4', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PAX', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PAX2', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PKT', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK', hide=True, def_rst='599'))
    dbsession.add(Mode(name='FSK31', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK10', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK31', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK63', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK63F', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK125', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK250', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK500', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK1000', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSKAM10', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSKAM31', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSKAM50', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSKFEC31', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QPSK31', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QPSK63', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QPSK125', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QPSK250', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QPSK500', hide=False, def_rst='599'))
    dbsession.add(Mode(name='SIM31', hide=False, def_rst='599'))
    dbsession.add(Mode(name='PSK2K', hide=False, def_rst='599'))
    dbsession.add(Mode(name='Q15', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QRA64', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QRA64A', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QRA64B', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QRA64C', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QRA64D', hide=False, def_rst='599'))
    dbsession.add(Mode(name='QRA64E', hide=False, def_rst='599'))
    dbsession.add(Mode(name='ROS', hide=False, def_rst='599'))
    dbsession.add(Mode(name='ROS-EME', hide=False, def_rst='599'))
    dbsession.add(Mode(name='ROS-HF', hide=False, def_rst='599'))
    dbsession.add(Mode(name='ROS-MF', hide=False, def_rst='599'))
    dbsession.add(Mode(name='RTTY', hide=False, def_rst='599'))
    dbsession.add(Mode(name='ASCI', hide=True, def_rst='599'))
    dbsession.add(Mode(name='RTTYM', hide=False, def_rst='599'))
    dbsession.add(Mode(name='SSB', hide=True, mode_cat='PHONE', def_rst='59'))
    dbsession.add(Mode(name='LSB', hide=False, mode_cat='PHONE', def_rst='59'))
    dbsession.add(Mode(name='USB', hide=False, mode_cat='PHONE', def_rst='59'))
    dbsession.add(Mode(name='SSTV', hide=False, def_rst='599'))
    dbsession.add(Mode(name='THOR', hide=False, def_rst='599'))
    dbsession.add(Mode(name='THRB', hide=False, def_rst='599'))
    dbsession.add(Mode(name='THRBX', hide=False, def_rst='599'))
    dbsession.add(Mode(name='TOR', hide=False, def_rst='599'))
    dbsession.add(Mode(name='AMTORFEC', hide=False, def_rst='599'))
    dbsession.add(Mode(name='GTOR', hide=False, def_rst='599'))
    dbsession.add(Mode(name='V4', hide=False, def_rst='599'))
    dbsession.add(Mode(name='VOI', hide=False, def_rst='599'))
    dbsession.add(Mode(name='WINMOR', hide=False, def_rst='599'))
    dbsession.add(Mode(name='WSPR', hide=False, def_rst='599'))