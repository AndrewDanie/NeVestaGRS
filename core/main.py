from core.view.TkAppContext import TkAppContext
from tests.functions.PhysicFunctions import run_all_tests


if __name__ == '__main__':
    run_all_tests()
    app_context = TkAppContext()
    app_context.run_app()