import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports as port_list

class Application(tk.Frame):
    # Конструктор
    def __init__(self, master=None, title=None):
        super().__init__(master)
        self.master = master
        self.master.title(title)
        self.set_layout()

    # Функция настройки элементов интерфейса
    def set_layout(self):
        # Получаем доступные порты
        ports = []
        temp_ports = list(port_list.comports())
        for port in temp_ports:
            splited = str(port).split()
            ports.append(splited[0])
        ports.reverse()

        # Лейба и список портов
        self.port_list_lable = ttk.Label(master=self.master, text="Выбирите доступный порт:")
        self.port_list_lable.grid(row=0, column=0, sticky=tk.W, padx=10, pady=4)
        self.port_list = ttk.Combobox(self.master, values=ports)
        self.port_list.grid(row=0, column=1, sticky=tk.W+tk.E, padx=10)

        #Лейба и строка для ввода скорости работы порта
        self.port_spd_lable = ttk.Label(master=self.master, text="Укажите скорость передачи:")
        self.port_spd_lable.grid(row=1, column=0, sticky=tk.W, padx=10, pady=4)
        self.port_spd_entity = ttk.Entry(master=self.master)
        self.port_spd_entity.grid(row=1, column=1, sticky=tk.W+tk.E, padx=10)

        # Кнопка подключения
        self.connect_btn = ttk.Button(self.master, text="Подключиться", command=self.connect())
        self.connect_btn.grid(row=3, columnspan=3, column=0, sticky=tk.E, padx=10, pady=4)

    #Функция подключения к порту (ТОДУ)
    def connect(self):
        try:
            self.connection = serial.Serial(self.port_list.current(), baudrate=self.port_spd_entity.get(), timeout=1)
        except ValueError:
            print("не удалось подключиться: порт не найден")
        else:
            print(self.connection)

    # Легаси
    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.print_port
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    # Легаси
    def say_hi(self):
        print("hi there, everyone!")

    # Легаси
    def print_port(self):
        print(self.connection)

# Начало программы
root1 = tk.Tk()
root2 = tk.Tk()
root1.geometry('350x350')
root2.geometry('350x350')

app1 = Application(master=root1,
                   title="Станция 1")

app2 = Application(master=root2,
                   title="Станция 2")

app1.mainloop()

app2.mainloop()