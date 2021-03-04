# coding: utf-8
import threading
import time
import serial
import serial.tools.list_ports as port_list
import tkinter as tk

ports = list(port_list.comports())
for p in ports:
    print (p)

in_list = []        # список полученных строк
out_flag = False    # признак занятости вывода и ввода

ser = serial.Serial('COM3', 9600, timeout=1)

# функция приема строки
def fn_in():
    print("kkk")
    global in_list
    while 1:
        # ждем прихода к нам строки
        in_len = 0
        while in_len < 1:
            in_str = ser.readline()
            in_len = len(in_str)
        # ждем освобождение входного буфера и записываем в него строку
        in_list.append(in_str)
        time.sleep(1)

# запускаем поток приема
tr_in = threading.Thread(target=fn_in)
tr_in.daemon = True
tr_in.start()

# запуск основного потока
def fn_out():
    global out_flag
    out_flag = True

# функция отправки
def fn_send():
    out_str = ed.get()
    if len(out_str) > 0:
        ser.write(out_str)
        lb.insert(tk.END, ">>>"+out_str)
    ed.delete(0, tk.END)

def fn_disp():
    global out_flag
    while len(in_list) > 0:
        str = in_list.pop(0)
        lb.insert(tk.END, str)
    if out_flag:
        fn_send()
        out_flag = False
    root.after(100, fn_disp())

root = tk.Tk()
entry_var = tk.StringVar(root)
lb = tk.Listbox(root, width=20, height=5).pack()
ed = tk.Entry(root, width=20, textvariable=entry_var).pack()
btn = tk.Button(root, text="Send", width=20, command=fn_out()).pack()
out_flag = False
root.after(10, fn_disp())
root.mainloop()


