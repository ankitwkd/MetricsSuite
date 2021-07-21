from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QStandardItemModel, QRegExpValidator
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, \
    QFormLayout, QHBoxLayout, QLineEdit, QButtonGroup, QRadioButton, QGridLayout, QTableWidget, QTableWidgetItem, \
    QTableView, QInputDialog, QMessageBox

from SmiData import SmiData


class SMITab(QWidget):

    def __init__(self):
        super().__init__()

        self.gridLayout=QGridLayout()

        self.smiData=SmiData()
        self.fpData=None
        self.ucpData=None
        self.rowCount = 0
        self.totalTillRow = []
        self.totalModules = []
        self.flag = False
        # layout = QVBoxLayout(self)
        # layout.setAlignment(Qt.AlignTop)
        # layout.setContentsMargins(0,0,0,0)

        title = QLabel('Software Maturity Index')

        title.setFont(QFont('Arial', 20))

        # layout.addWidget(title)
        self.gridLayout.addWidget(title)
        self.createForm()
        # layout.addLayout(self.gridLayout)

        self.setLayout(self.vbox)





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
        # creating a table widget
        self.table = QTableWidget(0, 5);
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 110)
        self.table.setColumnWidth(2, 110)
        self.table.setColumnWidth(3, 110)
        self.table.setColumnWidth(4, 110)
        self.table.cellChanged.connect(self.changedCell)
        self.table.setHorizontalHeaderLabels(['SMI', 'Modules Added', 'Modules Changed', 'Modules Deleted', 'Total Modules'])
        self.gridLayout.addWidget(self.table)

        self.addRowBtn = QPushButton('Add Row')
        self.addRowBtn.clicked.connect(self.addRow)
        self.computeIndexBtn = QPushButton('Compute Index')
        self.computeIndexBtn.clicked.connect(self.computeIndex)

        self.vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.addRowBtn)
        hbox.addWidget(self.computeIndexBtn)
        self.vbox.addLayout(self.gridLayout)
        self.vbox.addLayout(hbox)



        index = 0


    def computeIndex(self):
        self.table.reset()
        self.smiData.values.clear()
        for r in range(self.rowCount):
            added = int(self.table.item(r, 1).text())
            changed = int(self.table.item(r, 2).text())
            deleted = int(self.table.item(r, 3).text())
            total = int(self.table.item(r, 4).text())
            if total == 0:
                msg = QMessageBox()
                msg.move(300,200)
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Total is 0, please enter values")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
            else:
                smi = (total - (added+changed+deleted)) / total
                self.table.setItem(r, 0, QTableWidgetItem(str(smi)))
                self.table.item(r, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.smiData.values.append([smi,added,changed,deleted,total])

    def addRow(self):
        self.table.insertRow(self.rowCount)
        self.initializeRow()
        self.rowCount = self.rowCount + 1

        #tbl.setItem(inx, 0, QTableWidgetItem(str(row[0])))

    def initializeRow(self):
        r = self.rowCount
        self.table.setItem(r, 0, QTableWidgetItem('0.0'))
        self.table.setItem(r, 1, QTableWidgetItem('0'))
        self.table.setItem(r, 2, QTableWidgetItem('0'))
        self.table.setItem(r, 3, QTableWidgetItem('0'))
        total = '0'
        if r>0:
            total = self.table.item(r-1, 4).text()
        self.table.setItem(r, 4, QTableWidgetItem(total))
        self.table.item(r, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.item(r, 4).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def changedCell(self, row):
        try:
            self.table.cellChanged.disconnect()
            for r in range(self.rowCount):

                addedTextItem = self.table.item(r, 1)
                if addedTextItem and addedTextItem.text()!='':
                    added = int(addedTextItem.text())
                else:
                    self.table.setItem(r, 1, QTableWidgetItem('0'))
                    added = 0

                changedTextItem = self.table.item(r, 2)
                if changedTextItem and changedTextItem.text() != '':
                    changed = int(changedTextItem.text())
                else:
                    self.table.setItem(r, 2, QTableWidgetItem('0'))
                    changed = 0

                deletedTextItem = self.table.item(r, 3)
                if deletedTextItem and deletedTextItem.text() != '':
                    deleted = int(deletedTextItem.text())
                else:
                    self.table.setItem(r, 3, QTableWidgetItem('0'))
                    deleted = 0
                total = added - deleted
                if r > 0:
                    total = total + int(self.table.item(r-1, 4).text())
                self.table.setItem(r, 4, QTableWidgetItem(str(total)))
                self.table.item(r, 4).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                # smi = (total - (added+changed+deleted)) / total
                # self.table.setItem(r, 0, QTableWidgetItem(str(smi)))

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter a valid value")
            self.table.currentItem().setText('0')
            msg.exec()
        finally:
            self.table.cellChanged.connect(self.changedCell)
            return

    def createRow(self,factor,simple,average,complex,index):
        valueComps={}
        valueComps["radioComps"]=[]
        w=QWidget()
        rowLayout = QHBoxLayout()
        label = QLabel(factor+': ')
        countText = QLineEdit()
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



