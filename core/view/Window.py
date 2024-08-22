from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from core.model.functions.variables import cache_variable_dict


class Window:

    def __init__(self, title, size='800x600', ):
        self.root = Tk()
        self.title = self.root.title(title)
        self.geometry = self.root.geometry(size)

    def mainloop(self):
        self.root.mainloop()

    def clear_window(self):
        for slave in self.root.winfo_children():
            slave.destroy()

    def make_default_frames(self, label):
        Label(self.root, text=label, font=('Arial Bold', 18)).pack(pady=15)
        Button(self.root,
               name='to_main_menu_button',
               text='Главное меню', font=("Arial Bold", 10))\
            .place(anchor=NE, relx=1, x=-15, y=15)
        left_frame = ttk.Frame(master=self.root,
                               name='left_frame',
                               borderwidth=1, relief=SOLID, padding=[8, 10])
        left_frame.place(relheight=1, relwidth=0.7, rely=0.1)
        right_frame = ttk.Frame(master=self.root,
                                name='right_frame',
                                borderwidth=1, relief=SOLID, padding=[8, 10])
        right_frame.place(relheight=1, relwidth=0.3, rely=0.1, relx=0.7)

    def add_output_block(self, master_widget, pack_side=TOP):
        output_txt_field = ScrolledText(master_widget,
                                  name='output_txt_field',
                                  height=20, state='disabled')
        output_txt_field.pack(fill=X, side=pack_side)
        Button(master_widget,
               text='Очистить окно вывода',
               font=("Arial Bold", 10),
               command=self.clear_output_window).pack(pady=10, side=pack_side)

    def clear_output_window(self):
        output_txt_field = self.root.nametowidget('left_frame.!frame.output_txt_field')
        output_txt_field.configure(state='normal')
        output_txt_field.delete(1.0, END)
        output_txt_field.configure(state='disable')

    def add_input_block(self, master_widget, input_data, pack_side=TOP):
        for label in input_data:
            frame = ttk.Frame(master_widget,
                              name=f'{label}_input_wrapper',
                              borderwidth=1, padding=[4, 5])
            frame.pack(fill=X, side=pack_side)
            lbl_text = label[2:] if label[:2] == '__' else cache_variable_dict[label]
            Label(frame, text=lbl_text, font=('Arial Bold', 10)).pack(side=LEFT)
            entry = Entry(master=frame,
                          name=label,
                          width=10, justify='center')
            entry.pack(side=LEFT)

    def add_buttons_block(self, master_widget, button_data, pack_side=TOP):
        for button_name in button_data:
            frame = ttk.Frame(master=master_widget,
                              name=f'{button_name}_button_wrapper',
                              borderwidth=1, padding=[4, 5])
            frame.pack(fill=X, side=pack_side)
            lbl_text = button_name
            button = Button(master=frame,
                name=button_name,
                text=lbl_text,
                font=("Arial Bold", 10),
            )
            button.pack(side=LEFT)

    def add_combobox(self, master_widget, combobox_data, values, pack_side=TOP):
        for combobox_name in combobox_data:
            frame = ttk.Frame(master=master_widget,
                              name=f'{combobox_name}_input_wrapper',
                              borderwidth=1, padding=[8, 10])
            frame.pack(fill=X, side=pack_side)
            lbl_text = combobox_name[2:] if combobox_name[:2] == '__' else cache_variable_dict[combobox_name]
            Label(frame, text=lbl_text, font=('Arial Bold', 10)).pack(side=LEFT)
            combo = ttk.Combobox(frame, name=combobox_name)
            combo['values'] = values
            combo.current(0)
            combo.pack(side=LEFT)

    def add_empty_space(self, master_widget, amount=30, pack_side=TOP):
        Label(master_widget, text="", font=('Arial Bold', 10)).pack(pady=amount, side=pack_side)

    def build_default_calculator(self, window_name, window_data):
        self.clear_window()
        self.make_default_frames(window_name)
        right_frame = self.root.nametowidget("right_frame")
        left_frame = self.root.nametowidget("left_frame")
        self.add_output_block(left_frame)
        widgets = window_data['widgets']
        if 'combobox' in widgets:
            self.add_combobox(right_frame, widgets['combobox'], [1, 2, 3])
        if 'entry' in widgets:
            self.add_input_block(right_frame, widgets['entry'])
        self.add_empty_space(right_frame, pack_side=BOTTOM)
        if 'button' in widgets:
            self.add_buttons_block(right_frame, widgets['button'],pack_side=BOTTOM)

    def build_window_menu(self, properties):
        # Главное меню
        self.clear_window()
        Label(self.root, text='НеВеста-ГРС', font=('Arial Bold', 18)).place(relx=0.5, anchor=N, y=30)
        central_frame = ttk.Frame(self.root, borderwidth=1, padding=[4, 5])
        central_frame.pack(expand=True, anchor=CENTER)
        i = 0
        self.button_list = []
        for window_name in properties:
            frame = ttk.Frame(central_frame, borderwidth=1, padding=[4, 5])
            frame.grid(row=i // 2, column=i % 2)
            button = Button(frame, text=window_name, font=("Arial Bold", 10), width=30)
            button.pack()
            self.button_list.append(button)
            i += 1
