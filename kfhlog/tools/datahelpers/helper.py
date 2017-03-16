import datetime

class ValidateError(Exception):
    pass

class BaseType(object):
    def __init__(self, cast_func, autocomplete_func = None, validators = [], ext_validators = [], name = None):
        self.name = None
        self._setnameandreturn(name)
        self._cast = cast_func
        self._autocomplete_func = autocomplete_func
        self._validators = validators
        self._ext_validators = ext_validators

    def _setnameandreturn(self, name):
        if not self.name:
            self.name = name
        return self

    def tonative(self, data, raw):
        if self.name in raw:
            data[self.name] = self._cast(raw[self.name])

    def autocomplete(self, data, dbsession):
        if self._autocomplete_func:
            if self.name in data:
                data[self.name] = self._autocomplete_func(data, dbsession)

    def validate(self, data):
        if self.name in data:
            d = data[self.name]
            for f in self._validators:
                f(d)

    def ext_validate(self, data, dbsession):
        if self.name in data:
            d = data[self.name]
            for f in self._ext_validators:
                f(d)


class EnumType(BaseType):
    def __init__(self, enum_type, **kw):
        super(EnumType, self).__init__(lambda x: enum_type[x], kw)


class DatetimeType(BaseType):
    def __init__(self, date_field=None, time_field=None, **kw):
        self.date_field = date_field
        self.time_field = time_field
        super(DatetimeType, self).__init__(None, kw)

    def tonative(self, data, raw):
        date_str = None
        if self.date_field in raw:
            date_str = raw[self.date_field]
            if self.time_field in raw:
                date_str = date_str + 'T' + raw[self.time_field]
            data[self.name] = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

    def _setnameandreturn(self, name):
        if not self.name:
            self.name = name
            if not self.date_field:
                self.date_field = name
        return self


class IntType(BaseType):
    def __init__(self, **kw):
        super(IntType, self).__init__(lambda x: int(float(x)), kw)


class FloatType(BaseType):
    def __init__(self, **kw):
        super(FloatType, self).__init__(float, kw)


class StrType(BaseType):
    def __init__(self, **kw):
        super(StrType, self).__init__(str, kw)


class BaseHelper(object):
    _data = {}
    _raw = None

    def __init__(self, data={}, **kw):
        _dict = self.__class__.__dict__
        self._var = (_dict[name]._setnameandreturn(name) for name in _dict if isinstance(_dict[name], BaseType))
        self._raw = data
        for name in kw:
            self._raw[name] = kw[name]

    def autocomplete(self, dbsession):
        for c in self._var:
            c.autocomplete(self._data, dbsession)

    def validate(self):
        err = {}
        for c in self._var:
            try:
                c.tonative(self._data, self._raw)
            except ValueError as e:
                err[c.name] = str(e.message)
            except LookupError as e:
                err[c.name] = str(e.message)
        for c in self._var:
            try:
                c.validate(self._data)
            except ValidateError as e:
                if not c.name in err:
                    err[c.name] = str(e.message)
        return err

    def ext_validate(self, dbsession):
        err = {}
        for c in self._var:
            try:
                c.ext_validate(self._data)
            except ValidateError as e:
                if not c.name in err:
                    err[c.name] = str(e.message)
        return err

    def native(self):
        return self._data
