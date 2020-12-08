# Model-Based Monte Carlo Tree Search For Pacman

## Environment Details

All our code has been tested with Python 2 (2.7.18 to be precise). We do not use any version specific libraries so any
Python 2 (>=2.7) should be fine.

## Instructions
0) You need to be present in the `multiagent/` directory to run all the commands below.

1) (Optional) Train the Pacman agent by running the Monte-Carlo Tree Search simulations.  
   You can skip this step. In that case, the trained model we have included will be used for playing the games.
   Prefer running training games on the `smallStandard`. It is especially made for training.
```bash
python pacman.py --numTraining 10000 -q -p MCTSAgent -l smallStandard -n 10000
```
The trained model will be saved to `models/model-latest.pkl`.  
A robust model which has been well-trained has already been provided. It is named `models/perfect-model.pkl`.  
If you do not make any changes to the `constants.py` config parameters. This model will be used as the base model, even
for the training, and for playing your games after that.


2) Using a created model for playing games
and then run your game:
```bash
python pacman.py --numTraining 0 -q -p MCTSAgent -l trickyFoodsFar -n 100
```

## File Description

`multiagents.py` - contains the `MCTSAgent` which implements the Monte-Carlo Tree Search algorithm

`featureBasedGameState.py` - feature-based representation of a game state

`model.py` - storing, retrieving and using the generated model for playing games

`search.py` - search algorthims from project 1 (A-Star search) are used to generate some features required for
game state representation

`searchAgents.py` - the search problems present here are used for some feature extractions

`layoutTransformer.py` - used to generate random layouts for performance analysis and debugging

## Layouts

We have provided varied layouts for you to try and see how the `MCTSAgent` works:

1) `testClassic`
2) `smallClassic`
3) `mediumClassic`
4) `bigClassic`
5) `trickyFoodsFar`
6) `openClassic2`
7) `franksClassic`
8) `openClassic`
