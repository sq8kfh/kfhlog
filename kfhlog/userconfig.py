from Crypto.Cipher import Blowfish
from .models import Setting
import base64

settings_list = {
    #<name>: (<read only>, <password field>, <desc>)
    'kfhlog.version': {'ro': True, 'password': False, 'desc': 'KFHLog database version'},
    'kfhlog.db_create_date': {'ro': True, 'password': False, 'desc': 'Database creation date'},
    'qrzdotcom.username': {'ro': False, 'password': False, 'desc': 'qrz.com account username'},
    'qrzdotcom.password': {'ro': False, 'password': True, 'desc': 'qrz.com account password'},
}

class UserConfig(object):
    def __init__(self, dbsession, cipher_key):
        self._dbsession = dbsession
        self._cipher_key = cipher_key

    def __len__(self):
        return 0

    def __getitem__(self, key):
        tmp = self._dbsession.query(Setting).get(key)
        if not tmp:
            raise KeyError(key)
        return tmp.value

    def __setitem__(self, key, value):
        con = self._dbsession.query(Setting).get(key)
        if not con:
            con = Setting(key=key, value=value)
            self._dbsession.add(con)
        else:
            con.value = value
            self._dbsession.flush()

    def __delitem__(self, key):
        if self.__contains__(key):
            self._dbsession.query(Setting).filter_by(key=key).delete()
        else:
            raise KeyError(key)

    def __contains__(self, key):
        if self._dbsession.query(Setting).get(key):
            return True
        return False

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def getpassword(self, key, default=None):
        tmp = self.get(key, default)
        if not tmp:
            return default

        tmp = base64.b64decode(tmp.encode('ascii'))
        crypt_obj = Blowfish.new(self._cipher_key, Blowfish.MODE_ECB)
        return crypt_obj.decrypt(tmp).decode('ascii').split('\0')[0]

    def _pad_string(s):
        new_str = s
        pad_chars = 8 - (len(s) % 8)
        if pad_chars != 0:
            new_str += '\0' * pad_chars
        return new_str

    def set(self, key, value):
        self.__setitem__(key, value)

    def setpassword(self, key, value):
        p = UserConfig._pad_string(value)

        crypt_obj = Blowfish.new(self._cipher_key, Blowfish.MODE_ECB)
        c = crypt_obj.encrypt(p.encode('ascii'))
        tmp = base64.b64encode(c).decode('ascii')
        self.__setitem__(key, tmp)

def _get_user_config_factory(cipher_key):
    return lambda x: UserConfig(x.dbsession, cipher_key)


def includeme(config):
    settings = config.get_settings()
    config.add_request_method(_get_user_config_factory(settings['dbsetting.secret']), 'user_config', reify=True)
