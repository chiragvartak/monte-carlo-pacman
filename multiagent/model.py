from collections import namedtuple
from featureBasedGameState import FeatureBasedGameState

ModelEntry = namedtuple('ModelEntry', "nWins pseudoWins nSimulations avgReward")

class Model(object):
    def __init__(self):
        self.data = {}

    def getPseudoWins(self, avgReward):
            wValue = max(0, avgReward + 600)  # Scores less than -600 are effectively 0
            wValue = wValue / 10
            return wValue

    def updateEntry(self, fbgs, actionTaken, nWins, nSimulations, avgReward):
        # type: (FeatureBasedGameState, str, int, int, float) -> None
        pseudoWins = self.getPseudoWins(avgReward)
        self.data[(fbgs, actionTaken)] = ModelEntry(nWins=nWins, pseudoWins=pseudoWins,
                                                    nSimulations=nSimulations, avgReward=avgReward)

    def writeModelToFile(self, file="model.txt"):
        with open(file, 'w') as f:
            for key, value in self.data.items():
                f.write(str(key) + ": " + str(value) + "\n")



commonModel = Model()