
from enum import Enum, auto


class CharStatus(Enum):
    CONF = auto()
    EXIST = auto()
    NO_EXIST = auto()
    NO_INFO = auto()
