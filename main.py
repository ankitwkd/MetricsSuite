import json
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QInputDialog, QGroupBox, QLineEdit, QFormLayout, \
    QLabel, QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QComboBox, QFileDialog, QTabWidget, QMessageBox, \
    QGridLayout, QVBoxLayout

from FPTabs import FPTabs
from LanguagesWindow import Languages
from SMITab import SMITab
from UCPTabs import UCPTabs


class Main(QMainWindow):
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.quit()
        a0.ignore()
    def __init__(self):
        super().__init__()

        self.loadMode=False
        self.lang= Languages()
        self.initUI()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.currentTab=None
        self.tabs.currentChanged.connect(self.tabChange)
        self.d=None
        self.tabNames=[]
        self.smiTab = None



        self.pName=''
        self.title='CECS 543 - Metrics Suite'
        self.lang.button.clicked.connect(self.clickLangDone)

        self.locPerFP = {}
        self.loc = [337, 154, 148, 59, 58, 80, 90, 43, 55, 54, 38, 50]



        index = 0
        for l in self.lang.availableLang:
            self.locPerFP[l] = self.loc[index]
            index += 1


    def initUI(self):
        #Actions
        self.newAct = QAction('&New', self)
        self.openAct = QAction('&Open', self)
        saveAct = QAction('&Save', self)
        exitAct = QAction('&Exit', self)
        languageAct = QAction('&Language', self)
        enterfpAct = QAction("&Enter FP data", self)
        enterucpAct = QAction("&Enter UCP data", self)
        smiAct = QAction('&Calculate SMI', self)
        helpAct = QAction('&Help', self)

        #Action Triggers
        self.newAct.triggered.connect(self.triggerNewProject)
        saveAct.triggered.connect(self.saveFileDialog)
        self.openAct.triggered.connect(self.openFileDialog)
        exitAct.triggered.connect(self.quit)
        languageAct.triggered.connect(self.triggerLanguage)
        enterfpAct.triggered.connect(self.triggerEnterFP)
        enterucpAct.triggered.connect(self.triggerEnterUCP)
        helpAct.triggered.connect(self.triggerHelp)

        smiAct.triggered.connect(self.triggerSMI)

        menuBar = self.menuBar()

        #Menus
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(exitAct)

        editMenu = menuBar.addMenu('&Edit')

        prefMenu = menuBar.addMenu('&Preferences')
        prefMenu.addAction(languageAct)
        self.metricsMenu = menuBar.addMenu('&Metrics')
        self.metricsMenu.setDisabled(True)
        ucpMenu = self.metricsMenu.addMenu('&Use Case Points')
        fpMenu=self.metricsMenu.addMenu('&Function Point')
        smiMenu=self.metricsMenu.addMenu('&Software Maturity Index')
        fpMenu.addAction(enterfpAct)
        ucpMenu.addAction(enterucpAct)
        smiMenu.addAction(smiAct)
        helpMenu = menuBar.addMenu('&Help')
        helpMenu.addAction(helpAct)
        menuBar.setNativeMenuBar(False)


        # self.setCustomStyle()
        self.setGeometry(100, 100, 700, 500)
        self.move(300,200)
        self.setWindowTitle('CECS 543 Metrics Suite')
        self.show()

    def triggerHelp(self):
        msg = QMessageBox()
        msg.setText("1. You have to either create a new project or open an existing project to view any metrics pane. (Disabled by default)\n2. During an active project, new and open option will be disabled.\n3. Save option will save into file named project-name.ms and will display a success message with file-name\n4. On File—>Exit or close button of window will ask the user to save or discard changes.\n5. SMI Tab can open only once, so on clicking on new SMI tab when its already active, will bring control to existing SMI tab.\n6. Under UCP metrics, TCF,ECF,UUCW and UAW dialogs have calculated result which is evaluated on the go.\n7. All values under UCP metrics are either rounded upto 2 decimal places or to nearest Integer as mentioned in UI\n8. All sub-windows inside tabs support open-close mechanism as in they are not destroyed. (as asked)\n9. Under SMI, each row will be initialized with default values (0)\n10. Total modules are evaluated on the go. (once any cell value is changed)\n11. SMI value is not rounded as shown on beachboard.\n12. Valid integer(positive/negative) validation is present on each value inserted in SMI table.\n13. Under UCP and FP, all calculated metrics are disabled for input as asked. \n14. Under UCP and FP, all input fields have a validator in place to check for non-negative integers.\n15. Under UCP, UCP is calculated as TCF*ECF*UUCP and Estimated hours is evaluated as UCP * PF \n16. Estimated LOC = (LOC/UCP) * UCP\n17. Estimated PM = (LOC/(LOC/PM))\n18. Adding this document to Help for convenience as a pop-up dialog.")
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Few Features")
        msg.exec()
    def quit(self):
        q = QMessageBox()
        q.move(300,200)
        reply = q.question(
            self, "Message",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
            QMessageBox.Save)
        if reply == QMessageBox.Save:
            self.saveFileDialog()
        elif reply == QMessageBox.Cancel:
            return

        qApp.quit()
    def tabChange(self):
        self.currentTab=self.tabs.currentWidget()
        if self.currentTab.fpData and len(self.lang.selectedLang)>0:
            self.currentTab.fpData.preferredLanguage=self.lang.selectedLang
    def triggerNewProject(self):

        self.formGroupBox = QGroupBox("CECS 543 Metrics Suite New Project")
        self.formGroupBox.setWindowTitle("New Project")
        # project name,product name, creator, comments
        self.projectName=QLineEdit()
        self.productName=QLineEdit()
        self.creator=QLineEdit()
        self.comments=QPlainTextEdit()
        self.createForm()
        self.formGroupBox.show()



    def createForm(self):
        # creating a form layout
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)

        # adding rows
        layout.addRow(QLabel("Project Name: "), self.projectName)

        layout.addRow(QLabel("Product Name: "), self.productName)

        layout.addRow(QLabel("Creator: "), self.creator)

        layout.addRow(QLabel("Comments:"))
        layout.addRow(self.comments)

        ok=QPushButton('Ok')
        cancel=QPushButton('Cancel')
        ok.clicked.connect(self.createNewProject)
        cancel.clicked.connect(self.formGroupBox.close)

        btnLayout=QHBoxLayout()
        btnLayout.addWidget(ok)
        btnLayout.addWidget(cancel)
        layout.addRow(btnLayout)


        # setting layout
        self.formGroupBox.setLayout(layout)
        self.formGroupBox.setGeometry(100,100,300,300)
        self.formGroupBox.move(300,200)
    def createTcfForm(self):
        # creating a form layout
        if len(self.currentTab.tcfComplexity)>0:
            self.currentTab.saveTcfWidget.show()
            return
        self.currentTab.tcfFactors.clear()
        self.currentTab.tcfComplexity.clear()
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.setHorizontalSpacing(50)
        layout.addRow(QLabel('Assign a value from 0 to 5 for each of the following Technical Complexity Factors:'))
        headers_layout = QHBoxLayout()
        headers_layout.setSpacing(80)
        headers = ['Technical Factor', 'Weight', 'Perceived Complexity', 'Calculated Factor']
        headers_layout.addWidget(QLabel(headers[0]))
        headers_layout.addSpacing(150)
        for h in headers[1::]:
            headers_layout.addWidget(QLabel(h))
        layout.addRow(headers_layout)
        tcfactors=['T1 - Distributed System','T2 - Performance','T3 - End User Efficiency','T4 - Complex Internal Processing','T5 - Reusability','T6 - Easy to install','T7 - Easy to use','T8 - Portable','T9 - Easy to change','T10 - Concurrent','T11 - Special security features','T12 - Provides direct access for third parties','T13 - Special user training facilities are required']
        weights = ['2','1','1','1','1','0.5','0.5','2','1','1','1','1','1']
        # adding rows
        weight_combos = []
        complexity_combos = []
        calculated_factors = []
        for f, w in zip(tcfactors,weights):
            comboLayout = QHBoxLayout()
            comboLayout.setSpacing(100)
            weight_combo = QLineEdit(self)
            complexity_combo = QComboBox(self)
            calculated_factor = QLineEdit(self)
            calculated_factor.setText('0.0')
            calculated_factor.setReadOnly(True)
            weight_combo.setReadOnly(True)
            comboLayout.addWidget(weight_combo)
            comboLayout.addWidget(complexity_combo)
            comboLayout.addSpacing(30)
            comboLayout.addWidget(calculated_factor)
            self.currentTab.tcfFactors.append(calculated_factor)
            self.currentTab.tcfComplexity.append(complexity_combo)
            complexity_combo.addItems(['0', '1', '2', '3', '4', '5'])
            weight_combo.setText(w)
            complexity_combo.setCurrentIndex(0)
            weight_combos.append(weight_combo)
            complexity_combos.append(complexity_combo)
            calculated_factors.append(calculated_factor)
            layout.addRow(QLabel(f), comboLayout)
            def comboChange():
                for w,c,f in zip(weight_combos,complexity_combos,calculated_factors):
                    wt = float(w.text())
                    cmp = float(c.currentText())
                    f.setText(str(wt * cmp))


            complexity_combo.currentIndexChanged.connect(comboChange)





        done=QPushButton('Done')
        cancel=QPushButton('Cancel')
        done.clicked.connect(self.saveTcf)
        cancel.clicked.connect(self.currentTab.saveTcfWidget.close)

        btnLayout=QHBoxLayout()
        btnLayout.addWidget(done)
        btnLayout.addWidget(cancel)
        btnLayout.addStretch(2)
        layout.addRow(btnLayout)


        # setting layout
        self.currentTab.saveTcfWidget.setLayout(layout)
        self.currentTab.saveTcfWidget.setGeometry(100,100,300,300)
        self.currentTab.saveTcfWidget.move(300,200)
        self.currentTab.saveTcfWidget.setWindowTitle("Technical Complexity Factors")
        self.currentTab.saveTcfWidget.show()



    def createEcfForm(self):
        # creating a form layout
        if len(self.currentTab.ecfComplexity)>0:
            self.currentTab.saveEcfWidget.show()
            return
        self.currentTab.ecfFactors.clear()
        self.currentTab.ecfComplexity.clear()
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.setHorizontalSpacing(50)
        layout.addRow(QLabel('Assign a value from 0 to 5 for each of the following Environmental Complexity Factors:'))
        headers_layout = QHBoxLayout()
        headers_layout.setSpacing(80)
        headers = ['Environmental Factor', 'Weight', 'Perceived Impact', 'Calculated Factor']
        headers_layout.addWidget(QLabel(headers[0]))
        headers_layout.addSpacing(150)
        for h in headers[1::]:
            headers_layout.addWidget(QLabel(h))
        layout.addRow(headers_layout)
        ecfactors = ['E1 - Familiarity with UML', 'E2 - Application Experience', 'E3 - Object oriented experience',
                     'E4 - Lead analyst capability', 'E5 - Motivation', 'E6 - Stable requirements',
                     'E7 - Part-time workers', 'E8 - Difficult programming language']
        weights = ['1.5','0.5','1','0.5','1','2','-1','2'   ]
        # adding rows
        weight_combos = []
        complexity_combos = []
        calculated_factors = []
        for f, w in zip(ecfactors,weights):
            comboLayout = QHBoxLayout()
            comboLayout.setSpacing(100)
            weight_combo = QLineEdit(self)
            complexity_combo = QComboBox(self)
            calculated_factor = QLineEdit(self)

            calculated_factor.setReadOnly(True)
            weight_combo.setReadOnly(True)
            comboLayout.addWidget(weight_combo)
            comboLayout.addWidget(complexity_combo)
            comboLayout.addSpacing(30)
            comboLayout.addWidget(calculated_factor)
            self.currentTab.ecfFactors.append(calculated_factor)
            self.currentTab.ecfComplexity.append(complexity_combo)
            complexity_combo.addItems(['0', '1', '2', '3', '4', '5'])
            weight_combo.setText(w)
            complexity_combo.setCurrentIndex(0)
            calculated_factor.setText(str(float(weight_combo.text())*float(complexity_combo.currentText())))
            weight_combos.append(weight_combo)
            complexity_combos.append(complexity_combo)
            calculated_factors.append(calculated_factor)
            layout.addRow(QLabel(f), comboLayout)
            def comboChange():
                for w,c,f in zip(weight_combos,complexity_combos,calculated_factors):
                    wt = float(w.text())
                    cmp = float(c.currentText())
                    f.setText(str(wt * cmp))


            complexity_combo.currentIndexChanged.connect(comboChange)

        done=QPushButton('Done')
        cancel=QPushButton('Cancel')
        done.clicked.connect(self.saveEcf)
        cancel.clicked.connect(self.currentTab.saveEcfWidget.close)

        btnLayout=QHBoxLayout()
        btnLayout.addWidget(done)
        btnLayout.addWidget(cancel)
        btnLayout.addStretch(2)
        layout.addRow(btnLayout)


        # setting layout
        self.currentTab.saveEcfWidget.setLayout(layout)
        self.currentTab.saveEcfWidget.setGeometry(100,100,300,300)
        self.currentTab.saveEcfWidget.move(300, 200)
        self.currentTab.saveEcfWidget.setWindowTitle("Environmental Complexity Factors")
        self.currentTab.saveEcfWidget.show()

    def createUucwForm(self):
        # creating a form layout
        if len(self.currentTab.uucwUseCases) > 0:
            self.currentTab.saveUucwWidget.show()
            return
        self.currentTab.uucwUseCases.clear()
        self.currentTab.uucwResult.clear()
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.setHorizontalSpacing(100)
        layout.addRow(QLabel('Assign number of use cases for each of the following use case categories:'))
        headers_layout = QHBoxLayout()
        headers_layout.setSpacing(100)
        headers = ['Use case type', 'Description', 'Weight', 'Number of use cases', 'Result']
        headers_layout.addWidget(QLabel(headers[0]))
        headers_layout.addWidget(QLabel(headers[1]))
        headers_layout.addSpacing(280)

        #headers_layout.addSpacing(60)
        for h in headers[2::]:
            headers_layout.addWidget(QLabel(h))
        layout.addRow(headers_layout)
        useCaseTypes = ['Simple', 'Average', 'Complex']
        description = ['A simple user interface and touches only a single database entity;\nits success scenario has 3 steps or less;\nits implementation involves less than 5 classes. ',
                       'More interface design and touches 2 or more database entities;it \nis between 4 to 7 steps; its implementation \ninvolves between 5 to 10 classes.                    ',
                       'Involves a complex user interface or processing and touches 3 or\nmore database entities; over seven steps;\nits implementation involves more than 10 classes.']
        weights = ['5', '10', '15']
        # adding rows
        usecases_combos = []
        result_combos = []
        for u,d, w in zip(useCaseTypes, description, weights):
            comboLayout = QHBoxLayout()
            comboLayout.setSpacing(100)
            description_combo = QLabel(d)
            weight_combo = QLabel(w)
            useCases_combo = QLineEdit(self)
            reg_ex = QRegExp("[0-9]+")
            input_validator = QRegExpValidator(reg_ex, useCases_combo)
            useCases_combo.setValidator(input_validator)
            useCases_combo.setText('0')
            result = QLineEdit(self)

            result.setReadOnly(True)
            comboLayout.addWidget(description_combo)
            comboLayout.addWidget(weight_combo)
            comboLayout.addSpacing(30)
            comboLayout.addWidget(useCases_combo)
            comboLayout.addSpacing(30)
            comboLayout.addWidget(result)
            self.currentTab.uucwUseCases.append(useCases_combo)
            self.currentTab.uucwResult.append(result)
            result.setText(str(int(useCases_combo.text()) * int(weight_combo.text())))
            usecases_combos.append(useCases_combo)
            result_combos.append(result)
            layout.addRow(QLabel(u), comboLayout)

            def comboChange():
                for u, w, r in zip(usecases_combos, weights, result_combos):
                    if u.text()=='':
                        use_cases = 0
                    else:
                        use_cases = int(u.text())
                    wt = int(w)
                    r.setText(str(wt * use_cases))

            useCases_combo.textChanged.connect(comboChange)

        done = QPushButton('Done')
        cancel = QPushButton('Cancel')
        done.clicked.connect(self.saveUucw)
        cancel.clicked.connect(self.currentTab.saveUucwWidget.close)

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(done)
        btnLayout.addWidget(cancel)
        btnLayout.addStretch(2)
        layout.addRow(btnLayout)

        # setting layout
        self.currentTab.saveUucwWidget.setLayout(layout)
        self.currentTab.saveUucwWidget.setGeometry(100, 100, 300, 300)
        self.currentTab.saveUucfWidget.move(300, 200)
        self.currentTab.saveUucwWidget.show()

    def createUucwGrid(self):
        # creating a form layout
        if len(self.currentTab.uucwUseCases) > 0:
            self.currentTab.saveUucwWidget.show()
            return
        self.currentTab.uucwUseCases.clear()
        self.currentTab.uucwResult.clear()
        layout = QGridLayout()
        layout.addWidget(QLabel('Assign number of use cases for each of the following use case categories:'))
        headers = ['Use case type', 'Description', 'Weight', 'Number of use cases', 'Result']

        #headers_layout.addSpacing(60)
        for i,h in enumerate(headers):
            layout.addWidget(QLabel(h), 1, i)
        useCaseTypes = ['Simple', 'Average', 'Complex']
        description = ['A simple user interface and touches only a single database entity;\nits success scenario has 3 steps or less;\nits implementation involves less than 5 classes. ',
                       'More interface design and touches 2 or more database entities;it \nis between 4 to 7 steps; its implementation \ninvolves between 5 to 10 classes.                    ',
                       'Involves a complex user interface or processing and touches 3 or\nmore database entities; over seven steps;\nits implementation involves more than 10 classes.']
        weights = ['5', '10', '15']
        # adding rows
        usecases_combos = []
        result_combos = []
        grid_index = 2
        for u,d, w in zip(useCaseTypes, description, weights):
            description_combo = QLabel(d)
            weight_combo = QLabel(w)
            useCases_combo = QLineEdit(self)
            reg_ex = QRegExp("[0-9]+")
            input_validator = QRegExpValidator(reg_ex, useCases_combo)
            useCases_combo.setValidator(input_validator)
            useCases_combo.setText('0')
            result = QLineEdit(self)
            result.setReadOnly(True)
            layout.addWidget(QLabel(u), grid_index, 0)
            layout.addWidget(description_combo, grid_index, 1)
            layout.addWidget(weight_combo, grid_index, 2)
            layout.addWidget(useCases_combo, grid_index, 3)
            layout.addWidget(result, grid_index, 4)

            self.currentTab.uucwUseCases.append(useCases_combo)
            self.currentTab.uucwResult.append(result)
            result.setText(str(int(useCases_combo.text()) * int(weight_combo.text())))
            usecases_combos.append(useCases_combo)
            result_combos.append(result)
            grid_index += 1

            def comboChange():
                for u, w, r in zip(usecases_combos, weights, result_combos):
                    if u.text()=='':
                        use_cases = 0
                    else:
                        use_cases = int(u.text())
                    wt = int(w)
                    r.setText(str(wt * use_cases))

            useCases_combo.textChanged.connect(comboChange)

        done = QPushButton('Done')
        cancel = QPushButton('Cancel')
        done.clicked.connect(self.saveUucw)
        cancel.clicked.connect(self.currentTab.saveUucwWidget.close)

        vbox = QVBoxLayout()
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(done)
        btnLayout.addWidget(cancel)
        btnLayout.addStretch(2)
        vbox.addLayout(layout)
        vbox.addLayout(btnLayout)

        # setting layout
        self.currentTab.saveUucwWidget.setLayout(vbox)
        self.currentTab.saveUucwWidget.setGeometry(100, 100, 300, 300)
        self.currentTab.saveUucwWidget.move(150, 400)
        self.currentTab.saveUucwWidget.setWindowTitle("Unadjusted Use Case Weights")
        self.currentTab.saveUucwWidget.show()
    def createUawGrid(self):
        # creating a form layout
        if len(self.currentTab.uawActors) > 0:
            self.currentTab.saveUawWidget.show()
            return
        self.currentTab.uawActors.clear()
        self.currentTab.uawResult.clear()
        layout = QGridLayout()
        layout.addWidget(QLabel('Assign number of use cases actors for each of the following use case categories:'))
        headers = ['Use case type', 'Description', 'Weight', 'Number of usecase actors', 'Result']

        #headers_layout.addSpacing(60)
        for i,h in enumerate(headers):
            layout.addWidget(QLabel(h), 1, i)
        useCaseTypes = ['Simple', 'Average', 'Complex']
        description = [
            'The Actor represents another system with a defined API.  ',
            'The Actor represents another system interacting through\na protocol, like TCP/IP.',
            'The Actor is a person interacting via an interface.              ']
        weights = ['1', '2', '3']
        # adding rows
        usecases_combos = []
        result_combos = []
        grid_index = 2
        for u,d, w in zip(useCaseTypes, description, weights):
            description_combo = QLabel(d)
            weight_combo = QLabel(w)
            useCases_combo = QLineEdit(self)
            reg_ex = QRegExp("[0-9]+")
            input_validator = QRegExpValidator(reg_ex, useCases_combo)
            useCases_combo.setValidator(input_validator)
            useCases_combo.setText('0')
            result = QLineEdit(self)
            result.setReadOnly(True)
            layout.addWidget(QLabel(u), grid_index, 0)
            layout.addWidget(description_combo, grid_index, 1)
            layout.addWidget(weight_combo, grid_index, 2)
            layout.addWidget(useCases_combo, grid_index, 3)
            layout.addWidget(result, grid_index, 4)

            self.currentTab.uawActors.append(useCases_combo)
            self.currentTab.uawResult.append(result)
            result.setText(str(int(useCases_combo.text()) * int(weight_combo.text())))
            usecases_combos.append(useCases_combo)
            result_combos.append(result)
            grid_index += 1

            def comboChange():
                for u, w, r in zip(usecases_combos, weights, result_combos):
                    if u.text()=='':
                        use_cases = 0
                    else:
                        use_cases = int(u.text())
                    wt = int(w)
                    r.setText(str(wt * use_cases))

            useCases_combo.textChanged.connect(comboChange)

        done = QPushButton('Done')
        cancel = QPushButton('Cancel')
        done.clicked.connect(self.saveUaw)
        cancel.clicked.connect(self.currentTab.saveUawWidget.close)

        vbox = QVBoxLayout()
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(done)
        btnLayout.addWidget(cancel)
        btnLayout.addStretch(2)
        vbox.addLayout(layout)
        vbox.addLayout(btnLayout)

        # setting layout
        self.currentTab.saveUawWidget.setLayout(vbox)
        self.currentTab.saveUawWidget.setGeometry(100, 100, 300, 300)
        self.currentTab.saveUawWidget.move(150, 400)
        self.currentTab.saveUucwWidget.setWindowTitle("Unadjusted Actor Weights")
        self.currentTab.saveUawWidget.show()

    def createUawForm(self):
        # creating a form layout
        if len(self.currentTab.uawActors) > 0:
            self.currentTab.saveUawWidget.show()
            return
        self.currentTab.uawActors.clear()
        self.currentTab.uawResult.clear()
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.setHorizontalSpacing(60)
        layout.addRow(QLabel('Assign number of use cases actors for each of the following use case categories:'))
        headers_layout = QHBoxLayout()
        headers_layout.setSpacing(100)
        headers = ['Use case type', 'Description', 'Weight', 'Number of usecase actors', 'Result']
        headers_layout.addWidget(QLabel(headers[0]))
        headers_layout.addWidget(QLabel(headers[1]))
        headers_layout.addSpacing(185)

        # headers_layout.addSpacing(60)
        for h in headers[2::]:
            headers_layout.addWidget(QLabel(h))
        layout.addRow(headers_layout)
        useCaseTypes = ['Simple', 'Average', 'Complex']
        description = [
            'The Actor represents another system with a defined API.  ',
            'The Actor represents another system interacting through\na protocol, like TCP/IP.',
            'The Actor is a person interacting via an interface.              ']
        weights = ['1', '2', '3']
        # adding rows
        usecases_combos = []
        result_combos = []
        for u, d, w in zip(useCaseTypes, description, weights):
            comboLayout = QHBoxLayout()
            comboLayout.setSpacing(100)
            description_combo = QLabel(d)
            weight_combo = QLabel(w)
            useCases_combo = QLineEdit(self)
            reg_ex = QRegExp("[0-9]+")
            input_validator = QRegExpValidator(reg_ex, useCases_combo)
            useCases_combo.setValidator(input_validator)
            useCases_combo.setText('0')
            result = QLineEdit(self)

            result.setReadOnly(True)
            comboLayout.addWidget(description_combo)
            comboLayout.addWidget(weight_combo)
            comboLayout.addSpacing(30)
            comboLayout.addWidget(useCases_combo)
            comboLayout.addSpacing(30)
            comboLayout.addWidget(result)
            self.currentTab.uawActors.append(useCases_combo)
            self.currentTab.uawResult.append(result)
            result.setText(str(int(useCases_combo.text()) * int(weight_combo.text())))
            usecases_combos.append(useCases_combo)
            result_combos.append(result)
            layout.addRow(QLabel(u), comboLayout)

            def comboChange():
                for u, w, r in zip(usecases_combos, weights, result_combos):
                    if u.text() == '':
                        use_cases = 0
                    else:
                        use_cases = int(u.text())
                    wt = int(w)
                    r.setText(str(wt * use_cases))

            useCases_combo.textChanged.connect(comboChange)

        done = QPushButton('Done')
        cancel = QPushButton('Cancel')
        done.clicked.connect(self.saveUaw)
        cancel.clicked.connect(self.currentTab.saveUawWidget.close)

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(done)
        btnLayout.addWidget(cancel)
        btnLayout.addStretch(2)
        layout.addRow(btnLayout)

        # setting layout
        self.currentTab.saveUawWidget.setLayout(layout)
        self.currentTab.saveUawWidget.setGeometry(100, 100, 300, 300)
        self.currentTab.saveUawWidget.move(300, 200)
        self.currentTab.saveUawWidget.show()

    def createVafForm(self):
        # creating a form layout
        if len(self.currentTab.vafCombos)>0:
            self.currentTab.saveVafWidget.show()
            return
        self.currentTab.vafCombos.clear()
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow(QLabel('Assign a value from 0 to 5 for each of the following Value Adjustment Factors:'))
        vafactors=['Does the system require reliable backup and recovery processes?','Are specialized data communications required to transfer information to or from the application?','Are there distributed processing functions?','Is performance critical?','Will the system run in an existing, heavily utilized operational environment','Does the system require online data entry?','Does the online data entry require the input transaction to be built over multiple screens or operations?','Are the internal logical files updated online?','Are the input, output, files or inquiries complex?','Is the internal processing complex?','Is the code designed to be reusable?','Are conversion and installation included in the design? ','Is the system designed for multiple installations in different organizations?','Is the application designed to facilitate change and for ease of use by the user']
        # adding rows
        for f in vafactors:
            combo = QComboBox(self)
            self.currentTab.vafCombos.append(combo)
            combo.addItems(['0','1','2','3','4','5'])
            combo.setCurrentIndex(0)
            layout.addRow(QLabel(f), combo)



        done=QPushButton('Done')
        cancel=QPushButton('Cancel')
        done.clicked.connect(self.saveVaf)
        cancel.clicked.connect(self.currentTab.saveVafWidget.close)

        btnLayout=QHBoxLayout()
        btnLayout.addWidget(done)
        btnLayout.addWidget(cancel)
        btnLayout.addStretch(2)
        layout.addRow(btnLayout)


        # setting layout
        self.currentTab.saveVafWidget.setWindowTitle("Value Adjustment Factors")
        self.currentTab.saveVafWidget.setLayout(layout)
        self.currentTab.saveVafWidget.setGeometry(100,100,300,300)
        self.currentTab.saveVafWidget.move(300,200)
        self.currentTab.saveVafWidget.show()
    def saveVaf(self):
        vaf=0
        self.currentTab.fpData.vafValues.clear()
        for v in self.currentTab.vafCombos:
            value=int(v.currentText())
            self.currentTab.fpData.vafValues.append(value)
            vaf+=value
        self.currentTab.vafOutput.setText(str(vaf))
        self.currentTab.fpData.vafCount = vaf
        self.currentTab.saveVafWidget.hide()
    def saveTcf(self):
        total=0.0
        self.currentTab.ucpData.tcfValues.clear()
        self.currentTab.ucpData.tcfFactors.clear()
        for c,v in zip(self.currentTab.tcfComplexity,self.currentTab.tcfFactors):
            value=float(v.text())
            cmp = float(c.currentText())
            self.currentTab.ucpData.tcfValues.append(value)
            self.currentTab.ucpData.tcfFactors.append(cmp)
            total+=value
        tcf = 0.6 + (.01*total)
        self.currentTab.tcfOutput.setText(str(round(tcf,2)))
        self.currentTab.ucpData.tcfOutput = round(tcf,2)
        self.currentTab.saveTcfWidget.hide()
    def saveEcf(self):
        total = 0.0
        self.currentTab.ucpData.ecfValues.clear()
        self.currentTab.ucpData.ecfFactors.clear()
        for c, v in zip(self.currentTab.ecfComplexity, self.currentTab.ecfFactors):
            value = float(v.text())
            cmp = float(c.currentText())
            self.currentTab.ucpData.ecfValues.append(value)
            self.currentTab.ucpData.ecfFactors.append(cmp)
            total += value
        ecf = 1.4 + (-0.03*total)
        self.currentTab.ecfOutput.setText(str(round(ecf,2)))
        self.currentTab.ucpData.ecfOutput = round(ecf,2)
        self.currentTab.saveEcfWidget.hide()
    def saveUucw(self):
        uucw = 0
        self.currentTab.ucpData.uucwUseCases.clear()
        self.currentTab.ucpData.uucwResults.clear()
        for u, r in zip(self.currentTab.uucwUseCases, self.currentTab.uucwResult):
            if u.text() == '':
                use_case = 0
            else:
                use_case = int(u.text())
            res = int(r.text())
            self.currentTab.ucpData.uucwUseCases.append(use_case)
            self.currentTab.ucpData.uucwResults.append(res)
            uucw += res
        self.currentTab.uucwOutput.setText(str(uucw))
        self.currentTab.ucpData.uucwOutput = uucw
        self.currentTab.saveUucwWidget.hide()
    def saveUaw(self):
        uaw = 0
        self.currentTab.ucpData.uawActors.clear()
        self.currentTab.ucpData.uawResults.clear()
        for u, r in zip(self.currentTab.uawActors, self.currentTab.uawResult):
            if u.text() == '':
                use_case = 0
            else:
                use_case = int(u.text())
            res = int(r.text())
            self.currentTab.ucpData.uawActors.append(use_case)
            self.currentTab.ucpData.uawResults.append(res)
            uaw += res
        self.currentTab.uawOutput.setText(str(uaw))
        self.currentTab.ucpData.uawOutput = uaw
        self.currentTab.saveUawWidget.hide()
    def createNewProject(self):
        if self.d!=None:
            self.pName=self.d[0]["projectName"]
        else:
            self.pName=self.projectName.text()
            self.formGroupBox.close()
        self.setWindowTitle(self.title+ ' - ' + self.pName)
        self.metricsMenu.setDisabled(False)
        self.newAct.setDisabled(True)
        self.openAct.setDisabled(True)

    def triggerLanguage(self):
        self.lang.show()
    def triggerEnterFP(self):
        name, ok = QInputDialog.getText(self, 'Input', 'Name of this FP',QLineEdit.Normal,"Untitled")
        if not ok:
            return

        newTab = FPTabs()
        newTab.currLangValue.setText(self.lang.selectedLang)
        newTab.localLang=self.lang.selectedLang
        newTab.computeFPbtn.clicked.connect(self.computeFP)
        newTab.changeLangBtn.clicked.connect(self.changeLanguageWindow)
        newTab.vafBtn.clicked.connect(self.createVafForm)
        newTab.codeSizeBtn.clicked.connect(self.calculateCodeSize)
        self.tabNames.append(name)
        self.tabs.addTab(newTab,name)

    def triggerEnterUCP(self):
        name, ok = QInputDialog.getText(self, 'Input', 'Name of this UCP',QLineEdit.Normal,"Untitled")
        if not ok:
            return

        newTab = UCPTabs()
        newTab.tcfBtn.clicked.connect(self.createTcfForm)
        newTab.ecfBtn.clicked.connect(self.createEcfForm)
        newTab.uucwBtn.clicked.connect(self.createUucwGrid)
        newTab.uawBtn.clicked.connect(self.createUawGrid)

        self.tabNames.append(name)
        self.tabs.addTab(newTab,name)

    def triggerSMI(self):
        if self.smiTab:
            self.tabs.setCurrentWidget(self.smiTab)
            return
        name = 'SMI'
        newTab = SMITab()
        self.smiTab = newTab
        # newTab.tcfBtn.clicked.connect(self.createTcfForm)
        # newTab.ecfBtn.clicked.connect(self.createEcfForm)
        # newTab.uucwBtn.clicked.connect(self.createUucwForm)
        # newTab.uawBtn.clicked.connect(self.createUawForm)

        self.tabNames.append(name)
        self.tabs.addTab(newTab, name)
    def changeLanguageWindow(self):
        if self.currentTab.currLangChangeWindow==None:
            self.currentTab.currLangChangeWindow=Languages()
            self.currentTab.currLangChangeWindow.gb.buttons()[self.lang.availableLang.index(self.lang.gb.checkedButton().text())].setChecked(True)
        self.currentTab.currLangChangeWindow.show()
        self.currentTab.currLangChangeWindow.button.clicked.connect(self.changeCurrLang)
    def changeCurrLang(self):
        self.currentTab.localLang=self.currentTab.currLangChangeWindow.gb.checkedButton().text()
        self.currentTab.currLangValue.setText(self.currentTab.localLang)
        self.currentTab.currLangChangeWindow.hide()
    def computeFP(self):
        self.currentTab.fpData.weights.clear()
        self.currentTab.fpData.inputs.clear()
        self.currentTab.fpData.outputs.clear()
        sum=0
        for comp in self.currentTab.fpComponents:
            wt=0
            for r in comp["radioComps"]:
                if r.isChecked():
                    wt=int(r.text())
                    self.currentTab.fpData.weights.append(wt)
            counttxt=comp["countComp"].text()
            self.currentTab.fpData.inputs.append(counttxt)
            if len(counttxt)>0:
                val=wt*int(counttxt)
            else:
                val=0
            self.currentTab.fpData.outputs.append(val)
            sum+=val
            comp["outputComp"].setText(str(val))
        self.currentTab.totalCountOp.setText(str(sum))
        self.currentTab.fpData.inputTotal=sum
        vaf=int(self.currentTab.vafOutput.text())
        self.currentTab.fpData.vafCount=vaf
        fp = sum*(0.65+(0.01*vaf))
        fp=round(fp,2)
        self.currentTab.fpData.computedFP=fp
        self.currentTab.fpOutput.setText(str(fp))
    def clickLangDone(self):
        self.lang.selectedLang=self.lang.gb.checkedButton().text()
        #if len(self.lang.selectedLang)>0:
        #    self.currentTab.fpData.preferredLanguage=self.lang.selectedLang
        self.lang.close()
    def calculateCodeSize(self):
        fp=float(self.currentTab.fpOutput.text())
        loc=self.locPerFP[self.currentTab.localLang]
        op=fp*loc
        op=round(op)
        self.currentTab.fpData.codeSize=op
        self.currentTab.codeSizeOutput.setText(str(op))

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "",
         #                                         "All Files (*);;Text Files (*.txt);;MS Files(*.ms)", options=options)
        file = open(self.pName+'.ms', 'w')
        tabList=[]
        for t in range(0,self.tabs.count()):
            tab=self.tabs.widget(t)
            if tab.fpData:
                tab.fpData.projectName = self.pName
                tab.fpData.tabName = self.tabNames[t]
                tab.fpData.currLang = tab.localLang
                d = vars(tab.fpData)
            elif tab.ucpData:
                tab.ucpData.projectName = self.pName
                tab.ucpData.tabName = self.tabNames[t]
                d = vars(tab.ucpData)
            elif tab.smiData:
                tab.smiData.projectName = self.pName
                tab.smiData.tabName = self.tabNames[t]
                d = vars(tab.smiData)
            tabList.append(d)
        jsonDump = json.dumps(tabList)
        file.write(jsonDump)
        file.close()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("File saved successfully as " + self.pName + ".ms")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName,_= QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "MS Files(*.ms)", options=options)

        file = open(fileName, 'r')
        jsonDump=file.read()
        self.d=json.loads(jsonDump)
        self.createNewProject()
        for tab in self.d:
            if tab["type"] == "FP":
                newTab=FPTabs()
                newTab.fpData.projectName = tab["projectName"]
                self.lang.selectedLang = tab["preferredLanguage"]
                newTab.currLangValue.setText(tab["currLang"])
                newTab.localLang = tab["currLang"]
                newTab.computeFPbtn.clicked.connect(self.computeFP)
                newTab.changeLangBtn.clicked.connect(self.changeLanguageWindow)
                newTab.vafBtn.clicked.connect(self.createVafForm)
                self.currentTab = newTab
                self.createVafForm()
                self.currentTab.saveVafWidget.hide()
                pts = [0, 1, 2, 3, 4, 5]
                for vafCombo, vafvalue in zip(self.currentTab.vafCombos, tab["vafValues"]):
                    vafCombo.setCurrentIndex(pts.index(vafvalue))
                    self.currentTab.fpData.vafValues.append(vafvalue)
                newTab.codeSizeBtn.clicked.connect(self.calculateCodeSize)
                newTab.fpOutput.setText(str(tab["computedFP"]))
                newTab.fpData.computedFP = tab["computedFP"]
                newTab.totalCountOp.setText(str(tab["inputTotal"]))
                newTab.fpData.inputTotal = tab["inputTotal"]
                newTab.vafOutput.setText(str(tab["vafCount"]))
                newTab.fpData.vafCount = tab["vafCount"]
                newTab.codeSizeOutput.setText(str(tab["codeSize"]))
                newTab.fpData.codeSize = tab["codeSize"]
                index = 0
                for c in newTab.fpComponents:
                    weight = str(tab["weights"][index])
                    newTab.fpData.weights = tab["weights"]
                    for r in c["radioComps"]:
                        if r.text() == weight:
                            r.setChecked(True)
                    c["countComp"].setText(str(tab["inputs"][index]))
                    newTab.fpData.inputs = tab["inputs"]
                    c["outputComp"].setText(str(tab["outputs"][index]))
                    newTab.fpData.outputs = tab["outputs"]
                    index += 1
                self.tabs.addTab(newTab, tab["tabName"])
                newTab.fpData.tabName = tab["tabName"]
                self.tabNames.append(tab["tabName"])
                self.currentTab = self.tabs.currentWidget()
            elif tab["type"] == "UCP":
                newTab=UCPTabs()
                newTab.ucpData.projectName = tab["projectName"]
                newTab.tcfBtn.clicked.connect(self.createTcfForm)
                newTab.ecfBtn.clicked.connect(self.createEcfForm)
                newTab.uucwBtn.clicked.connect(self.createUucwGrid)
                newTab.uawBtn.clicked.connect(self.createUawGrid)

                self.currentTab = newTab
                self.createTcfForm()
                self.createEcfForm()
                self.createUucwGrid()
                self.createUawGrid()
                self.currentTab.saveTcfWidget.hide()
                self.currentTab.saveEcfWidget.hide()
                self.currentTab.saveUucwWidget.hide()
                self.currentTab.saveUawWidget.hide()
                pts = [0,1,2,3,4,5]
                for tcfCombo, tcfCmp in zip(self.currentTab.tcfComplexity, tab["tcfFactors"]):
                    tcfCombo.setCurrentIndex(pts.index(tcfCmp))
                    self.currentTab.ucpData.tcfFactors.append(tcfCmp)

                self.currentTab.tcfOutput.setText(str(tab["tcfOutput"]))
                self.currentTab.ucpData.tcfOutput = tab["tcfOutput"]

                for ecfCombo, ecfCmp in zip(self.currentTab.ecfComplexity, tab["ecfFactors"]):
                    ecfCombo.setCurrentIndex(pts.index(ecfCmp))
                    self.currentTab.ucpData.ecfFactors.append(ecfCmp)
                self.currentTab.ecfOutput.setText(str(tab["ecfOutput"]))
                self.currentTab.ucpData.ecfOutput = tab["ecfOutput"]

                for uucwCombo, uucwUsecase in zip(self.currentTab.uucwUseCases, tab["uucwUseCases"]):
                    uucwCombo.setText(str(uucwUsecase))
                    self.currentTab.ucpData.uucwUseCases.append(uucwUsecase)
                self.currentTab.uucwOutput.setText(str(tab["uucwOutput"]))
                self.currentTab.ucpData.uucwOutput = tab["uucwOutput"]

                for uawCombo, uawActor in zip(self.currentTab.uawActors, tab["uawActors"]):
                    uawCombo.setText(str(uawActor))
                    self.currentTab.ucpData.uawActors.append(uawActor)
                self.currentTab.uawOutput.setText(str(tab["uawOutput"]))
                self.currentTab.ucpData.uawOutput = tab["uawOutput"]

                self.currentTab.uucpOutput.setText(str(tab["uucpOutput"]))
                self.currentTab.ucpData.uucpOutput = tab["uucpOutput"]
                self.currentTab.totalUcpOutput.setText(str(tab["ucpOutput"]))
                self.currentTab.ucpData.ucpOutput = tab["ucpOutput"]
                self.currentTab.locperpm.setText(str(tab["locperpm"]))
                self.currentTab.ucpData.locperpm = tab["locperpm"]
                self.currentTab.locperucp.setText(str(tab["locperucp"]))
                self.currentTab.ucpData.locperucp = tab["locperucp"]
                self.currentTab.estimatedLoc.setText(str(tab["estimatedLoc"]))
                self.currentTab.ucpData.estimatedLoc = tab["estimatedLoc"]
                self.currentTab.estimatedHours.setText(str(tab["estimatedHours"]))
                self.currentTab.ucpData.estimatedHours = tab["estimatedHours"]
                self.currentTab.estimatedPm.setText(str(tab["pm"]))
                self.currentTab.ucpData.pm = tab["pm"]
                self.currentTab.pf.setText(str(tab["pf"]))
                self.currentTab.ucpData.pf = tab["pf"]
                self.currentTab.ucpData.estimatedPm = tab["pm"]

                self.tabs.addTab(newTab, tab["tabName"])
                newTab.ucpData.tabName = tab["tabName"]
                self.tabNames.append(tab["tabName"])
                self.currentTab = self.tabs.currentWidget()

            elif tab["type"] == "SMI":
                name = 'SMI'
                newTab = SMITab()
                self.currentTab = newTab
                self.smiTab = newTab
                self.currentTab.smiData.projectName = tab["projectName"]
                self.currentTab.smiData.values = tab["values"]
                for index, row in enumerate(tab["values"]):
                    self.currentTab.addRow()
                    self.currentTab.table.item(index, 0).setText(str(row[0]))
                    self.currentTab.table.item(index, 1).setText(str(row[1]))
                    self.currentTab.table.item(index, 2).setText(str(row[2]))
                    self.currentTab.table.item(index, 3).setText(str(row[3]))
                    self.currentTab.table.item(index, 4).setText(str(row[4]))
                self.tabs.addTab(newTab, tab["tabName"])
                newTab.smiData.tabName = tab["tabName"]
                self.tabNames.append(tab["tabName"])
                self.currentTab = self.tabs.currentWidget()






def main():
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
