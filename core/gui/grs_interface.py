import tkinter
from tkinter import scrolledtext
from tkinter.ttk import Combobox


class Window:
    def __init__(self, title, inputs, size='800x600', txtwin=[50, 20]):
        labels = inputs
        self.root = tkinter.Tk()
        self.title = self.root.title(title)
        self.geometry = self.root.geometry(size)

        self.combo = tkinter.ttk.Combobox(self.root)
        self.combo.pack()

        self.labels = list(tkinter.Label(self.root, text=lbl, font=('Arial Bold', 14)) for lbl in labels)
        self.entries = list(tkinter.Entry(self.root, width=len(_)) for _ in labels)
        for i in range(len(self.labels)):
            self.labels[i].pack()
            self.entries[i].pack()
        txtwin = scrolledtext.ScrolledText(self.root, width=txtwin[0], height=txtwin[1], bg="darkgreen", fg='white')
        txtwin.pack()
        self.button = tkinter.Button(self.root, text='Нажми', command=self.get_data)
        self.button.pack()

    def mainloop(self):
        self.mainloop = self.root.mainloop()

    def get_data(self):
        print([data.get() for data in self.entries])
        return [data.get() for data in self.entries]

odorant_input = ('Вместимость ёмкости', 'Расход газа, ст. м3/ч', 'Комментарий')

odorant_window = Window(title='Расчёт ёмкости одоранта', size='800x600', inputs=odorant_input)
odorant_window.mainloop()

valve_input = ('Давление, МПа', 'Температура, °С', 'Расход, ст м3/ч', 'Диаметр трубопровода, мм', 'Толщина стенки, мм')

valve_window = Window(title='Расчёт скорости в трубопроводах', size='1920x1080', inputs=valve_input)
valve_window.mainloop()


