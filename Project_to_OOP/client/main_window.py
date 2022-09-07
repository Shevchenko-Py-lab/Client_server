import sys
import json
import logging
sys.path.append('../')


from client_ui import Ui_MainClientWindow
from PyQt5.QtWidgets import QMainWindow


logger = logging.getLogger('client_dist')


# Класс основного окна
class ClientMainWindow(QMainWindow):
    def __init__(self, database, transport):
        super().__init__()
