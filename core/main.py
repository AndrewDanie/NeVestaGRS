from core.controller.Controller import Controller
from core.view.GRSWindow import GRSWindow


if __name__ == '__main__':
    window = GRSWindow('НеВеста-ГРС')
    window.bind_controller(Controller())
    window.load_window_menu()
    window.mainloop()