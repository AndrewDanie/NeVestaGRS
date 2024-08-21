from core.controller.Controller import Controller
from core.view.Window import Window
from tests.functions.PhysicFunctions import run_all_tests


if __name__ == '__main__':
    run_all_tests()
    window = Window('НеВеста-ГРС')
    controller = Controller(window)
    controller.run_application()