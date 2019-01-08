from PyQt5.QtWidgets import QWidget, QApplication, QLabel
import sys

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

def show_mywindow():
    app = QApplication(sys.argv)
    mywindows = MyWindow()
    QLabel(mywindows).setText("<p style='color: red; margin-left: 20px'><b>hell world</b></p>")
    mywindows.show()
    # app.exec_()
    sys.exit(app.exec_())

show_mywindow()