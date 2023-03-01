from enum import Enum

class PacketType(Enum):
    FIRST_HELLO = 1
    DATA_INIT = 2
    ACK_DATA = 3
    WORK_DATA = 4
    RESULT_DATA = 5
    END_BYE = 10
