from copy import deepcopy
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt

from core.util.ConfigCache import ConfigCache
from core.view.callback import db
from core.view.callback.meta import get_yaml_callback
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
        'combobox': {},
        'entry': {},
        'button': {},
        'output': {},
        'plot': {},
    }

    def __init__(self, title, size='800x600', ):
        self.root = Tk()
        self.title = self.root.title(title)
        self.geometry = self.root.geometry(size)
        self.widgets = None
        self.clear_screen()

    def mainloop(self):
        self.root.mainloop()

    def clear_screen(self):
        self.widgets = deepcopy(Window.EMPTY_WIDGET_LIST)
        for slave in self.root.winfo_children():
            slave.destroy()

    def clear_output_window(self):
        output_txt_field = self.widgets['output']['__txt_field__']
        if isinstance(output_txt_field, LabeledWidget):
            output_txt_field = output_txt_field.widget
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
                raise Exception(f'Неверный путь к виджету! {parameter_path}')

        widget = folder
        return widget

    def get_data(self, parameter_path : str):
        widget = self.get_widget(parameter_path)
        if isinstance(widget, LabeledWidget):
            widget = widget.widget
        return widget.get()

    def set_data(self, parameter_path, output_entity):
        widget = self.get_widget(parameter_path)
        if isinstance(widget, LabeledWidget):
            widget = widget.widget
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
        self.binding_config = None

    def build_screen(self, screen_name, screen_config, binding_config):
        """
        Строит экран по конфигам из файлов binding_config.yml и template_config.yml
        """
        self.window.clear_screen()
        self.binding_config = binding_config
        widget_config = binding_config['widgets']

        if screen_config['frames'] == 'default':
            # Default frames
            for frame_name in screen_config:
                if frame_name == 'frames':
                    continue
                if frame_name == 'up_frame':
                    if screen_config['up_frame'] == 'default_top':
                        self.__make_default_screen(screen_name)
                else:
                    frame_widget = self.root.nametowidget(frame_name)
                    frame = screen_config[frame_name]
                    for elem in frame:
                        self.build_element(elem, frame_widget, frame, widget_config)

        elif screen_config['frames'] == 'one':
            frame = screen_config['one_frame']
            central_frame = ttk.Frame(self.root, borderwidth=1, padding=[4, 5])
            central_frame.pack(expand=True, anchor=CENTER)
            for elem in frame:
                self.build_element(elem, central_frame, frame, widget_config)

    def bind_widgets(self):
        """
        Связывает элементы интерфейса с остальными частями программы по конфигу из файла binding_config.yml
        """
        if self.binding_config is None:
            raise Exception('Экран не создан!')
        wgts = self.window.widgets
        if '__to_main_menu__' in wgts['button']:
            context = ConfigCache.get_cache().get('context')
            clback = lambda e, ctx=context: ctx.make_context('Главное меню')
            back_button = wgts['button']['__to_main_menu__']
            back_button.bind('<Button-1>', clback)

        widgets_config = self.binding_config['widgets']
        for block in widgets_config:
            block_config = widgets_config[block]
            if 'values' in block_config:
                # Автогенерация в конфиге
                call_set = get_yaml_callback(block_config['values'])()
                for call_data in call_set:
                    label = call_data[0]
                    callback = call_data[1]
                    curr_widget = wgts[block][label]
                    if block == 'button':
                        curr_widget.configure(text=label)
                        curr_widget.bind('<Button-1>', callback)
            else:
                for label in block_config:
                    # Обычный конфиг
                    w_config = None
                    if isinstance(label, dict):
                        w_config = label
                        label = list(label.keys())[0]
                    curr_widget = wgts[block][label]
                    if block == 'button':
                        callback = None
                        if label[:2] != '__':
                            callback = get_yaml_callback(label)
                        curr_widget.configure(text=label)
                        curr_widget.bind('<Button-1>', callback)
                    elif block == 'combobox':
                        callback_name = db.load_combobox_config_by_name(label)

                        # ----------- Убрать хардкод -------------
                        if label == 'quantity':
                            values = ['day_capacity', 'hour_capacity', 'pressure', 'temperature', 'actual_flow']
                        # ----------------------------------------
                        else:
                            values = get_yaml_callback(callback_name)()
                        if len(values) > 0:
                            curr_widget.widget['values'] = values
                            curr_widget.widget.current(0)
                        if isinstance(w_config, dict):
                            if 'selected' in w_config[label]:
                                callback_config = w_config[label]['selected']
                                if isinstance(callback_config, list):
                                    callback_list = []
                                    for callback_name in callback_config:
                                        callback_list.append(get_yaml_callback(callback_name))
                                    curr_widget.widget.bind("<<ComboboxSelected>>", lambda e: [x(e) for x in callback_list])
                                else:
                                    curr_widget.widget.bind("<<ComboboxSelected>>", get_yaml_callback(callback_config))

                    elif block == 'entry':
                        pass

    def build_element(self, elem, master_widget, master_config, widget_config):
        """
        Добавляет элемент из yaml конфигов
        """
        if isinstance(elem, dict):
            master_config = elem
            elem = list(elem.keys())[0]
        elem_name = elem[elem.find('.') + 1:] if elem[0] == '$' else elem
        widget_config = widget_config[elem_name] if elem_name in widget_config else None
        if elem[0] == '$':
            self.add_block(elem, master_widget, widget_config)
        elif elem == 'space':
            space_config = master_config[elem]
            pack_side = space_config['pack_side'] if 'pack_side' in space_config else TOP
            size = space_config['size'] if 'size' in space_config else 30
            self.add_empty_space(master_widget, size=size, pack_side=pack_side)
        elif elem == 'label':
            self.add_label(master_widget, master_config[elem], widget_config)

    def add_block(self, block_name : str, master_widget, block_config):
        """
        Добавляет элемент, помеченный $block или $grid
        """
        if block_name not in ('$block.output', '$block.plot') and block_config is None:
            return
        config = block_name[1:].split('.')
        block_type = config[0]
        w_type = config[1]
        if block_type == 'block':
            getattr(self, f'add_{w_type}_block')(master_widget=master_widget, block_config=block_config)
        elif block_type == 'grid':
            self.add_grid(master_widget, block_config)

    def __make_default_screen(self, label):
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
        self.window.widgets['button']['__to_main_menu__'] = main_menu_button

    def add_output_block(self, master_widget, block_config=None, pack_side=TOP):
        """
        Добавляет блок вывода, состоящий из текстового поля вывода и кнопки очистки этого поля
        """
        output_txt_field = ScrolledText(master_widget,
                                  height=20, state='disabled')
        output_txt_field.pack(fill=X, side=pack_side)
        self.window.widgets['output']['__txt_field__'] = LabeledWidget(output_txt_field)
        Button(master_widget,
               text='Очистить окно вывода',
               font=("Arial Bold", 10),
               command=self.window.clear_output_window).pack(pady=10, side=pack_side)

    def add_entry_block(self, master_widget, block_config, pack_side=TOP):
        """
        Добавляет блок ввода, состоящий из текстовых полей ввода
        """
        for label in block_config:
            if label[0] == '$':
                if label[1:7] == 'custom':
                    raise Exception('Префикс $custom не определен!')
            else:
                frame = ttk.Frame(master_widget,
                                  borderwidth=1, padding=[4, 5])
                frame.pack(fill=X, side=pack_side)
                lbl_text = label
                lbl = Label(frame, text=lbl_text, font=('Arial Bold', 10))
                lbl.pack(side=LEFT)
                entry = Entry(master=frame,
                              width=10, justify='center')
                entry.pack(side=LEFT)
                self.window.widgets['entry'][label] = LabeledWidget(entry, lbl)

    def add_button_block(self, master_widget, block_config, pack_side=BOTTOM):
        """
        Добавляет блок кнопок, рассчитывающих параметры
        """
        for label in block_config:
            frame = ttk.Frame(master=master_widget,
                              borderwidth=1, padding=[4, 5])
            frame.pack(fill=X, side=pack_side)
            button = Button(master=frame, font=("Arial Bold", 10))
            button.pack(side=LEFT)
            self.window.widgets['button'][label] = button

    def add_combobox_block(self, master_widget, block_config, pack_side=TOP):
        """
        Добавляет блок ввода, состоящий из комбобоксов
        """
        for config in block_config:
            label = list(config.keys())[0] if isinstance(config, dict) else config
            frame = ttk.Frame(master=master_widget,
                              borderwidth=1, padding=[8, 10])
            frame.pack(fill=X, side=pack_side)
            lbl_text = label
            lbl = Label(frame, text=lbl_text, font=('Arial Bold', 10))
            lbl.pack(side=LEFT)
            combo = ttk.Combobox(frame, name=label)
            combo.pack(side=LEFT)
            self.window.widgets['combobox'][label] = LabeledWidget(combo, lbl)

    def add_empty_space(self, master_widget, size=30, pack_side=TOP):
        """
        Добавляет блок пустоты, заданный по amount
        """
        Label(master_widget, text="", font=('Arial Bold', 10)).pack(pady=size, side=pack_side)

    def add_plot_block(self, master_widget, block_config=None):
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
        self.window.widgets['plot']['plot'] = plot1
        self.window.widgets['plot']['canvas'] = canvas

    def add_grid(self, master_widget, grid_config):
        i = 0
        if 'values' in grid_config:
            callback_list = get_yaml_callback(grid_config['values'])()
            for screen_data in callback_list:
                screen_name = screen_data[0]
                if screen_name == 'Главное меню':
                    continue
                frame = ttk.Frame(master_widget, borderwidth=1, padding=[4, 5])
                frame.grid(row=i // 2, column=i % 2)
                button = Button(frame, font=("Arial Bold", 10), width=30)
                button.pack()
                self.window.widgets['button'][screen_name] = button
                i += 1

    def add_label(self, master_widget, gui_config, label_config):
        master_widget = self.window.root
        lbl = Label(master_widget, text=gui_config['text'], font=('Arial Bold', 18))
        if 'place' in gui_config:
            place_props = gui_config['place']
            lbl.place(place_props)
        else:
            lbl.pack()
        # self.widgets['label'][screen_name] = button
