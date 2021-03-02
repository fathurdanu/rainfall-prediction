from PyQt5.QtWidgets import QMessageBox

class viewPopup():
    #1
    def ANNselectTargetWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Rainfall Prediction")
        msg.setText("Select the target, please!")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec()

    #2
    def ANNselectDailyMonthlyWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Rainfall Prediction")
        msg.setText("Select daily or monthly forecast, please!")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec()

    #3
    def confirmationBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Rainfall Prediction")
        msg.setText("Are you sure you want to leave the last project?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.buttonClicked.connect(self.buttonPressed)
        x = msg.exec()
        return x

    #4
    def TFdatasetColumnsWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Rainfall Prediction")
        msg.setText("Use 2 Columns only!")
        msg.setInformativeText("1. Date\n2. Rainfall")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec()

    #5
    def ANNdatasetColumnsWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Rainfall Prediction")
        msg.setText("At least 3 Columns!")
        msg.setInformativeText("1. Date in the first column\n2. N Parameter(s): at least one column\n3. And The Target")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec()

    #6
    def dateNotExistWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Rainfall Prediction")
        msg.setText("Put dates in the first column dataset!")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec()

    #7
    def numericDatasetWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Rainfall Prediction")
        msg.setText("Use numeric dataset, please!")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec()

    #7
    def ANNtrainingComplete(self):
        msg = QMessageBox()
        msg.setWindowTitle("Rainfall Prediction")
        msg.setText("Training complete!")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec()

    #8
    def buttonPressed(self,ans):
        return(ans)