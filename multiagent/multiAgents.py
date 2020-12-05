# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
from model import commonModel
from featureBasedGameState import FeatureBasedGameState
from math import sqrt, log

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Imports
        from util import manhattanDistance as md

        # Better represented information for convenience
        newFoodList = newFood.asList()
        successorGameScore = successorGameState.getScore()

        numberOfRemainingFood = len(newFoodList)

        distanceFromFoods = [md(newPos, newFoodPos) for newFoodPos in newFoodList]
        distanceFromClosestFood = 0 if (len(distanceFromFoods) == 0) else min(distanceFromFoods)

        distancesFromGhosts = [md(newPos, ngs.getPosition()) for ngs in newGhostStates]
        distanceFromClosestGhost = 0 if (len(distancesFromGhosts) == 0) else min(distancesFromGhosts)

        finalScore = successorGameScore \
                     - (1000 if (distanceFromClosestGhost<=1) else 0) \
                     - 50*numberOfRemainingFood \
                     - distanceFromClosestFood
        return finalScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # Initializations for convenience
        utility = self.evaluationFunction
        maxDepth = self.depth

        # Helper functions for improved readability
        def terminalTest(state):
            return state.isLose() or state.isWin()

        def maxValue(state, depth):
            agentIndex = 0  # MAX player is always agent 0
            FIRST_MIN_AGENT_INDEX = 1

            if terminalTest(state) or (depth > maxDepth): return utility(state)
            v = -1000000000
            for action in state.getLegalActions(agentIndex):
                successorState = state.generateSuccessor(agentIndex, action)
                v = max(v, minValue(successorState, FIRST_MIN_AGENT_INDEX, depth))
            return v

        def minValue(state, agentIndex, depth):
            numMinAgents = state.getNumAgents() - 1

            isTerminalState = terminalTest(state)
            if isTerminalState: return utility(state)
            v = 1000000000
            for action in state.getLegalActions(agentIndex):
                successorState = state.generateSuccessor(agentIndex, action)
                if agentIndex < numMinAgents:
                    v = min(v, minValue(successorState, agentIndex+1, depth))
                else:
                    v = min(v, maxValue(successorState, depth+1))
            return v

        # Constants
        MAX_AGENT_INDEX = 0
        FIRST_MIN_AGENT_INDEX = 1
        INITIAL_DEPTH = 1

        # The actual algorithm starts here
        actions = gameState.getLegalActions(MAX_AGENT_INDEX)
        bestValue = -1000000000
        bestAction = None
        for action in actions:
            successor = gameState.generateSuccessor(MAX_AGENT_INDEX, action)
            successorMinValue = minValue(successor, FIRST_MIN_AGENT_INDEX, INITIAL_DEPTH)
            if successorMinValue > bestValue:
                bestValue = successorMinValue
                bestAction = action
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Initializations for convenience
        utility = self.evaluationFunction
        maxDepth = self.depth

        # Helper functions for improved readability
        def terminalTest(state):
            return state.isLose() or state.isWin()

        def maxValue(state, depth, alpha, beta):
            agentIndex = 0  # MAX player is always agent 0
            FIRST_MIN_AGENT_INDEX = 1

            if terminalTest(state) or (depth > maxDepth): return (utility(state), None)
            v = -1000000000
            bestAction = None
            for action in state.getLegalActions(agentIndex):
                successorState = state.generateSuccessor(agentIndex, action)
                minValueOfSuccessor, _ = minValue(successorState, FIRST_MIN_AGENT_INDEX, depth, alpha, beta)
                if minValueOfSuccessor > v:
                    v = minValueOfSuccessor
                    bestAction = action
                if v > beta: return (v, action)
                alpha = max(alpha, v)
            return (v, bestAction)

        def minValue(state, agentIndex, depth, alpha, beta):
            numMinAgents = state.getNumAgents() - 1

            isTerminalState = terminalTest(state)
            if isTerminalState: return (utility(state), None)
            v = 1000000000
            bestAction = None
            for action in state.getLegalActions(agentIndex):
                successorState = state.generateSuccessor(agentIndex, action)
                if agentIndex < numMinAgents:
                    minValueOfSuccessor, _ = minValue(successorState, agentIndex + 1, depth, alpha, beta)
                    if minValueOfSuccessor < v:
                        v = minValueOfSuccessor
                        bestAction = action
                else:
                    maxValueOfSuccessor, _ = maxValue(successorState, depth + 1, alpha, beta)
                    if maxValueOfSuccessor < v:
                        v = maxValueOfSuccessor
                        bestAction = action
                if v < alpha: return (v, action)
                beta = min(beta, v)
            return (v, bestAction)

        _, bestAction = maxValue(gameState, depth=1, alpha=-1000000000, beta=1000000000)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Initializations for convenience
        utility = self.evaluationFunction
        maxDepth = self.depth

        # Some nested helper functions for improved readability of code
        def terminalTest(state):
            return state.isLose() or state.isWin()

        def maxValue(state, depth):
            agentIndex = 0  # MAX player is always agent 0
            FIRST_MIN_AGENT_INDEX = 1

            if terminalTest(state) or (depth > maxDepth): return utility(state)
            v = -1000000000
            for action in state.getLegalActions(agentIndex):
                successorState = state.generateSuccessor(agentIndex, action)
                v = max(v, minValue(successorState, FIRST_MIN_AGENT_INDEX, depth))
            return v

        def minValue(state, agentIndex, depth):
            numMinAgents = state.getNumAgents() - 1

            isTerminalState = terminalTest(state)
            if isTerminalState: return utility(state)
            v = 0
            legalActions = state.getLegalActions(agentIndex)
            probabilityOfEachAction = 1.0 / len(legalActions)
            for action in legalActions:
                successorState = state.generateSuccessor(agentIndex, action)
                if agentIndex < numMinAgents:
                    v += probabilityOfEachAction * minValue(successorState, agentIndex + 1, depth)
                else:
                    v += probabilityOfEachAction * maxValue(successorState, depth + 1)
            return v

        # Constants
        MAX_AGENT_INDEX = 0
        FIRST_MIN_AGENT_INDEX = 1
        INITIAL_DEPTH = 1

        # The actual algorithm starts here
        actions = gameState.getLegalActions(MAX_AGENT_INDEX)
        bestValue = -1000000000
        bestAction = None
        dictActionValue = {}
        for action in actions:
            successor = gameState.generateSuccessor(MAX_AGENT_INDEX, action)
            successorMinValue = minValue(successor, FIRST_MIN_AGENT_INDEX, INITIAL_DEPTH)
            dictActionValue[action] = successorMinValue
            if successorMinValue > bestValue:
                bestValue = successorMinValue
                bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: This evaluation function -
      1) Rewards not dying (of course!) - this logic is captured by the game score itself
      2) Gives a high reward for eating up food pellets
      3) Gives a small reward for being closer to the food
    """
    "*** YOUR CODE HERE ***"
    # Imports
    from random import randint
    from util import manhattanDistance as md

    # Useful information extracted from GameState (pacman.py)
    pacmanPos = currentGameState.getPacmanPosition()
    foodMatrix = currentGameState.getFood()
    foodList = foodMatrix.asList()
    successorGameScore = currentGameState.getScore()

    # Actual calculations start here
    numberOfRemainingFood = len(foodList)

    distanceFromFoods = [md(pacmanPos, newFoodPos) for newFoodPos in foodList]
    distanceFromClosestFood = 0 if (len(distanceFromFoods) == 0) else min(distanceFromFoods)

    finalScore = successorGameScore - (50 * numberOfRemainingFood) - (5 * distanceFromClosestFood)  + randint(0,1)
    return finalScore

# Abbreviation
better = betterEvaluationFunction

class MCTSAgent(Agent):
    pass

    def registerInitialState(self, state):
        pass
        # print "state\n", state
        # print "type(state)\n", type(state)
        # print "state.__class__.__name__\n", state.__class__.__name__

    def getAction(self, state):
        # type: (GameState) -> str
        # return random.choice(state.getLegalActions())
        # if random.randint(0,10000) % 100 == 0:
        #     print 1, random.randint(0, 1000)
        fbgs = FeatureBasedGameState(state)
        # if random.randint(0,10000) % 100 == 0:
        #     print 2, random.randint(0, 1000)
        uctValues = self.getUCTValues(fbgs, commonModel)
        # if random.randint(0,10000) % 100 == 0:
        #     print 3, random.randint(0, 1000)
        # print "uctValues", uctValues
        actionToReturn = max(uctValues)[1]
        # print actionToReturn
        return actionToReturn

    def getUCTValues(self, fbgs, model):
        # type: (FeatureBasedGameState, Model) -> List[(float, str)]
        w = {}
        n = {}
        N = 0
        c = sqrt(2)
        legalActions = fbgs.rawGameState.getLegalActions()
        for action in legalActions:
            if (fbgs, action) not in model.data:
                n[action] = 0
                w[action] = 0
            else:
                n[action] = model.data[(fbgs, action)].nSimulations
                w[action] = model.data[(fbgs, action)].nWins
            N += n[action]
        uctValues = []
        for action in legalActions:
            uctValue = self.getUCTValue(w[action], n[action], N, c)
            uctValues.append((uctValue, action))
        return uctValues

    def getUCTValue(self, w, n, N, c):
        return w/(n+1.0) + c*sqrt(log(N+1.0)/(n+1.0))
