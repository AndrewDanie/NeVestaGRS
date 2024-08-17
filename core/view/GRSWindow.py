from tkinter import ttk
from tkinter import *


from core.view.Window import Window


class GRSWindow(Window):

    def load_window_velocity_calc(self):
        # Расчет скорости в трубопроводах
        self.build_default_gui('Расчет скорости в трубопроводах')

    def load_window_odorant_calc(self):
        # Ёмкость одоранта

        self.clear_window()
        input_labels = [
            'Вместимость ёмкости',
            'Расход газа в ст. м3',
        ]
        button_labels = {
            'Требуемый объём' : None,
            'Запас' : None,
        }
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
        button_labels = {
            'Полный расчёт' : None,
            'Расчёт Kv' : None,
            'Выполнить расчёт' : None,
        }
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
        button_labels = {
            'Выполнить расчёт' : None,
        }
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
        button_labels = {
            'Выполнить расчёт' : None,
            'Расчет седла' : None,
        }
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
        button_labels = {
            'Таблица' : None,
            'Расчёт' : None,
            'Вставить секцию ТВПС' : None,
            'График ТВПС' : None,
            'Показать ТВПС' : None
        }
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
