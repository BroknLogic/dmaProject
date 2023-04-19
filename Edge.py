class Edge:
    def __init__(self, source: str, target: str, mean, stdDev):
        self.target = target
        self.source = source
        self.mean = mean
        self.stdDev = stdDev
        
    def getId(self) -> str:
        return self.source + '__' + self.target
    
    def getTarget(self) -> str:
        return self.target
    
    def getSource(self) -> str:
        return self.source
    
    def getWidth(self):
        self.mean
        
    def randParams(self) -> tuple:
        return (self.mean, self.stdDev)
    
    def toDict(self) -> dict[str, str]:
        return {'data':{
            'label': self.getId(),
            'source': self.source,
            'target': self.target,
            'width': self.mean,
            'mean': str(self.mean),
            'stdDev': str(self.stdDev),}
            }
        
    def __str__(self) -> str:
        return self.getId()
    
    def __lt__(self, other) -> bool:
        return self.getId() < other.getId()