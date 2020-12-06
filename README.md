# Notes of the MCTS parts

First things first:
1) Take a look at the `constants.py` file. You can choose to use an existing model, or not. Details are in `constants.py`
2) If you add features to the `featureBasedGameState.py`, there are multiple places you will need to make changes in
there. This is indicated by the comments in there.

### Run training games and generate a model
(Prefer running training games on the `smallStandard`. It is made for that)
```bash
python pacman.py --numTraining 10000 -p MCTSAgent -l smallStandard -n 10000
```
The model is generated in the `models/` directory. It will mostly be named `model-latest.pkl`

### Using a created model for future games
Simple rename the file `model-latest.pkl` to `model.pkl` in the `models/` directory  
and then run your game:
```bash
python pacman.py --numTraining 0 -p MCTSAgent -l bigClassic -n 10
```
Let the `--numTraining` param be present. Set it to 0 if you want. Weird things happens if it isn't present.
