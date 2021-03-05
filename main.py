import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import serial
import serial.tools.list_ports as port_list

class Connection(tk.Frame):
    # Конструктор
    def __init__(self, master=None, title=None):
        super().__init__(master)
        self.pack()
        self.master = master
        self.master.title(title)
        self.master.resizable(False, False)
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
        self.port_list_lable = ttk.Label(self, text="Выбирите доступный порт:")
        self.port_list_lable.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.port_list = ttk.Combobox(self, values=ports)
        self.port_list.grid(row=0, column=1, sticky=tk.W+tk.E, padx=10)

        # Лейба и строка для ввода скорости работы порта
        self.port_spd_lable = ttk.Label(self, text="Укажите скорость передачи:")
        self.port_spd_lable.grid(row=1, column=0, sticky=tk.W, padx=10, pady=4)
        self.port_spd_entity = ttk.Entry(self)
        self.port_spd_entity.grid(row=1, column=1, sticky=tk.W+tk.E, padx=10)

        # Кнопка подключения
        self.connect_btn = ttk.Button(self)
        self.connect_btn["text"] = "Подключиться"
        self.connect_btn["command"] = self.connect
        self.connect_btn.grid(row=3, columnspan=3, column=0, sticky=tk.E, padx=10, pady=4)

    # Функция подключения к порту
    def connect(self):
        try:
            self.connection = serial.Serial(self.port_list.get(), baudrate=int(self.port_spd_entity.get()), timeout=1)
        except ValueError as e:
            errHandler(e)
        except serial.SerialException as e:
            errHandler(e)
        else:
            print(self.connection)
            # Сохраняем порт и вызываем дочернее окно
            self.portVar = tk.StringVar()
            self.portVar.set(self.port_list.get())
            Connected(master=tk.Toplevel(), parent=self)

# Дочернее окно (после совершения подключения)
class Connected(tk.ttk.Frame):
    # Конструктор
    def __init__(self, master=None, parent = None):
        super().__init__(master)
        self.parent = parent
        self.pack()
        self.master.title(self.parent.master.title()+f" ({self.parent.portVar.get()})")
        self.master.geometry('550x550')
        self.master.resizable(False, False)
        self.parent.master.withdraw()
        self.filename = tk.StringVar()
        self.filename.set("Файл не выбран")
        self.set_layout()

    # Функция настройки элементов интерфейса
    def set_layout(self):
        # Лейба выбора файла
        self.file_lable = ttk.Label(self, text="Выбирите файл:")
        self.file_lable.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        # Кнопка отключения
        self.disconnect_btn = tk.ttk.Button(self, text = "Отключиться", command = self.disconnect)
        self.disconnect_btn.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)

        # Кнопка выбора файла
        self.pick_file_btn = tk.ttk.Button(self, text="Обзор", command=self.pick_file)
        self.pick_file_btn.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

        # Лейба названия файла
        self.file_name_lable = ttk.Label(self, text=self.filename.get())
        self.file_name_lable.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

    # Функция выбора файла
    def pick_file(self):
        # сохраняем путь до файла
        self.pwd = fd.askopenfilename()
        # вынимаем название файла
        self.temp = self.pwd.split('/')
        self.filename.set(self.temp[-1])
        # устанавливаем название выбранного фала лейбе
        self.file_name_lable.config(text=self.filename.get())

    def disconnect(self):
        # закрываем подключение к com порту
        self.parent.connection.close()
        # проявляем родительское окно
        self.parent.master.deiconify()
        # закрываем текущее окно
        self.master.destroy()

# Функция вывода ошибок в консоль
def errHandler(e = None):
    print(f"\033[31mExcepted Error Description:\033[0m\n{e}")

# Главные окна
root1 = tk.Tk()
root2 = tk.Tk()

# Начало программы
if __name__ == '__main__':
    root1.geometry(f'350x100+{int(root1.winfo_screenwidth()/2)-100}-{int(root1.winfo_screenheight()/2)+50}')
    root2.geometry(f'350x100+{int(root1.winfo_screenwidth()/2)}-{int(root1.winfo_screenheight()/2)}')
    app1 = Connection(master=root1, title="Станция 1")
    app2 = Connection(master=root2, title="Станция 2")
    app1.mainloop()
    app2.mainloop()