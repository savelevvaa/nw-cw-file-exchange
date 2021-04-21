from layout.windows import tk, Connection

# Главные окна
root1 = tk.Tk()
root2 = tk.Tk()

# Начало программы
if __name__ == '__main__':
    root1.geometry(f'350x237+{int(root1.winfo_screenwidth()/2)-400}-{int(root1.winfo_screenheight()/2)}')
    root2.geometry(f'350x237+{int(root1.winfo_screenwidth()/2)}-{int(root1.winfo_screenheight()/2)}')
    app1 = Connection(master=root1, title="Станция 1")
    app2 = Connection(master=root2, title="Станция 2")
    app1.mainloop()
    app2.mainloop()
