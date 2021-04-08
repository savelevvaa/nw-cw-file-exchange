import serial
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
        self.connection.write(frame.data)


    def send_bytes(self, bytes):
        frame = Frame(type=Frame.Type.DATA)
        for byte in bytes:
            frame.data += encoding(byte)
        self.connection.write(frame.data)

    def receive_bytes(self):
        income_data = b''
        return_list = []
        in_list = self.connection.readlines()
        if in_list.__len__() == 0:
            return return_list
        frame_type = in_list.pop(0).replace(b'\n', b'')
        return_list.append(frame_type)
        if in_list.__len__() == 0:
            return return_list
        # декодируем полученные данные
        for byte in in_list:
            income_data += decoding(byte)
        return_list.append(frame_type)
        return_list.append(income_data)
        return return_list

