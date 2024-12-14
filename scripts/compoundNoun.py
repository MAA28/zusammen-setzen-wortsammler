class CompoundNoun:
    def __init__(self, firstNoun, connectorParticle, secondNoun):
        self.firstNoun = firstNoun
        self.connectorParticle = connectorParticle
        self.secondNoun = secondNoun

    def __format__(self, spec):
        if self.connectorParticle == '':
            return f'{self.firstNoun} + {self.secondNoun}'
        else:
            return f'{self.firstNoun} + {self.connectorParticle} + {self.secondNoun}'

    def reconstruct(self):
        return f'{self.firstNoun}{self.connectorParticle}{self.secondNoun}'

    def toCSVLine(self):
        return f'{self.firstNoun},{self.connectorParticle},{self.secondNoun}'

    def fromCSVLine(line):
        values = line.split(',')
        return CompoundNoun(values[0], values[1], values[2])
