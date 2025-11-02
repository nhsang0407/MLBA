from PyQt6.QtWidgets import QApplication, QMainWindow

from ML_exercise.qtdesigner.ui.MainWindowEx import MainWindowEx

app=QApplication([])
myWindow=MainWindowEx()
myWindow.setupUi(QMainWindow())
myWindow.show()
app.exec()