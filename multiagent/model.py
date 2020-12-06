from collections import namedtuple
from featureBasedGameState import FeatureBasedGameState
import pickle
from time import strftime
import constants

ModelEntry = namedtuple('ModelEntry', "nWins nSimulations avgReward pseudoWins")

class Model(object):
    def __init__(self):
        self.data = {}

    def updateEntry(self, fbgs, actionTaken, nWins, pseudoWins, nSimulations, avgReward):
        # type: (FeatureBasedGameState, str, int, float, int, float) -> None
        self.data[(fbgs, actionTaken)] = ModelEntry(nWins=nWins, pseudoWins=pseudoWins,
                                                    nSimulations=nSimulations, avgReward=avgReward)

    def writeModelToFile(self, file):
        with open(file, 'w') as f:
            for key, value in self.data.items():
                f.write(str(key) + ": " + str(value) + "\n")
        self.saveModel(constants.OUTPUT_MODEL)

    def saveModel(self, outputModelFilePath):
        filename = outputModelFilePath
        with open(filename, 'wb') as f:
            pickle.dump(self.data, f)



def getModel(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    model = Model()
    model.data = data
    return model


commonModel = None
if constants.MODEL_TO_USE is not None:
    commonModel = getModel(constants.MODEL_TO_USE)
else:
    commonModel = Model()