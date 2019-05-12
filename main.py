import sys
import start
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #MainWindow = QMainWindow()
    ui = start.MainWindow2()
    ui.show()
    #ui.setupMain(MainWindow)
    #ui.setupUi(MainWindow)
    #ui.setupMain(MainWindow)
    #MainWindow.show()
    #ui.show()
    sys.exit(app.exec_())

