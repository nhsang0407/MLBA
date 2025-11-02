from ML_exercise.qtdesigner.FileUtil import FileUtil
from ML_exercise.qtdesigner.ui.MainWindow import Ui_MainWindow


class MainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()

    def show(self):
        self.MainWindow.show()
    def close(self):
        self.MainWindow.close()
    def setupSignalAndSlot(self):
        self.pushButtonPredict.clicked.connect(self.predict)
    def predict(self):
        area_income_value = float(self.lineEditIncome.text())
        area_house_age_value = float(self.lineEditAge.text())
        area_number_of_rooms_value = float(self.lineEditRooms.text())
        area_number_of_bedrooms_value = float(self.lineEditBedRooms.text())
        area_population_value = float(self.lineEditPopulation.text())

        trainedModel = FileUtil.loadmodel("housingmodel.zip")
        result = trainedModel.predict([[area_income_value,
                                        area_house_age_value,
                                        area_number_of_rooms_value,
                                        area_number_of_bedrooms_value,
                                        area_population_value]])

        self.lineEditPredict.setText(str(result[0]))