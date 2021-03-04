import tkinter as tk
import serial

class Application(tk.Frame):
    def __init__(self, master=None, port=None, baudrate=None, timeout=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.port_connect()


    def set_layout(self):
        self.master.tk.geometry('350x350')
        print("tbc")

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.print_port
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def print_port(self):
        print(self.connection)


    def port_connect(self):
        if self.port != None and self.baudrate != None and self.timeout != None:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        else:
            print("connection failed")

root1 = tk.Tk()
root2 = tk.Tk()
app = Application(master=root1, port="COM3", baudrate=9600, timeout=1)

app1 = Application(master=root2, port="COM4", baudrate=9600, timeout=1)

app.mainloop()

app1.mainloop()