class UcpData():
    def __init__(self):
        super().__init__()
        self.type='UCP'
        self.projectName=''
        self.tabName = ''

        self.tcfWeights = []
        self.tcfFactors = []
        self.tcfValues = []
        self.tcfOutput = 0.0
        self.tcfCount = []

        self.ecfValues = []
        self.ecfFactors = []
        self.ecfOutput = 0.0

        self.uucwUseCases = []
        self.uucwResults = []
        self.uucwOutput = 0

        self.uawActors = []
        self.uawResults = []
        self.uawOutput = 0

        self.uucpOutput = 0
        self.ucpOutput = 0.0
        self.estimatedHours = 0
        self.locperpm = 0
        self.locperucp = 0
        self.pm = 0
        self.estimatedLoc = 0
        self.pf = 0

