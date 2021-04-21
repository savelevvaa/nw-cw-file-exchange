import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as msb
import serial
import serial.tools.list_ports as port_list
import threading
import time
from network.frame import *
from network.coding import *
from network.networkmanager import NetworkManager


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
            ports.append(str(port).split()[0])

        # Лейба и строка для ввода Пользователя
        self.user_lable = ttk.Label(self, text="Пользователь")
        self.user_lable.grid(row=0, column=0, sticky=tk.W, padx=10, pady=14)
        self.user_entity = ttk.Entry(self)
        self.user_entity.insert(tk.END, "pc1")
        self.user_entity.grid(row=0, column=1, sticky=tk.W + tk.E, padx=10)

        # Разделитель
        self.separator = tk.ttk.Separator(self)
        self.separator.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)

        # Лейба и список портов
        self.port_list_lable = ttk.Label(self, text="Выбирите доступный порт:")
        self.port_list_lable.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.port_list = ttk.Combobox(self, values=ports)
        self.port_list.grid(row=2, column=1, sticky=tk.W+tk.E, padx=10)

        # Лейба и строка для ввода скорости работы порта
        self.port_spd_lable = ttk.Label(self, text="Скорость:")
        self.port_spd_lable.grid(row=3, column=0, sticky=tk.W, padx=10, pady=4)
        self.port_spd_entity = ttk.Entry(self)
        self.port_spd_entity.insert(tk.END, "9600")
        self.port_spd_entity.grid(row=3, column=1, sticky=tk.W+tk.E, padx=10)

        # Лейба и строка для ввода битов данных
        self.bytesize_lable = ttk.Label(self, text="Биты данных:")
        self.bytesize_lable.grid(row=4, column=0, sticky=tk.W, padx=10, pady=4)
        self.bytesize_entity = ttk.Entry(self)
        self.bytesize_entity.insert(tk.END, "8")
        self.bytesize_entity.grid(row=4, column=1, sticky=tk.W + tk.E, padx=10)

        # Лейба и строка для ввода стоп-битов
        self.stopbit_lable = ttk.Label(self, text="Стоп-биты:")
        self.stopbit_lable.grid(row=5, column=0, sticky=tk.W, padx=10, pady=4)
        self.stopbit_entity = ttk.Entry(self)
        self.stopbit_entity.insert(tk.END, "1")
        self.stopbit_entity.grid(row=5, column=1, sticky=tk.W + tk.E, padx=10)

        # Лейба и строка для ввода таймаута
        self.timeout_lable = ttk.Label(self, text="Таймаут:")
        self.timeout_lable.grid(row=6, column=0, sticky=tk.W, padx=10, pady=4)
        self.timeout_entity = ttk.Entry(self)
        self.timeout_entity.insert(tk.END, "0.5")
        self.timeout_entity.grid(row=6, column=1, sticky=tk.W + tk.E, padx=10)

        # Кнопка подключения
        self.connect_btn = ttk.Button(self)
        self.connect_btn["text"] = "Подключиться"
        self.connect_btn["command"] = self.connect
        self.connect_btn.grid(row=8, columnspan=3, column=0, sticky=tk.E, padx=10, pady=4)

    # Функция подключения к порту
    def connect(self):
        try:
            self.nm = NetworkManager(port=self.port_list.get(),
                                     baudrate=int(self.port_spd_entity.get()),
                                     bytesize=int(self.bytesize_entity.get()),
                                     stopbits=int(self.stopbit_entity.get()),
                                     timeout=float(self.timeout_entity.get()),
                                     username=self.user_entity.get())

        except serial.SerialException as e:
            msb.showwarning(title="Ошибка подключения", message="Укажите иной порт")
            errHandler(e)
            return
        else:
            print(self.nm.connection)
            for user in sessions.keys():
                if user == self.nm.session.username:
                    msb.showwarning(title="Ошибка подключения", message="Укажите иное имя пользователя")
                    return
            sessions[self.nm.session.username] = self.nm.session.con
            Connected(master=tk.Toplevel(),
                      parent=self,
                      session=self.nm.session)

# Дочернее окно (после совершения подключения)
class Connected(tk.ttk.Frame):
    # Конструктор
    def __init__(self, master=None, parent = None, session=None):
        # База
        super().__init__(master)
        self.parent = parent
        self.pack()
        self.session = session
        self.master.title(self.parent.master.title()+
                          f" ({self.session.username}, "
                          f"{self.session.con.port}, "
                          f"{self.session.con.baudrate})")
        self.master.resizable(False, False)
        self.parent.master.withdraw()

        # Переменные
        self.filename = "Файл не выбран"
        self.pwd = ""
        self.files = dict()
        self.LINKED = False

        # Методы
        self.set_layout()
        self.parent.nm.send_control_bytes(Frame.Type.LINK)

        # Потоки
        self.tr_in = threading.Thread(target=self.istream)
        self.tr_in.daemon = True
        self.tr_in.start()

        self.tr_users = threading.Thread(target=self.users)
        self.tr_users.daemon = True
        self.tr_users.start()

    # Функция настройки элементов интерфейса
    def set_layout(self):

        # Фрейм для лейбы и пользователей
        self.entryFrame = tk.Frame(self, width=130)
        self.entryFrame.grid(row=0, rowspan=5, column=4)

        # Лейба пользователей
        self.session_lable = ttk.Label(self.entryFrame, text="Пользователи:")
        self.session_lable.grid(row=0, column=0, sticky=tk.W, padx=10, pady=6)

        # Текстбокс для пользователей
        self.textbox = tk.Text(self.entryFrame, height=8, width=13)
        self.textbox.grid(row=1, column=0, padx=10, pady=6)

        # Лейба выбора файла
        self.file_lable = ttk.Label(self, text="Выбирите файл:")
        self.file_lable.grid(row=0, column=0, sticky=tk.W, padx=10, pady=6)

        # Кнопка выбора файла
        self.pick_file_btn = tk.Button(self, text="Обзор", command=self.pick_file, fg='blue')
        self.pick_file_btn.grid(row=0, column=1, sticky=tk.W, padx=10, pady=6)

        # Лейба названия файла
        self.file_name_lable = ttk.Label(self, text=self.filename)
        self.file_name_lable.grid(row=0, column=2, sticky=tk.W, padx=10, pady=6)

        # Кнопка отключения
        self.disconnect_btn = tk.Button(self, text="Отключиться", command=self.disconnect, fg='red')
        self.disconnect_btn.grid(row=0, column=3, sticky=tk.E, padx=10, pady=6)

        # Кнопка просмотра файла
        self.show_file_btn = tk.Button(self, text="Просмотр", command=self.show_file, state="disabled")
        self.show_file_btn.grid(row=2, column=1, sticky=tk.W, padx=10, pady=6)

        # Кнопка отправки файла
        self.send_file_btn = tk.Button(self, text="Отправить", command=self.send_file, fg='green', state="disabled")
        self.send_file_btn.grid(row=2, column=0, sticky=tk.W, padx=10, pady=6)

        # Лейба логического соединения
        self.logic_con_lable = ttk.Label(self, text="Логическое соединение: не установлено")
        self.logic_con_lable.grid(row=1, column=0, columnspan=4, sticky=tk.W, padx=10, pady=6)

        # Разделитель
        self.separator = tk.ttk.Separator(self)
        self.separator.grid(row=3, column=0, columnspan=4, sticky=tk.W+tk.E)

        # Лейба получения файла
        self.file_recieved_lable = tk.Label(self, text="Получено файлов: 0", fg='red')
        self.file_recieved_lable.grid(row=4, column=2, sticky=tk.E, padx=10, pady=6)

        # Кнопка сохранения файла
        self.save_file_btn = tk.ttk.Button(self, text="Сохранить", command=self.save_file, state="disabled")
        self.save_file_btn.grid(row=4, column=0, sticky=tk.W, padx=10, pady=6)

        # Кнопка просмотра полученного файла
        self.show_recieved_file_btn = tk.ttk.Button(self, text="Просмотр", command=self.show_recieved_file, state="disabled")
        self.show_recieved_file_btn.grid(row=4, column=1, sticky=tk.W, padx=10, pady=6)

        # Выпадающий список полученных файлов
        self.files_list = ttk.Combobox(self)
        self.files_list.grid(row=4, column=3, sticky=tk.W, padx=10, pady=6)

    def send_frame(self, type):
        frame = Frame(type=type)
        self.parent.nm.connection.send_control_bytes(frame.data)


    def show_file(self):
        self.read_file()
        FileContent(master=tk.Toplevel(),
                    parent=self,
                    title=self.filename,
                    content=self.file_data_bin)

    def show_recieved_file(self):
        # получаем имя файла для просмотра
        file_name = self.files_list.get()
        if file_name == "":
            msb.showwarning(title="Внимание", message="Выбирите файл для просмотра")
            return
        content = self.files[file_name]
        FileContent(master=tk.Toplevel(),
                    parent=self,
                    title=file_name,
                    content=content)

    # Функция выбора файла
    def pick_file(self):
        # сохраняем путь до файла
        self.pwd = fd.askopenfilename()
        if self.pwd == '':
            return
        # вынимаем название файла
        self.filename = self.pwd.split('/')[-1]
        # устанавливаем название выбранного файла лейбе
        self.file_name_lable.config(text=self.filename)
        self.show_file_btn.config(state="normal")

    # Функция чтения файла
    def read_file(self):
        self.file_data_bin = open(self.pwd, 'rb').read()

    # Функция отправки файла
    def send_file(self):
        if self.pwd == "":
            msb.showwarning(title="Внимание", message="Выбирите файл")
            return
        else:
            self.read_file()
        if len(self.file_data_bin) > 0:
            name = self.filename.encode()
            out_str = name + b'\n' + self.file_data_bin
            self.parent.nm.send_bytes(out_str)

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
            msb.showwarning(title="Внимание", message="Выбирите файл для сохранения")
            return
        # получаем содержимое файла
        text2save = self.files[file_name].decode()
        # вызываем диалог сохранения файла
        self.save = fd.asksaveasfile(mode='w', filetypes=filestypes, defaultextension=filestypes)
        if self.save is None:
            return
        self.save.write(text2save.replace('\r',''))
        self.save.close()

    # Функция отключения
    def disconnect(self):
        # разрываем логическое соединение
        self.parent.nm.send_control_bytes(Frame.Type.DOWNLINK)
        # закрываем сессию
        sessions.pop(self.parent.nm.session.username)
        # закрываем подключение к com порту
        self.parent.nm.connection.close()
        # проявляем родительское окно
        self.parent.master.deiconify()
        # закрываем текущее окно
        self.master.destroy()

    # Потоковая функция на прием из com-порта
    def istream(self):
        while 1:
            # ждем прихода к нам строки
            in_len = 0
            while in_len < 1:
                # читаем из порта
                in_list = self.parent.nm.read_bytes()
                in_len = len(in_list)
                # если чтото прочитали, то обрабатываем
                if in_len > 0:
                    # читаем тип фрейма
                    frame_type = in_list.pop(0).replace(b'\n', b'')
                    # ОБРАБАТЫВАЕМ ПОЛУЧЕННЫЙ ФРЕЙМ (по типу)
                    if frame_type == Frame.Type.LINK.value and self.LINKED == False:
                        print(f'( {self.parent.nm.session.username} ) : '+'\033[33mLINK frame recieved\033[0m')
                        # устанавливаем логическую связ
                        self.LINKED = True
                        self.logic_con_lable.config(text="Логическое соединение: установлено")
                        self.send_file_btn.config(state="normal")
                        # отправляем такой же фрейм в ответ на полученный
                        self.parent.nm.send_control_bytes(Frame.Type.LINK)
                    # TODO обработка ASK фрейма
                    elif frame_type == Frame.Type.ASK.value:
                        print(f'( {self.parent.nm.session.username} ) : ' + '\033[33mASK frame recieved\033[0m')
                    # TODO обработка REP фрейма
                    elif frame_type == Frame.Type.REP.value:
                        print(f'( {self.parent.nm.session.username} ) : ' + '\033[33mREP frame recieved\033[0m')
                    elif frame_type == Frame.Type.DATA.value:
                        print(f'( {self.parent.nm.session.username} ) : ' + '\033[33mDATA frame recieved\033[0m')
                        income_data = b''
                        # декодируем полученные данные
                        for byte in in_list:
                            income_data += decoding(byte)
                        # получаем имя полученного файла
                        file_name = income_data.decode().split('\n')[0]
                        self.recieved_file_name = file_name
                        # удаляем имя файла из название файла
                        income_data = income_data.replace(file_name.encode()+b'\n', b'')
                        # заполняем словарь { имя файла : содержание (байты) }
                        self.files[self.recieved_file_name] = income_data
                    # TODO обработка ERROR фрейма
                    elif frame_type == Frame.Type.ERROR.value:
                        print(f'( {self.parent.nm.session.username} ) : ' + '\033[33mERROR frame recieved\033[0m')
                    elif frame_type == Frame.Type.DOWNLINK.value:
                        print(f'( {self.parent.nm.session.username} ) : ' + '\033[33mDOWNLINK frame recieved\033[0m')
                        # разрываем установленное соединение
                        self.LINKED = False
                        self.logic_con_lable.config(text="Логическое соединение: разорвано")
                        self.send_file_btn.config(state="disabled")

            if self.files.__len__() > 0:
                # разблокируем кнопку сохранения
                self.save_file_btn.config(state="enable")
                # разблокируем кнопку просмотра полученного файла
                self.show_recieved_file_btn.config(state="enable")
                # обновляем лейбу
                self.file_recieved_lable.config(text="Получено файлов: " + str(self.files.__len__()))
                self.file_recieved_lable.config(fg="green")
                # получаем списко ключей (получаем имена файлов)
                keys = []
                for key in sorted(self.files.keys()):
                    keys.append(key)
                # обновляем выпадающий список полученных файлов
                self.files_list.config(values=keys)

    # Потоковая функция обновления пользователей в списке
    def users(self):
        while 1:
            users = ""
            users_list = sessions.keys()
            for user in users_list:
                users += "* " + user + f" ({sessions[user].port})\n"
            self.textbox.config(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.INSERT, users)
            self.textbox.config(state=tk.DISABLED)
            time.sleep(1)

# Дочернее окно для отображения содержимого файла
class FileContent(tk.Frame):
    # Конструктор
    def __init__(self, master=None, parent=None, title=None, content=None):
        super().__init__(master)
        self.parent = parent
        self.pack()
        self.master = master
        self.master.title(title)
        self.master.resizable(False, False)
        self.content = content

        self.set_layout()

    def set_layout(self):
        # Лейба выбора файла
        self.lable = ttk.Label(self, text="Содержимое файла:")
        self.lable.grid(row=0, column=0, sticky=tk.W, padx=10, pady=6)

        # Текстбокс для содержимого файла
        self.textbox = tk.Text(self, height=20, width=60)
        self.textbox.grid(row=1, column=0, padx=10, pady=6)
        self.textbox.insert(tk.END, self.content.decode())
        self.textbox.config(state="disabled")



# Функция вывода ошибок в консоль
def errHandler(e = None):
    print(f"\033[31mExcepted Error Description:\033[0m\n{e}")

sessions = dict()