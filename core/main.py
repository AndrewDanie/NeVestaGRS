from core.controller.Controller import Controller
from core.view.Window import Window


if __name__ == '__main__':
    window = Window('НеВеста-ГРС')
    window.bind_controller(Controller())
    window.load_window_menu()
    window.mainloop()