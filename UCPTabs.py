from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, \
    QFormLayout, QHBoxLayout, QLineEdit, QButtonGroup, QRadioButton, QGridLayout

from UcpData import UcpData


class UCPTabs(QWidget):

    def __init__(self):
        super().__init__()

        self.tcfFactors=[]
        self.tcfWeights=[]
        self.tcfComplexity=[]
        self.saveTcfWidget=QWidget()

        self.ecfFactors = []
        self.ecfWeights = []
        self.ecfComplexity = []
        self.saveEcfWidget = QWidget()


        self.gridLayout=QGridLayout()

        self.tcf = QWidget()
        self.tcfOutput = QLineEdit()
        self.tcfBtn = QPushButton('Compute TCF')

        self.ecf = QWidget()
        self.ecfOutput = QLineEdit()
        self.ecfBtn = QPushButton('Compute ECF')

        self.uucw = QWidget()
        self.uucwOutput = QLineEdit()
        self.uucwBtn = QPushButton('Compute UUCW')

        self.uucwUseCases = []
        self.uucwResult = []
        self.saveUucwWidget = QWidget()

        self.uawActors = []
        self.uawResult = []
        self.saveUawWidget = QWidget()



        self.uaw = QWidget()
        self.uawOutput = QLineEdit()
        self.uawBtn = QPushButton('Compute UAW')

        self.uucp = QWidget()
        self.uucpOutput = QLineEdit()
        self.uucpBtn = QPushButton('Compute UUCP')
        self.uucpBtn.clicked.connect(self.computeUucp)

        self.pf = QLineEdit();
        self.locperpm = QLineEdit();
        self.locperucp = QLineEdit();

        self.totalUcpOutput = QLineEdit();
        self.totalUcpOutput.setReadOnly(True)
        self.ucpBtn = QPushButton('Compute UCP')
        self.ucpBtn.clicked.connect(self.computeUcp)

        self.estimatedHours = QLineEdit();
        self.estimatedLoc = QLineEdit();
        self.estimatedPm = QLineEdit();



        self.ucpData=UcpData()
        self.fpData=None
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        title = QLabel('Use Case Points')

        title.setFont(QFont('Arial', 20))

        layout.addWidget(title)
        self.gridLayout.addWidget(title,0,2)
        self.createForm()
        #layout.addLayout(self.formlayout)
        layout.addLayout(self.gridLayout)

        self.setLayout(layout)





    # def addTab(self):
    #     tab1 = QWidget()
    #     self.tabs.resize(1000, 800)
    #
    #     # Add tabs
    #     self.tabs.addTab(tab1, "Function Points")
    #     # Create first tab
    #     layout = QVBoxLayout()
    #     title=QLabel('Weighting Factors')
    #     title.setFont(QFont('Arial',15))
    #     types=QLabel('Simple    Average    Complex')
    #     types.setFont(QFont('Arial',25))
    #     layout.addWidget(title)
    #     layout.addWidget(types)
    #     self.createForm()
    #     layout.addLayout(self.formlayout)
    #
    #
    #     tab1.setLayout(layout)
    #
    #     # Add tabs to widget
    #     self.layout().addWidget(self.tabs)
    def createForm(self):
        # creating a form layout
        self.formlayout = QFormLayout()
        self.formlayout.setLabelAlignment(Qt.AlignLeft)
        self.formlayout.setContentsMargins(0,0,0,0)
        info_label = "approx.  *Rounded to nearest integer"
        round_label = "approx. *Rounded to 2 decimal places"

        index = 0

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(self.tcfBtn)
        self.gridLayout.addWidget(self.tcfBtn, index+2, 0)

        rowLayout.addStretch(2)
        totalTcf = QLabel('Total TCF')
        self.gridLayout.addWidget(totalTcf, index+2, 2)
        self.tcfOutput.setText('0')
        rowLayout.addWidget(self.tcfOutput)
        self.gridLayout.addWidget(self.tcfOutput, index+2, 3)
        self.gridLayout.addWidget(QLabel(round_label), index+2, 4)
        index+=1
        self.tcf.setLayout(rowLayout)
        self.formlayout.addRow(self.tcf)

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(self.ecfBtn)
        self.gridLayout.addWidget(self.ecfBtn, index + 2, 0)
        totalEcf = QLabel('Total ECF')

        self.gridLayout.addWidget(totalEcf, index + 2, 2)
        rowLayout.addStretch(2)
        self.ecfOutput.setText('0')
        rowLayout.addWidget(self.ecfOutput)
        self.gridLayout.addWidget(self.ecfOutput, index + 2, 3)
        self.gridLayout.addWidget(QLabel(round_label), index + 2, 4)
        index += 1
        self.ecf.setLayout(rowLayout)
        self.formlayout.addRow(self.ecf)

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(self.uucwBtn)
        self.gridLayout.addWidget(self.uucwBtn, index + 2, 0)

        rowLayout.addStretch(2)
        totalUucw = QLabel('Total UUCW')
        self.gridLayout.addWidget(totalUucw, index + 2, 2)
        self.uucwOutput.setText('0')
        rowLayout.addWidget(self.uucwOutput)
        self.gridLayout.addWidget(self.uucwOutput, index + 2, 3)
        index += 1
        self.uucw.setLayout(rowLayout)
        self.formlayout.addRow(self.uucw)

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(self.uawBtn)
        self.gridLayout.addWidget(self.uawBtn, index + 2, 0)

        rowLayout.addStretch(2)
        totalUaw = QLabel('Total UAW')
        self.gridLayout.addWidget(totalUaw, index + 2, 2)
        self.uawOutput.setText('0')
        rowLayout.addWidget(self.uawOutput)
        self.gridLayout.addWidget(self.uawOutput, index + 2, 3)
        index += 1
        self.uaw.setLayout(rowLayout)
        self.formlayout.addRow(self.uaw)

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(self.uucpBtn)
        self.gridLayout.addWidget(self.uucpBtn, index + 2, 0)

        rowLayout.addStretch(2)
        totalUucp = QLabel('Total UUCP')
        self.gridLayout.addWidget(totalUucp, index + 2, 2)
        self.uucpOutput.setText('0')
        rowLayout.addWidget(self.uucpOutput)
        self.gridLayout.addWidget(self.uucpOutput, index + 2, 3)
        index += 1
        self.uucp.setLayout(rowLayout)
        self.formlayout.addRow(self.uucp)


        pf = QLabel('Productivity Factor')
        self.gridLayout.addWidget(pf, index + 2, 0)
        self.pf.setText('20')
        self.gridLayout.addWidget(self.pf, index + 2, 2)
        index += 1

        locperpm = QLabel('LOC/PM')
        self.gridLayout.addWidget(locperpm, index + 2, 0)
        self.locperpm.setText('700')
        self.gridLayout.addWidget(self.locperpm, index + 2, 2)
        index += 1

        locperucp = QLabel('LOC/UCP')
        self.gridLayout.addWidget(locperucp, index + 2, 0)
        self.locperucp.setText('100')
        self.gridLayout.addWidget(self.locperucp, index + 2, 2)
        index += 1

        ucp = QLabel('Total UCP')
        self.gridLayout.addWidget(self.ucpBtn, index + 2, 0)
        self.totalUcpOutput.setText('0')
        self.gridLayout.addWidget(ucp, index + 2, 2)
        self.gridLayout.addWidget(self.totalUcpOutput, index + 2, 3)
        self.gridLayout.addWidget(QLabel(round_label), index + 2, 4)
        index += 1

        estimatedHours = QLabel('Estimated Hours')
        self.gridLayout.addWidget(estimatedHours, index + 2, 0)
        self.estimatedHours.setText('0')
        self.gridLayout.addWidget(self.estimatedHours, index + 2, 2)
        self.gridLayout.addWidget(QLabel(info_label), index + 2, 3)
        index += 1

        estimatedLoc = QLabel('Estimated LOC')
        self.gridLayout.addWidget(estimatedLoc, index + 2, 0)
        self.estimatedLoc.setText('0')
        self.gridLayout.addWidget(self.estimatedLoc, index + 2, 2)
        self.gridLayout.addWidget(QLabel(info_label), index + 2, 3)
        index += 1

        estimatedPm = QLabel('Estimated PM')
        self.gridLayout.addWidget(estimatedPm, index + 2, 0)
        self.estimatedPm.setText('0')
        self.gridLayout.addWidget(self.estimatedPm, index + 2, 2)
        self.gridLayout.addWidget(QLabel(info_label), index + 2, 3)
        index += 1


        self.tcfOutput.setReadOnly(True)
        self.ecfOutput.setReadOnly(True)
        self.uucwOutput.setReadOnly(True)
        self.uawOutput.setReadOnly(True)
        self.uucpOutput.setReadOnly(True)
        self.totalUcpOutput.setReadOnly(True)
        self.estimatedHours.setReadOnly(True)
        self.estimatedLoc.setReadOnly(True)
        self.estimatedPm.setReadOnly(True)

        reg_ex = QRegExp("[0-9]+")
        input_validator = QRegExpValidator(reg_ex, self.pf)
        self.pf.setValidator(input_validator)

        input_validator = QRegExpValidator(reg_ex, self.locperpm)
        self.locperpm.setValidator(input_validator)

        input_validator = QRegExpValidator(reg_ex, self.locperucp)
        self.locperucp.setValidator(input_validator)




    def computeUucp(self):
        uucp = int(self.uucwOutput.text()) + int(self.uawOutput.text())
        self.uucpOutput.setText(str(uucp))
        self.ucpData.uucpOutput = uucp


    def computeUcp(self):
        pf = int(self.pf.text())
        self.ucpData.pf = pf
        ucp = round(float(self.tcfOutput.text())*float(self.ecfOutput.text())*float(self.uucpOutput.text()),2)
        self.totalUcpOutput.setText(str(ucp))
        self.ucpData.ucpOutput = ucp

        est_hrs = round((ucp * pf))
        self.estimatedHours.setText(str(est_hrs))
        self.ucpData.estimatedHours = est_hrs

        if self.locperucp.text()=='':
            locperucp = 100
        else:
            locperucp = int(self.locperucp.text())
        self.ucpData.locperucp = locperucp

        if self.locperpm == '':
            locperpm = 700
        else:
            locperpm = int(self.locperpm.text())
        self.ucpData.locperpm = locperpm

        loc = round(locperucp * ucp)
        self.estimatedLoc.setText(str(loc))
        self.ucpData.estimatedLoc = loc

        pm = round((loc/locperpm))
        self.estimatedPm.setText(str(pm))
        self.ucpData.pm = pm

