from collections import namedtuple
from featureBasedGameState import FeatureBasedGameState

ModelEntry = namedtuple('ModelEntry', "nWins nSimulations avgReward")

class Model(object):
    def __init__(self):
        self.data = {}

    def updateEntry(self, fbgs, actionTaken, nWins, nSimulations, avgReward):
        # type: (FeatureBasedGameState, str, int, int, float) -> None
        self.data[(fbgs, actionTaken)] = ModelEntry(nWins=nWins,
                                                    nSimulations=nSimulations, avgReward=avgReward)

    def writeModelToFile(self, file="model.txt"):
        with open(file, 'w') as f:
            for key, value in self.data.items():
                f.write(str(key) + ": " + str(value) + "\n")

commonModel = Model()