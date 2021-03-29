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

    def read_bytes(self):
        return self.connection.readlines()

