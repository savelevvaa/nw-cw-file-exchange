import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import serial
import serial.tools.list_ports as port_list
import threading
import time

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
        self.port_spd_entity.insert(tk.END, "9600")
        self.port_spd_entity.grid(row=1, column=1, sticky=tk.W+tk.E, padx=10)

        # Кнопка подключения
        self.connect_btn = ttk.Button(self)
        self.connect_btn["text"] = "Подключиться"
        self.connect_btn["command"] = self.connect
        self.connect_btn.grid(row=3, columnspan=3, column=0, sticky=tk.E, padx=10, pady=4)

    # Функция подключения к порту
    def connect(self):
        try:
            self.connection = serial.Serial(port=self.port_list.get(), baudrate=int(self.port_spd_entity.get()), timeout=0.5)
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
        self.master.resizable(False, False)
        self.parent.master.withdraw()
        self.filename = tk.StringVar()
        self.filename.set("Файл не выбран")
        self.set_layout()
        self.files = dict()
        self.tr_in = threading.Thread(target=self.istream)
        self.tr_in.daemon = True
        self.tr_in.start()

    # Функция настройки элементов интерфейса
    def set_layout(self):
        # Лейба выбора файла
        self.file_lable = ttk.Label(self, text="Выбирите файл:")
        self.file_lable.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        # Кнопка выбора файла
        self.pick_file_btn = tk.Button(self, text="Обзор", command=self.pick_file, fg='blue')
        self.pick_file_btn.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)

        # Лейба названия файла
        self.file_name_lable = ttk.Label(self, text=self.filename.get())
        self.file_name_lable.grid(row=0, column=2, sticky=tk.W, padx=10, pady=10)

        # Кнопка отключения
        self.disconnect_btn = tk.Button(self, text="Отключиться", command=self.disconnect, fg='red')
        self.disconnect_btn.grid(row=0, column=3, sticky=tk.E, padx=10, pady=10)

        # Кнопка отправки файла
        self.send_file_btn = tk.Button(self, text="Отправить", command=self.send_file, fg='green')
        self.send_file_btn.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

        # Разделитель
        self.separator = tk.ttk.Separator(self)
        self.separator.grid(row=2, column=0, columnspan=4, sticky=tk.W+tk.E)

        # Лейба получения файла
        self.file_recieved_lable = tk.Label(self, text="Получено файлов: 0", fg='red')
        self.file_recieved_lable.grid(row=3, column=2, sticky=tk.E, padx=10, pady=10)

        # Кнопка сохранения файла
        self.save_file_btn = tk.ttk.Button(self, text="Сохранить", command=self.save_file, state="disabled")
        self.save_file_btn.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)

        # Выпадающий список полученных файлов
        self.files_list = ttk.Combobox(self)
        self.files_list.grid(row=3, column=3, sticky=tk.W, padx=10, pady=10)

    # Функция выбора файла
    def pick_file(self):
        # сохраняем путь до файла
        self.pwd = fd.askopenfilename()
        if self.pwd == '':
            return
        # вынимаем название файла
        self.temp = self.pwd.split('/')
        self.filename.set(self.temp[-1])
        # устанавливаем название выбранного фала лейбе
        self.file_name_lable.config(text=self.filename.get())

    # Функция чтения файла
    def read_file(self):
        self.f_bin = open(self.pwd, 'rb').read()

    # Функция отправки файла
    def send_file(self):
        self.read_file()
        data_str = self.f_bin
        if len(data_str) > 0:
            name = self.filename.get().encode()
            out_str = name + b'\n' + data_str
            self.parent.connection.write(out_str)

    # Функция сохранения файла
    def save_file(self):
        text2save = ""
        # типы файлов (на сохранении)
        filestypes = [('Text Document', '*.txt'),
                      ('Python Files', '*.py'),
                      ('All Files', '*.*')]
        # получаем имя файла для сохранения
        file_name = self.files_list.get()
        if file_name == "":
            return
        # получаем содержимое файла
        self.in_list = self.files[file_name]
        for line in self.in_list:
            text2save += line.decode()
        # вызываем диалог сохранения файла
        self.save = fd.asksaveasfile(mode='w', filetypes=filestypes, defaultextension=filestypes)
        if self.save is None:
            return
        self.save.write(text2save.replace('\r',''))
        self.save.close()

    # Функция отключения
    def disconnect(self):
        # закрываем подключение к com порту
        self.parent.connection.close()
        # проявляем родительское окно
        self.parent.master.deiconify()
        # закрываем текущее окно
        self.master.destroy()

    # Потоковая функция на прием из com-порта
    def istream(self):
        in_str = ""
        while 1:
            # ждем прихода к нам строки
            in_len = 0
            while in_len < 1:
                # читаем из порта
                in_str = self.parent.connection.readlines()
                in_len = len(in_str)
                if in_len > 1:
                    # получаем имя файла
                    bin_file_name = in_str.pop(0)
                    self.recieved_file_name = bin_file_name.decode().replace('\n','')
                    # заполняем словарь { имя файла : содержание (байты) }
                    self.files[self.recieved_file_name] = in_str

            if self.files.__len__() > 0:
                # разблокируем кнопку сохранения
                self.save_file_btn.config(state="enable")
                # обновляем лейбу
                self.file_recieved_lable.config(text="Получено файлов: " + str(self.files.__len__()))
                self.file_recieved_lable.config(fg="green")
                # получаем списко ключей (получаем имена файлов)
                keys = []
                for key in sorted(self.files.keys()):
                    keys.append(key)
                # обновляем выпадающий список полученных файлов
                self.files_list.config(values=keys)


# Функция вывода ошибок в консоль
def errHandler(e = None):
    print(f"\033[31mExcepted Error Description:\033[0m\n{e}")

# Главные окна
root1 = tk.Tk()
root2 = tk.Tk()

# Начало программы
if __name__ == '__main__':
    root1.geometry(f'350x100+{int(root1.winfo_screenwidth()/2)-400}-{int(root1.winfo_screenheight()/2)}')
    root2.geometry(f'350x100+{int(root1.winfo_screenwidth()/2)}-{int(root1.winfo_screenheight()/2)}')
    app1 = Connection(master=root1, title="Станция 1")
    app2 = Connection(master=root2, title="Станция 2")
    app1.mainloop()
    app2.mainloop()



# # Потоковая функция на прием из com-порта
#     # TODO: Переделать логику работы на словарях (для получения множества файлов)
#     def istream(self):
#         in_str = ""
#         flag = False
#         while 1:
#             # ждем прихода к нам строки
#             in_len = 0
#             while in_len < 1:
#                 in_str = self.parent.connection.readline()
#                 in_len = len(in_str)
#                 # устанавливаем название полученного файла лейбе
#                 if self.in_list.__len__() > 1 and flag == False:
#                     bin_file_name = self.in_list[0]
#                     self.recieved_file_name = bin_file_name.decode()
#                     self.file_recieved_lable.config(text="Получен файл: " + self.recieved_file_name)
#                     self.file_recieved_lable.config(fg="green")
#                     self.in_list.pop(0)
#                     flag = True
#
#             # ждем освобождение входного буфера и записываем в него строку
#             self.in_list.append(in_str)
#             if self.in_list.__len__() > 1:
#                 self.save_file_btn.config(state="enable")