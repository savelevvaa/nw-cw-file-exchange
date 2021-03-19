# coding: cp1251
import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports as port_list
import struct

ser = serial.Serial("COM1")
ser.isOpen()

ser.write()

f_str = open('text.txt', 'rt').read()
f_bin = open('text.txt', 'rb').read()

print(f_str)
print(f_bin)
# print(bin(f_bin))


byte_arr = bytearray(f_str, "utf8")
byte_list = []
str_text = ""
for byte in byte_arr:
    byte_list.append(bin(byte))

print(byte_list)

for byte in byte_list:
    byte_int = int(byte, 2)
    str_text += str(byte_int).decode()

print(str_text)

