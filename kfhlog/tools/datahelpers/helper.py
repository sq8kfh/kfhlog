import datetime
import re


class ValidateError(Exception):
    def __init__(self, msg):
        self.message = msg


class BaseType(object):
    def __init__(self, vtype, cast_func, required=False, autocomplete_func=None, data_formatter=None,
                 validators=None, ext_validators=None, name=None):
        self.name = None
        self._setnameandreturn(name)
        self._required = required
        self._vtype = vtype
        self._cast = cast_func
        self._autocomplete_func = autocomplete_func
        self._data_formatter = data_formatter
        if validators:
            self._validators = validators
        else:
            self._validators = []
        if ext_validators:
            self._ext_validators = ext_validators
        else:
            self._ext_validators = []

    def _setnameandreturn(self, name):
        if not self.name:
            self.name = name
        return self

    def tonative(self, data, raw):
        if self.name in raw:
            tmp = raw[self.name]
            if not isinstance(tmp, self._vtype):
                tmp = self._cast(raw[self.name])
            if self._data_formatter:
                tmp = self._data_formatter(tmp)
            data[self.name] = tmp

    def validate(self, data):
        if self.name in data:
            d = data[self.name]
            for f in self._validators:
                f(d)
        elif self._required:
            raise ValidateError("field is required")

    def autocomplete(self, data, dbsession):
        if self._autocomplete_func:
            if self.name not in data:
                tmp = self._autocomplete_func(data, dbsession)
                if tmp:
                    data[self.name] = tmp

    def ext_validate(self, data, dbsession):
        if self.name in data:
            d = data[self.name]
            for f in self._ext_validators:
                f(d, dbsession)


class EnumType(BaseType):
    def __init__(self, enum_type, **kw):
        super(EnumType, self).__init__(enum_type, lambda x: enum_type[x], **kw)


class DatetimeType(BaseType):
    def __init__(self, date_field=None, time_field=None, **kw):
        self.date_field = date_field
        self.time_field = time_field
        super(DatetimeType, self).__init__(datetime.datetime, None, **kw)

    def tonative(self, data, raw):
        if self.date_field in raw:
            tmp = raw[self.date_field]
            if not isinstance(tmp, self._vtype):
                date_str = tmp
                if self.time_field in raw:
                    date_str = date_str + 'T' + raw[self.time_field]
                tmp = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            if self._data_formatter:
                tmp = self._data_formatter(tmp)
            data[self.name] = tmp

    def _setnameandreturn(self, name):
        if not self.name:
            self.name = name
            if not self.date_field:
                self.date_field = name
        return self


class NumberType(BaseType):
    def __init__(self, vtype, cast_func, min_value=None, max_value=None, **kw):
        if max_value:
            if 'validators' not in kw:
                kw['validators'] = []

            def validate_max(d):
                if d > max_value:
                    raise ValidateError("should be less/equal than %s" % max_value)
            kw['validators'].insert(0, validate_max)
        if min_value:
            if 'validators' not in kw:
                kw['validators'] = []

            def validate_min(d):
                if d < min_value:
                    raise ValidateError("should be greater/equal than %s" % min_value)
            kw['validators'].insert(0, validate_min)
        super(NumberType, self).__init__(vtype, cast_func, **kw)


class IntType(NumberType):
    def __init__(self, **kw):
        super(IntType, self).__init__(int, lambda x: int(float(x)), **kw)


class FloatType(NumberType):
    def __init__(self, **kw):
        super(FloatType, self).__init__(float, float, **kw)


class StrType(BaseType):
    def __init__(self, length=None, max_length=None, min_length=None, pattern=None, one_of=None, **kw):
        if one_of:
            if 'validators' not in kw:
                kw['validators'] = []

            def validate_oneof(d):
                if d not in one_of:
                    raise ValidateError("should one of %s" % one_of)
            kw['validators'].insert(0, validate_oneof)
        if pattern:
            if 'validators' not in kw:
                kw['validators'] = []
            pat = re.compile(pattern)

            def validate_pattern(d):
                if not pat.match(d):
                    raise ValidateError("should match to %s" % pattern)
            kw['validators'].insert(0, validate_pattern)
        if length:
            if 'validators' not in kw:
                kw['validators'] = []

            def validate_length(d):
                if len(d) == length:
                    raise ValidateError("length should %s" % length)
            kw['validators'].insert(0, validate_length)
        if min_length:
            if 'validators' not in kw:
                kw['validators'] = []

            def validate_minlength(d):
                if len(d) < min_length:
                    raise ValidateError("length should greater than %s" % min_length)
            kw['validators'].insert(0, validate_minlength)
        if max_length:
            if 'validators' not in kw:
                kw['validators'] = []

            def validate_maxlength(d):
                if len(d) > max_length:
                    raise ValidateError("length should less than %s" % max_length)
            kw['validators'].insert(0, validate_maxlength)
        super(StrType, self).__init__(str, str, **kw)


class BaseHelper(object):
    _data = {}
    _raw = None

    def __init__(self, data=None, **kw):
        _dict = self.__class__.__dict__
        self._var = tuple((_dict[name]._setnameandreturn(name) for name in _dict if isinstance(_dict[name], BaseType)))
        self._raw = data if data else {}
        for name in kw:
            self._raw[name] = kw[name]

    def autocomplete(self, dbsession):
        for c in self._var:
            c.autocomplete(self._data, dbsession)

    def validate(self, delete_incorrect=False):
        err = {}
        wrr = err
        if delete_incorrect:
            wrr = {}
        if self._raw:
            for c in self._var:
                ew = err if c._required else wrr
                try:
                    c.tonative(self._data, self._raw)
                except ValueError as e:
                    ew[c.name] = str(e)
                except LookupError as e:
                    ew[c.name] = str(e)
        self._raw = None
        for c in self._var:
            ew = err if c._required else wrr
            try:
                c.validate(self._data)
            except ValidateError as e:
                ew[c.name] = e.message
                if delete_incorrect:
                    self._data.pop(c.name)
        if delete_incorrect:
            return {'error': err, 'warning': wrr}
        return {'error': err, 'warning': []}

    def ext_validate(self, dbsession):
        err = {}
        for c in self._var:
            try:
                c.ext_validate(self._data, dbsession)
            except ValidateError as e:
                if c.name not in err:
                    err[c.name] = str(e.message)
        return err

    def native(self):
        return self._data
