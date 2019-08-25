import matplotlib
matplotlib.use('tkagg')
from utils.logger import Logger
from gui.main_window import MainWindow

if __name__ == "__main__":
    mw = MainWindow()
    mw.run()
