from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class Window:

    def __init__(self, title, size='800x600'):
        super().__init__()
        self.root = Tk()
        self.title = self.root.title(title)
        self.geometry = self.root.geometry(size)
        self.interactive_widgets = None
        self.clear_interactive_widgets()

    def mainloop(self):
        self.root.mainloop()

    def clear_interactive_widgets(self):
        self.interactive_widgets = dict()
        self.interactive_widgets['inputs'] = dict()
        self.interactive_widgets['outputs'] = dict()

    def clear_window(self):
        self.clear_interactive_widgets()
        for slave in self.root.winfo_children():
            slave.destroy()

    def make_default_frames(self, label):
        Label(self.root, text=label, font=('Arial Bold', 18)).pack(pady=15)
        Button(self.root, text='Главное меню', font=("Arial Bold", 10), command=self.load_window_menu)\
            .place(anchor=NE, relx=1, x=-15, y=15)

        left_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
        left_frame.place(relheight=1, relwidth=0.7, rely=0.1)

        right_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
        right_frame.place(relheight=1, relwidth=0.3, rely=0.1, relx=0.7)

        return left_frame, right_frame

    def add_output_block(self, master_widget, pack_side=TOP):
        txt_window = ScrolledText(master_widget, height=20, state='disabled')
        txt_window.pack(fill=X, side=pack_side)
        self.interactive_widgets['outputs']['scrolled_window'] = txt_window
        Button(master_widget, text='Очистить окно вывода', font=("Arial Bold", 10)).pack(pady=10, side=pack_side)

    def add_input_block(self, master_widget, input_labels, pack_side=TOP):
        for label in input_labels:
            frame = ttk.Frame(master_widget, borderwidth=1, padding=[4, 5])
            frame.pack(fill=X, side=pack_side)
            Label(frame, text=label, font=('Arial Bold', 10)).pack(side=LEFT)
            entry = Entry(frame, width=10, justify='center')
            entry.pack(side=LEFT)
            self.interactive_widgets['inputs'][label] = entry

    def add_buttons_block(self, master_widget, button_data, pack_side=TOP):
        for key in button_data:
            frame = ttk.Frame(master_widget, borderwidth=1, padding=[4, 5])
            frame.pack(fill=X, side=pack_side)
            Button(frame, text=key, font=("Arial Bold", 10), command=button_data[key]).pack(side=LEFT)

    def add_combobox(self, master_widget, label, values, pack_side=TOP):
        frame = ttk.Frame(master_widget, borderwidth=1, padding=[8, 10])
        frame.pack(fill=X, side=pack_side)
        Label(frame, text=label, font=('Arial Bold', 10)).pack(side=LEFT)
        combo = ttk.Combobox(frame)
        combo['values'] = values
        combo.current(0)
        combo.pack(side=LEFT)
        self.interactive_widgets['inputs'][label] = combo

    def add_empty_space(self, master_widget, amount, pack_side=TOP):
        Label(master_widget, text="", font=('Arial Bold', 10)).pack(pady=amount, side=pack_side)

