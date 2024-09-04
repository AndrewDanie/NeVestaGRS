from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt

from core.view.IView import IView


class LabeledWidget:

    def __init__(self, interactive_widget, label_widget=None):
        self.widget = interactive_widget
        self.label = label_widget

    def set_label(self, text):
        if self.label is not None:
            self.label.configure(text=text)


class Window(IView):

    EMPTY_WIDGET_LIST = {
        'input': {},
        'button': {},
        'output': {},
        'plot': {},
    }

    def __init__(self, title, size='800x600', ):
        self.root = Tk()
        self.title = self.root.title(title)
        self.geometry = self.root.geometry(size)
        self.widgets = Window.EMPTY_WIDGET_LIST

    def mainloop(self):
        self.root.mainloop()

    def clear_screen(self):
        self.widgets = Window.EMPTY_WIDGET_LIST
        for slave in self.root.winfo_children():
            slave.destroy()

    def clear_output_window(self):
        output_txt_field = self.widgets['output']['__txt_field__']
        output_txt_field.configure(state='normal')
        output_txt_field.delete(1.0, END)
        output_txt_field.configure(state='disable')

    def get_widget(self, parameter_path):
        path = parameter_path.split('.')
        folder = self.widgets
        for elem in path:
            try:
                folder = folder[elem]
            except:
                raise Exception('Неверный путь к виджету!')

        widget = folder
        return widget

    def get_data(self, parameter_path : str):
        widget = self.get_widget(parameter_path)
        return widget.get()

    def set_data(self, parameter_path, output_entity):
        widget = self.get_widget(parameter_path)
        widget.configure(state='normal')
        for name in output_entity:
            widget.insert(INSERT, name + ' = ' + str(output_entity[name]) + '\n')
        widget.configure(state='disable')


class TkScreenBuilder:
    """
    Строитель графического интерфейса
    Единственный класс, который должен иметь доступ к созданию объектов Tkinter'а
    """
    def __init__(self, window):
        self.window = window
        self.root = window.root
        self.widgets = window.widgets

    def set_window(self, window):
        self.window = window
        self.root = window.root
        self.widgets = window.widgets

    def make_default_frames(self, label):
        lbl = Label(self.root, text=label, font=('Arial Bold', 18))
        lbl.pack(pady=15)
        main_menu_button = Button(self.root,
               name='to_main_menu_button',
               text='Главное меню', font=("Arial Bold", 10))
        main_menu_button.place(anchor=NE, relx=1, x=-15, y=15)
        left_frame = ttk.Frame(master=self.root,
                               name='left_frame',
                               borderwidth=1, relief=SOLID, padding=[8, 10])
        left_frame.place(relheight=1, relwidth=0.7, rely=0.1)
        right_frame = ttk.Frame(master=self.root,
                                name='right_frame',
                                borderwidth=1, relief=SOLID, padding=[8, 10])
        right_frame.place(relheight=1, relwidth=0.3, rely=0.1, relx=0.7)
        self.widgets['button']['__to_main_menu__'] = main_menu_button

    def add_output_block(self, master_widget, pack_side=TOP):
        """
        Добавляет блок вывода, состоящий из текстового поля вывода и кнопки очистки этого поля
        """
        output_txt_field = ScrolledText(master_widget,
                                  height=20, state='disabled')
        output_txt_field.pack(fill=X, side=pack_side)
        self.widgets['output']['__txt_field__'] = LabeledWidget(output_txt_field)
        Button(master_widget,
               text='Очистить окно вывода',
               font=("Arial Bold", 10),
               command=self.window.clear_output_window).pack(pady=10, side=pack_side)

    def add_input_block(self, master_widget, input_data, pack_side=TOP):
        """
        Добавляет блок ввода, состоящий из текстовых полей ввода
        """
        for label in input_data:
            frame = ttk.Frame(master_widget,
                              borderwidth=1, padding=[4, 5])
            frame.pack(fill=X, side=pack_side)
            lbl_text = label
            lbl = Label(frame, text=lbl_text, font=('Arial Bold', 10))
            lbl.pack(side=LEFT)
            entry = Entry(master=frame,
                          width=10, justify='center')
            entry.pack(side=LEFT)
            self.widgets['input'][label] = LabeledWidget(entry, lbl)

    def add_buttons_block(self, master_widget, button_data, pack_side=TOP):
        """
        Добавляет блок кнопок, рассчитывающих параметры
        """
        for label in button_data:
            frame = ttk.Frame(master=master_widget,
                              borderwidth=1, padding=[4, 5])
            frame.pack(fill=X, side=pack_side)
            button = Button(master=frame, font=("Arial Bold", 10))
            button.pack(side=LEFT)
            self.widgets['button'][label] = button

    def add_combobox_block(self, master_widget, combobox_config, pack_side=TOP):
        """
        Добавляет блок ввода, состоящий из комбобоксов
        """
        for label in combobox_config:
            frame = ttk.Frame(master=master_widget,
                              borderwidth=1, padding=[8, 10])
            frame.pack(fill=X, side=pack_side)
            lbl_text = label
            lbl = Label(frame, text=lbl_text, font=('Arial Bold', 10))
            lbl.pack(side=LEFT)
            combo = ttk.Combobox(frame, name=label)
            combo.pack(side=LEFT)
            self.widgets['input'][label] = LabeledWidget(combo, lbl)

    def add_empty_space(self, master_widget, amount=30, pack_side=TOP):
        """
        Добавляет блок пустоты, заданный по amount
        """
        Label(master_widget, text="", font=('Arial Bold', 10)).pack(pady=amount, side=pack_side)

    def add_plot_example(self, master_widget):
        """
        Добавляет демонстрационный график mathplotlib'а
        """
        from matplotlib.figure import Figure

        fig = Figure(figsize=(5, 5), dpi=100)
        y = [i ** 2 for i in range(101)]
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plot1 = fig.add_subplot(111)

        # plot1.plot(y)
        canvas = FigureCanvasTkAgg(fig, master=master_widget)
        # plt.show()
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.widgets['plot']['plot'] = plot1
        self.widgets['plot']['canvas'] = canvas

    def build_default_calculator(self, window_name, screen_config):
        self.window.clear_screen()
        self.make_default_frames(window_name)
        right_frame = self.root.nametowidget("right_frame")
        left_frame = self.root.nametowidget("left_frame")
        self.add_output_block(left_frame)
        widgets = screen_config['widgets']
        if 'combobox' in widgets:
            self.add_combobox_block(right_frame, widgets['combobox'])
        if 'entry' in widgets:
            self.add_input_block(right_frame, widgets['entry'])
        self.add_empty_space(right_frame, pack_side=BOTTOM)
        if 'button' in widgets:
            self.add_buttons_block(right_frame, widgets['button'],pack_side=BOTTOM)

    def build_main_menu(self, screen_config):
        self.window.clear_screen()
        Label(self.root, text='НеВеста-ГРС', font=('Arial Bold', 18)).place(relx=0.5, anchor=N, y=30)
        central_frame = ttk.Frame(self.root, borderwidth=1, padding=[4, 5])
        central_frame.pack(expand=True, anchor=CENTER)
        i = 0
        self.button_list = []
        for screen_name in screen_config:
            if screen_name == 'Главное меню':
                continue
            frame = ttk.Frame(central_frame, borderwidth=1, padding=[4, 5])
            frame.grid(row=i // 2, column=i % 2)
            button = Button(frame, text=screen_name, font=("Arial Bold", 10), width=30)
            button.pack()
            self.button_list.append(button)
            i += 1

    def build_plot_window(self, screen_config):
        self.window.clear_screen()
        self.make_default_frames('Статистика')
        right_frame = self.root.nametowidget("right_frame")
        widgets = screen_config['widgets']
        self.add_combobox_block(right_frame, widgets['combobox'])
        for i in range(1):
            frame = ttk.Frame(self.root.nametowidget("left_frame"), borderwidth=1, padding=[4, 5])
            frame.grid(row=i // 2, column=i % 2)
            self.add_plot_example(frame)
        self.add_empty_space(right_frame, pack_side=BOTTOM)
        if 'button' in widgets:
            self.add_buttons_block(right_frame, widgets['button'], pack_side=BOTTOM)
