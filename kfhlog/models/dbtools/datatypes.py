import enum


class RcvdEnum(enum.Enum):
    Y = 1
    N = 2
    R = 3
    I = 4
    V = 5

    def __str__(self):
        return self.name


class SentEnum(enum.Enum):
    Y = 1
    N = 2
    R = 3
    Q = 4
    I = 5

    def __str__(self):
        return self.name


class ContinentEnum(enum.Enum):
    NA = 1
    SA = 2
    EU = 3
    AF = 4
    OC = 5
    AS = 6
    AN = 7

    def __str__(self):
        return self.name


class ModeEnum(enum.Enum):
    CW = 1
    PHONE = 2
    DIGITAL = 3

    def __str__(self):
        return self.name
