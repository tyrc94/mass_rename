# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from rename import Rename

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(426, 264)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # DIRECTORY FIELD
        self.directory_field = QtWidgets.QLineEdit(self.centralwidget)
        self.directory_field.setText("")
        self.directory_field.setObjectName("directory_field")
        self.gridLayout.addWidget(self.directory_field, 0, 0, 1, 1)

        # RECURSION CHECK
        self.recursion_check = QtWidgets.QCheckBox(self.centralwidget)
        self.recursion_check.setObjectName("recursion_check")
        self.gridLayout.addWidget(self.recursion_check, 0, 1, 1, 1)

        # SEARCH PATTERN
        self.search_pattern = QtWidgets.QLineEdit(self.centralwidget)
        self.search_pattern.setText("")
        self.search_pattern.setObjectName("search_pattern")
        self.gridLayout.addWidget(self.search_pattern, 1, 0, 1, 1)

        # REGEX CHECK
        self.regex_check = QtWidgets.QCheckBox(self.centralwidget)
        self.regex_check.setObjectName("regex_check")
        self.gridLayout.addWidget(self.regex_check, 1, 1, 1, 1)

        # REPLACEMENT TEXT
        self.replace_text = QtWidgets.QLineEdit(self.centralwidget)
        self.replace_text.setText("")
        self.replace_text.setObjectName("replace_text")
        self.gridLayout.addWidget(self.replace_text, 2, 0, 1, 1)

        # PROGRESS BAR
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 1)

        # EXECUTE
        self.go_button = QtWidgets.QPushButton(self.centralwidget)
        self.go_button.setObjectName("go_button")
        self.gridLayout.addWidget(self.go_button, 3, 1, 1, 1)
        self.go_button.clicked.connect(self.execute)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 426, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mass Rename Utility v0.5"))
        self.directory_field.setPlaceholderText(_translate("MainWindow", "Enter your directory here"))
        self.recursion_check.setText(_translate("MainWindow", "Recursive"))
        self.search_pattern.setPlaceholderText(_translate("MainWindow", "Enter your search pattern here"))
        self.regex_check.setText(_translate("MainWindow", "RegEx"))
        self.replace_text.setPlaceholderText(_translate("MainWindow", "Enter your replacement text here"))
        self.go_button.setText(_translate("MainWindow", "Start"))

    def execute(self):
        print(self.search_pattern.text())
        print(self.replace_text.text())
        print(self.directory_field.text())
        print(self.recursion_check.isChecked())

        if self.directory_field.text() == '':
            print('Empty!')
            QMessageBox.warning(QWidget(), 'Error', 'Directory field is empty!', QMessageBox.Ok)
            return

        run = Rename(self.search_pattern.text(), 
                    self.replace_text.text(), 
                    self.directory_field.text(),
                    self.recursion_check.isChecked())

        run.populate()
        confirm_msg = f'Are you sure that you want to change {run.num_files} files?\nThese changes will be irreversible.'
        reply = QMessageBox.question(QWidget(), 'Caution', confirm_msg,
                                    QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            complete = run.rename(self.progressBar.setValue)

        if reply == QMessageBox.No:
            return
        
        if complete:
            QMessageBox.information(QWidget(), 'Complete', 'Renaming successful.', QMessageBox.Ok)
            self.progressBar.setValue(0)
            self.search_pattern.setText("")
            self.replace_text.setText("")
            self.directory_field.setText("")
        
        elif not complete:
            QMessageBox.critical(QWidget(), 'Error', 'An error has occured.\nPlease check your input and try again.', QMessageBox.Ok)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
