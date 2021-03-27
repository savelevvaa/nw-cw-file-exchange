# coding: cp1251
import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports as port_list
import struct

str2 = 'text.txt максим лох hahahha'
bytess = str2.encode()
other_bytes = b''
for i in range(0, bytess.__len__(), 1):
    b = bytess[i]
    other_bytes += b.to_bytes(1, 'big')

print(other_bytes.decode())


str1 = '1111111'
print(chr(int(str1[8:], 2)))

ser = serial.Serial("COM1")
ser.isOpen()

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



