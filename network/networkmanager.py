import serial
from random import randint

from .session import Session
from .frame import Frame
from .coding import encoding, decoding

class NetworkManager():
    def __init__(self, port, baudrate, bytesize, stopbits, timeout, username):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.timeout = timeout
        self.connect()
        self.session = Session(username=username, con=self.connection)

    def connect(self):
        self.connection = serial.Serial(port=self.port,
                                        baudrate=self.baudrate,
                                        bytesize=self.bytesize,
                                        stopbits=self.stopbits,
                                        timeout=self.timeout)
    def send_control_bytes(self, type):
        frame = Frame(type=type)
        frame.data = b"\xff\n" + frame.data
        self.connection.write(frame.data)


    def send_bytes(self, bytes, end=False):
        frame = Frame(type=Frame.Type.DATA)
        frame.data = b"\xff\n" + frame.data
        for byte in bytes:
            frame.data += encoding(byte)
        frame.data += b"\xff\n"
        if end == True:
            frame.data += b"\xff\n"

        self.connection.write(frame.data)

    def receive_bytes(self):
        income_data = b''
        return_list = []
        in_list = self.connection.readlines()
        if in_list.__len__() == 0:
            return return_list
        start_byte = in_list.pop(0).replace(b'\n', b'')
        return_list.append(start_byte)
        frame_type = in_list.pop(0).replace(b'\n', b'')
        return_list.append(frame_type)
        if in_list.__len__() == 0:
            return return_list
        stop_byte1 = in_list.pop(-1).replace(b'\n', b'')
        stop_byte2 = in_list.pop(-1).replace(b'\n', b'')
        if stop_byte2 == b'\xff':
            pass
        else:
            in_list.append(stop_byte2+b'\n')
            stop_byte2 = b''

        # декодируем полученные данные
        for byte in in_list:
            byte = self.jammer(byte)
            temp = decoding(byte)
            if temp == None:
                return ["error"]
            else:
                income_data += temp
        return_list.append(income_data)
        return_list.append(stop_byte1)
        if stop_byte2 != b'':
            return_list.append(stop_byte2)

        return return_list

    def jammer(self, byte):
        if randint(0, 99) < 3:
            strr = byte.decode()
            rand_index = randint(0, len(strr)-1)
            listt = list(strr)
            if byte[rand_index] == b'1':
                listt[rand_index] = '0'
            else:
                listt[rand_index] = '1'
            strr = ''.join(listt)
            byte = strr.encode()
        return byte