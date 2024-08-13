from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import guidata.texts as TEXT


class Window:

    def __init__(self, title, size='800x600'):
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
        Button(self.root, text='Главное меню', font=("Arial Bold", 10), command=self.load_window_menu)\
            .place(anchor=NE, relx=1, x=-15, y=15)


        left_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
        left_frame.place(relheight=1, relwidth=0.7, rely=0.1)

        right_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
        right_frame.place(relheight=1, relwidth=0.3, rely=0.1, relx=0.7)

        return left_frame, right_frame

    def add_output_block(self, master_widget, pack_side=TOP):
        ScrolledText(master_widget, height=20, state='disabled').pack(fill=X, side=pack_side)
        Button(master_widget, text='Очистить окно вывода', font=("Arial Bold", 10)).pack(pady=10, side=pack_side)

    def add_input_block(self, master_widget, input_labels, pack_side=TOP):
        for label in input_labels:
            frame = ttk.Frame(master_widget, borderwidth=1, padding=[4, 5])
            frame.pack(fill=X, side=pack_side)
            Label(frame, text=label, font=('Arial Bold', 10)).pack(side=LEFT)
            Entry(frame, width=10, justify='center').pack(side=LEFT)

    def add_buttons_block(self, master_widget, button_labels, pack_side=TOP):
        for label in button_labels:
            frame = ttk.Frame(master_widget, borderwidth=1, padding=[4, 5])
            frame.pack(fill=X, side=pack_side)
            Button(frame, text=label, font=("Arial Bold", 10)).pack(side=LEFT)

    def add_combobox(self, master_widget, label, values, pack_side=TOP):
        frame = ttk.Frame(master_widget, borderwidth=1, padding=[8, 10])
        frame.pack(fill=X, side=pack_side)
        Label(frame, text=label, font=('Arial Bold', 10)).pack(side=LEFT)
        combo = ttk.Combobox(frame)
        combo['values'] = values
        combo.current(0)
        combo.pack(side=LEFT)

    def add_empty_space(self, master_widget, amount, pack_side=TOP):
        Label(master_widget, text="", font=('Arial Bold', 10)).pack(pady=amount, side=pack_side)

    def load_window_velocity_calc(self):
        # Расчет скорости в трубопроводах

        self.clear_window()
        input_labels = [
            'Давление, МПа',
            'Температура, °С',
            'Расход',
            'Диаметр Ду, мм'
        ]
        button_labels = [
            'Рассчитать всю ГРС',
            'Подбор диаметра',
            'Плотность газа',
            'Скорость газа',
        ]
        left_frame, right_frame = self.make_default_frames('Расчет скорости в трубопроводах')

        self.add_output_block(left_frame)

        self.add_combobox(right_frame, 'Доступные ГРС', [1, 2, 3])
        self.add_input_block(right_frame, input_labels)
        self.add_empty_space(right_frame, 30, pack_side=BOTTOM)
        self.add_buttons_block(right_frame, button_labels, pack_side=BOTTOM)

    def load_window_odorant_calc(self):
        # Ёмкость одоранта

        self.clear_window()
        input_labels = [
            'Вместимость ёмкости',
            'Расход газа в ст. м3',
        ]
        button_labels = [
            'Требуемый объём',
            'Запас',
        ]
        left_frame, right_frame = self.make_default_frames('Ёмкость одоранта')

        self.add_output_block(left_frame)

        self.add_input_block(right_frame, input_labels)
        self.add_empty_space(right_frame, 30, pack_side=BOTTOM)
        self.add_buttons_block(right_frame, button_labels, pack_side=BOTTOM)

    def load_window_valve_calc(self):
        # Расчёт пропускной способности клапанов
        self.clear_window()
        input_labels = [
            'Давление до клапана, МПа',
            'Давление после клапана, МПа',
            'Температура, °С',
            'Kv, м3/ч',
        ]
        button_labels = [
            'Полный расчёт',
            'Расчёт Kv',
            'Выполнить расчёт',
        ]
        left_frame, right_frame = self.make_default_frames('Расчёт пропускной способности клапанов')

        self.add_output_block(left_frame)

        self.add_combobox(right_frame, 'Доступные ГРС', [1, 2, 3])
        self.add_input_block(right_frame, input_labels)
        self.add_empty_space(right_frame, 30, pack_side=BOTTOM)
        self.add_buttons_block(right_frame, button_labels, pack_side=BOTTOM)

    def load_window_gas_heat_calc(self):
        # Теплотехнический расчёт, подбор подогревателя газа
        self.clear_window()
        input_labels = [
            'Расход газа, ст. м3/ч',
            'Давление на входе ГРС, МПа',
            'Давление на выходе ГРС, МПа',
            'Температура газа на входе ГРС, °С',
            'Минимальная тем-ра на выходе, °С',
        ]
        button_labels = [
            'Выполнить расчёт',
        ]
        left_frame, right_frame = self.make_default_frames('Теплотехнический расчёт, подбор подогревателя газа')

        self.add_output_block(left_frame)

        self.add_combobox(right_frame, 'Доступные ГРС', [1, 2, 3])
        self.add_input_block(right_frame, input_labels)
        self.add_empty_space(right_frame, 30, pack_side=BOTTOM)
        self.add_buttons_block(right_frame, button_labels, pack_side=BOTTOM)

    def load_window_ppk_calc(self):
        # Расчёт предохранительных клапанов ГРС
        self.clear_window()
        input_labels = [
            'Давление до клапана, МПа',
            'Температура, °С',
            'Альфа',
            'Расход газа, ст. м3/ч'
        ]
        button_labels = [
            'Выполнить расчёт',
            'Расчет седла',
        ]
        left_frame, right_frame = self.make_default_frames('Расчёт предохранительных клапанов ГРС')

        self.add_output_block(left_frame)

        self.add_combobox(right_frame, 'Доступные ГРС', [1, 2, 3])
        self.add_input_block(right_frame, input_labels)
        self.add_empty_space(right_frame, 30, pack_side=BOTTOM)
        self.add_buttons_block(right_frame, button_labels, pack_side=BOTTOM)

    def load_window_tvps_calc(self):
        # Расчёт ТВПС
        self.clear_window()
        input_labels = [
            'Минимальное давление',
            'Максимальное давление',
            'Шаг по давлению',
            'Минимальная температура',
            'Максимальная температура',
            'Число точек по температуре',
            'Масштаб подписей данных'
        ]
        button_labels = [
            'Таблица',
            'Расчёт',
            'Вставить секцию ТВПС',
            'График ТВПС',
            'Показать ТВПС'
        ]
        left_frame, right_frame = self.make_default_frames('Расчёт ТВПС')

        self.add_output_block(left_frame)

        self.add_combobox(right_frame, 'Доступные ГРС', [1, 2, 3])
        self.add_input_block(right_frame, input_labels)
        self.add_empty_space(right_frame, 30, pack_side=BOTTOM)
        self.add_buttons_block(right_frame, button_labels, pack_side=BOTTOM)

    def load_window_menu(self):
        # Главное меню
        self.clear_window()
        button_labels = {
            'Расчет скорости в трубопроводах': self.load_window_velocity_calc,
            'Ёмкость одоранта': self.load_window_odorant_calc,
            'Пропускная способность клапанов': self.load_window_valve_calc,
            'Расчёт подогревателя газа': self.load_window_gas_heat_calc,
            'Расчёт ППК': self.load_window_ppk_calc,
            'Толщина стенок трубопроводов': None,
            'Схема': None,
            'Статистика': None,
            'База данных ГРС': None,
            'Расчёт ТВПС': self.load_window_tvps_calc,
        }
        Label(self.root, text='НеВеста-ГРС', font=('Arial Bold', 18)).place(relx=0.5, anchor=N, y=30)

        central_frame = ttk.Frame(self.root, borderwidth=1, padding=[4, 5])
        central_frame.pack(expand=True, anchor=CENTER)
        l = len(button_labels)
        i = 0
        for label in button_labels:
            frame = ttk.Frame(central_frame, borderwidth=1, padding=[4, 5])
            frame.grid(row=i//2, column=i%2)
            Button(frame, text=label, font=("Arial Bold", 10), width=30, command=button_labels[label]).pack()
            i += 1

