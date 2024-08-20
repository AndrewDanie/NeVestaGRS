from tkinter import ttk
from tkinter import *


from core.view.Window import Window


class GRSWindow(Window):

    def load_window_velocity_calc(self):
        # Расчет скорости в трубопроводах
        self.build_default_gui('Расчет скорости в трубопроводах')

    def load_window_odorant_calc(self):
        # Ёмкость одоранта
        self.build_default_gui('Ёмкость одоранта')

    def load_window_valve_calc(self):
        # Расчёт пропускной способности клапанов
        self.build_default_gui('Пропускная способность клапанов')

    def load_window_gas_heat_calc(self):
        # Теплотехнический расчёт, подбор подогревателя газа
        self.build_default_gui('Расчет подогревателя газа')

    def load_window_ppk_calc(self):
        # Расчёт предохранительных клапанов ГРС
        self.build_default_gui('Расчёт предохранительных клапанов ГРС')

    def load_window_tvps_calc(self):
        # Расчёт ТВПС
        self.build_default_gui('Расчёт ТВПС')

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