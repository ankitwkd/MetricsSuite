class FpData():
    def __init__(self):
        super().__init__()
        self.type = 'FP'
        self.projectName=''
        self.preferredLanguage='C'
        self.vafValues=[]
        self.vafCount=[]
        self.inputs=[]
        self.outputs=[]
        self.weights=[]
        self.inputTotal=0
        self.computedFP=0
        self.codeSize=0
        self.tabName=''
        self.currLang=''

        self.tcfValues = []
        self.tcfCount = []
