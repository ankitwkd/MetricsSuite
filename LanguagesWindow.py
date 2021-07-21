from PyQt5.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel, QButtonGroup, QPushButton


class Languages(QWidget):

    def __init__(self):
        super().__init__()
        self.availableLang=['Assembled','ADA 95', 'C', 'C++','C#', 'COBOL', 'FORTRAN', 'HTML', 'Java', 'Javascript', 'VBScript', 'VirtualBasic']
        self.gb=QButtonGroup(self)

        self.selectedLang='C'
        self.button = QPushButton('Done', self)
        self.initUI()

    def initUI(self):
        vbox1 = QVBoxLayout()
        vbox1.addWidget(QLabel("Select one language"))
        vbox1.addStretch()
        vbox2 = QVBoxLayout()
        for l in self.availableLang:
            cb=QCheckBox()
            cb.setText(l)
            if l=='C':
                cb.setChecked(True)
            self.gb.addButton(cb)
            vbox2.addWidget(cb)
            vbox2.addStretch()
        vbox1.addLayout(vbox2)
        vbox1.addWidget(self.button)
        self.setLayout(vbox1)
        self.setGeometry(300,300,300,300)
        self.move(300,200)