from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, \
    QFormLayout, QHBoxLayout, QLineEdit, QButtonGroup, QRadioButton, QGridLayout

from FpData import FpData


class FPTabs(QWidget):

    def __init__(self):
        super().__init__()
        self.vafCombos=[]
        self.saveVafWidget=QWidget()
        self.gridLayout=QGridLayout()
        self.codeSizeOutput = QLineEdit()
        self.localLang=''
        self.currLangValue = QLineEdit()
        self.codeSizeBtn = QPushButton('Compute Code Size')
        self.totalCountOp=QLineEdit()
        self.fpComponents=[]
        self.fpOutput = QLineEdit()
        self.computeFPbtn = QPushButton('Compute FP')
        self.vaf = QWidget()
        self.vafOutput = QLineEdit()
        self.vafBtn = QPushButton('Value Adjustments')
        self.changeLangBtn = QPushButton('Change language')
        self.currLangChangeWindow=None
        self.fpData=FpData()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        title = QLabel('Weighting Factors')
        #title.setAlignment(Qt.AlignHCenter)
        title.setFont(QFont('Arial', 20))
        types = QLabel('Simple      Average     Complex')
        #types.setAlignment(Qt.AlignHCenter)
        types.setFont(QFont('Arial', 20))
        layout.addWidget(title)
        self.gridLayout.addWidget(title,0,2)
        #layout.addStretch()
        #layout.addWidget(types)
        self.gridLayout.addWidget(types,1,2)
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


        factors=['External Inputs','External Outputs', 'External Inquiries', 'Internal Logical Files', 'External Interface Files']

        simpleWeights=['3','4','3','7','5']
        averageWeights=['4','5','4','10','7']
        complexWeights=['6','7','6','15','10']
        weights=[simpleWeights,averageWeights,complexWeights]

        index=0

        for factor in factors:
            self.formlayout.addRow(self.createRow(factor,weights[0][index],weights[1][index],weights[2][index],index))
            index+=1

        totalCountWidget=QWidget()
        rowLayout=QHBoxLayout()
        totalCountText=QLabel('Total Count: ')
        rowLayout.addWidget(totalCountText)
        self.gridLayout.addWidget(totalCountText,index+2,0)
        rowLayout.addStretch(2)
        rowLayout.addWidget(self.totalCountOp)
        self.gridLayout.addWidget(self.totalCountOp, index+2, 3)
        index+=1
        totalCountWidget.setLayout(rowLayout)
        self.formlayout.addRow(totalCountWidget)

        computeFP = QWidget()
        rowLayout = QHBoxLayout()

        rowLayout.addWidget(self.computeFPbtn)
        self.gridLayout.addWidget(self.computeFPbtn, index+2, 0)
        rowLayout.addStretch(2)
        rowLayout.addWidget(self.fpOutput)
        self.gridLayout.addWidget(self.fpOutput, index+2, 3)
        index+=1
        computeFP.setLayout(rowLayout)
        self.formlayout.addRow(computeFP)

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(self.vafBtn)
        self.gridLayout.addWidget(self.vafBtn, index+2, 0)
        rowLayout.addStretch(2)
        self.vafOutput.setText('0')
        rowLayout.addWidget(self.vafOutput)
        self.gridLayout.addWidget(self.vafOutput, index+2, 3)
        index+=1
        self.vaf.setLayout(rowLayout)
        self.formlayout.addRow(self.vaf)

        self.vafOutput.setReadOnly(True)
        self.totalCountOp.setReadOnly(True)
        self.fpOutput.setReadOnly(True)
        self.codeSizeOutput.setReadOnly(True)
        self.currLangValue.setReadOnly(True)

        codeSize = QWidget()
        rowLayout = QHBoxLayout()
        currLang = QLabel('Current Language')
        rowLayout.addWidget(self.codeSizeBtn)
        self.gridLayout.addWidget(self.codeSizeBtn, index+2, 0)
        rowLayout.addStretch(2)
        rowLayout.addWidget(currLang)
        self.gridLayout.addWidget(currLang, index+2, 1)
        rowLayout.addWidget(self.currLangValue)
        self.gridLayout.addWidget(self.currLangValue, index+2, 2)
        rowLayout.addStretch(2)
        rowLayout.addWidget(self.codeSizeOutput)
        self.gridLayout.addWidget(self.codeSizeOutput, index+2, 3)
        index+=1
        codeSize.setLayout(rowLayout)
        self.formlayout.addRow(codeSize)

        changeLang=QWidget()

        rowLayout = QHBoxLayout()
        self.changeLangBtn.setFixedSize(170,30)

        rowLayout.addWidget(self.changeLangBtn)
        self.gridLayout.addWidget(self.changeLangBtn, index+2, 0)
        rowLayout.addStretch(3)
        changeLang.setLayout(rowLayout)
        self.formlayout.addRow(changeLang)


    def createRow(self,factor,simple,average,complex,index):
        valueComps={}
        valueComps["radioComps"]=[]
        w=QWidget()
        rowLayout = QHBoxLayout()
        label = QLabel(factor+': ')
        countText = QLineEdit()
        reg_ex = QRegExp("[0-9]+")
        input_validator = QRegExpValidator(reg_ex, countText)
        countText.setValidator(input_validator)
        valueComps["countComp"]=countText
        op = QLineEdit()
        op.setReadOnly(True)
        radioGroup = QButtonGroup(self)
        radioLayout = QHBoxLayout()
        radioLayout.setSpacing(80)
        radioLayout.setAlignment(Qt.AlignHCenter)
        r1 = QRadioButton(simple)
        valueComps["radioComps"].append(r1)
        r2 = QRadioButton(average)
        valueComps["radioComps"].append(r2)
        r2.setChecked(True)
        r3 = QRadioButton(complex)
        valueComps["radioComps"].append(r3)
        radioLayout.addWidget(r1)
        radioLayout.addWidget(r2)
        radioLayout.addWidget(r3)
        radioGroup.addButton(r1)
        radioGroup.addButton(r2)
        radioGroup.addButton(r3)
        rowLayout.addWidget(label)
        self.gridLayout.addWidget(label,index+2,0)
        rowLayout.addWidget(countText)
        self.gridLayout.addWidget(countText, index+2, 1)
        #rowLayout.addLayout(radioLayout)
        self.gridLayout.addLayout(radioLayout, index+2, 2)
        rowLayout.addWidget(op)
        self.gridLayout.addWidget(op,index+2,3)
        valueComps["outputComp"]=op
        w.setLayout(rowLayout)
        self.fpComponents.append(valueComps)
        return w

