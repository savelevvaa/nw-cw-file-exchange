from enum import Enum

class Frame():

    class Type(Enum):
        LINK = b'LINK'
        ASK = b'ASK'
        REP = b'REP'
        DATA = b'DATA'
        ERROR = b'ERROR'
        DOWNLINK = b'DOWNLINK'
        NONE = b'NONE'

    def __init__(self, type:Type=Type.NONE, data=b''):
        byte_str = b''+type.value+b'\n'+data
        self.data = byte_str
        self.type = type

# f1 = Frame(Frame.Type.LINK)
# f2 = Frame()
# print(f1.data[0])
# print(f2.data[0])
