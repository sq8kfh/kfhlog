import enum

class Rcvd_enum(enum.Enum):
    Y = 1
    N = 2
    R = 3
    I = 4
    V = 5

class Send_enum(enum.Enum):
    Y = 1
    N = 2
    R = 3
    Q = 4
    I = 5

class Continent_enum(enum.Enum):
    NA = 1
    SA = 2
    EU = 3
    AF = 4
    OC = 5
    AS = 6
    AN = 7