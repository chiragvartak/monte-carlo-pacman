# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import utilp1

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        utilp1.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        utilp1.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        utilp1.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        utilp1.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from collections import namedtuple
    SearchNode = namedtuple("SearchNode", "state actions")
    SearchNode.__eq__ = lambda x, y: x.state == y.state  # Though unnecessary, I have defined it for completeness

    # As a search node needs to store not just the state but also the path required to get to that state, it will be
    # be stored as a part of the search: (state, [actions])
    frontier = utilp1.Stack()  # Contains the *search nodes* to be tested for goal and expanded
    explored = set()  # Contains the explored *states*

    startNode = SearchNode(state=problem.getStartState(), actions=[])
    frontier.push(startNode)
    while True:
        if frontier.isEmpty(): return None
        currentNode = frontier.pop()
        if problem.isGoalState(currentNode.state): return currentNode.actions
        explored.add(currentNode.state)
        for childState,action,_ in problem.getSuccessors(currentNode.state):
            if childState not in explored:
                frontier.push(SearchNode(state=childState, actions=currentNode.actions+[action]))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from collections import namedtuple
    SearchNode = namedtuple("SearchNode", "state actions")
    SearchNode.__eq__ = lambda x, y: x.state == y.state  # Defined for completeness even though unnecessary

    # As a search node needs to store not just the state but also the path required to get to that state, it will be
    # be stored as a part of the search: (state, [actions])
    frontier = utilp1.Queue()  # Contains the *search nodes* to be tested for goal and expanded
    frontierStates = set()  # This is my own optimization for checking if a state exists in the frontier
    explored = set()  # Contains the explored *states*

    startNode = SearchNode(state=problem.getStartState(), actions=[])
    if problem.isGoalState(startNode.state): return startNode.actions
    frontier.push(startNode)
    frontierStates.add(startNode.state)
    while True:
        if frontier.isEmpty(): return None
        currentNode = frontier.pop()
        frontierStates.remove(currentNode.state)
        if problem.isGoalState(currentNode.state): return currentNode.actions
        explored.add(currentNode.state)
        for childState, action, _ in problem.getSuccessors(currentNode.state):
            if childState not in explored and childState not in frontierStates:
                frontier.push(SearchNode(state=childState, actions=currentNode.actions + [action]))
                frontierStates.add(childState)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from collections import namedtuple
    SearchNode = namedtuple("SearchNode", "state actions")
    SearchNode.__eq__ = lambda x, y: x.state == y.state

    # As a search node needs to store not just the state but also the path required to get to that state, it will be
    # be stored as a part of the search: (state, [actions])
    frontier = utilp1.PriorityQueue()  # Contains the *search nodes* to be tested for goal and expanded
    frontierStates = {}  # This is my own optimization for checking if a state exists in the frontier,
                         # and storing its path cost
    explored = set()  # Contains the explored *states*

    startNode = SearchNode(state=problem.getStartState(), actions=[])
    frontier.push(startNode, problem.getCostOfActions(startNode.actions))
    frontierStates[startNode.state] = problem.getCostOfActions(startNode.actions)
    while True:
        if frontier.isEmpty(): return None
        currentNode = frontier.pop()
        currentNodePathCost = frontierStates[currentNode.state]
        del frontierStates[currentNode.state]
        if problem.isGoalState(currentNode.state): return currentNode.actions
        explored.add(currentNode.state)
        for childState,action,stepCost in problem.getSuccessors(currentNode.state):
            childStateActions = currentNode.actions + [action]
            childStateCost = currentNodePathCost + stepCost
            if childState not in explored and childState not in frontierStates:
                frontier.push(SearchNode(state=childState, actions=childStateActions), childStateCost)
                frontierStates[childState] = childStateCost
            elif childState in frontierStates and frontierStates[childState] > childStateCost:
                frontier.update(SearchNode(state=childState, actions=childStateActions), childStateCost)
                frontierStates[childState] = childStateCost

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from collections import namedtuple
    SearchNode = namedtuple("SearchNode", "state actions")
    SearchNode.__eq__ = lambda x, y: x.state == y.state

    # As a search node needs to store not just the state but also the path required to get to that state, it will be
    # be stored as a part of the search: (state, [actions])
    frontier = utilp1.PriorityQueue()  # Contains the *search nodes* to be tested for goal and expanded
    frontierStates = {}  # This is my own optimization for checking if a state exists in the frontier,
                         # and storing its path and estimated cost as a tuple - so it has a twofold purpose.
                         # state: (pathCost, estimatedCost)
    explored = set()  # Contains the explored *states*

    startNode = SearchNode(state=problem.getStartState(), actions=[])
    startNodePathCost = problem.getCostOfActions(startNode.actions)
    startNodeEstimatedCost = startNodePathCost + heuristic(startNode.state, problem)
    frontier.push(startNode, startNodeEstimatedCost)
    frontierStates[startNode.state] = (startNodePathCost, startNodeEstimatedCost)
    while True:
        if frontier.isEmpty(): return None
        currentNode = frontier.pop()
        currentNodePathCost, currentNodeEstimatedCost = frontierStates[currentNode.state]  # Warning is a PyCharm bug
        del frontierStates[currentNode.state]
        if problem.isGoalState(currentNode.state): return currentNode.actions
        explored.add(currentNode.state)
        for childState,action,stepCost in problem.getSuccessors(currentNode.state):
            childStateActions = currentNode.actions + [action]
            childStatePathCost = currentNodePathCost + stepCost
            childStateEstimatedCost = childStatePathCost + heuristic(childState, problem)
            if childState not in explored and childState not in frontierStates:
                frontier.push(SearchNode(state=childState, actions=childStateActions), childStateEstimatedCost)
                frontierStates[childState] = (childStatePathCost, childStateEstimatedCost)
            elif childState in frontierStates and frontierStates[childState][1] > childStateEstimatedCost:
                frontier.update(SearchNode(state=childState, actions=childStateActions), childStateEstimatedCost)
                frontierStates[childState] = (childStatePathCost, childStateEstimatedCost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

###############################################
### Answers to questions inside the project ###
###############################################
#
# Question 1
# Q:
# Is the exploration order what you would have expected? Does Pacman
# actually go to all the explored squares on his way to the goal?
# A:
# Yes, the exploration order is as I expected.
# No, the Pacman does not go to all explored squares - all explored
# squares (states) need not be a part of the solution.
#
# Q:
# Is this the least cost solution? If not, think about what
# depth-first search is doing wrong.
# A:
# No.
# DFS simply returns the solution it encounters first; it does not
# return the least cost solution.
#
###############################################
#
# Question 2
# Q:
# Does BFS find a least cost solution?
# A:
# Yes.
# When all the step costs are equal (which they are here), BFS
# returns the solution of the lowest cost.
#
###############################################
#
# Question 4
# Q:
# What happens on openMaze for the various search strategies?
# A:
# DFS does not return the lowest cost solution.
# BFS, UCS and A* search all return the lowest cost solution.
# The number of nodes expanded by BFS and UCS are the same.
# The number of nodes expanded in decreasing order are:
# DFS > BFS=UCS > A*
#
################################################
#
# Question 8
# Q: Try to come up with a small example where repeatedly going to the closest dot does not
# result in finding the shortest path for eating all the dots.
# A:
# %%%%%%%%
# %      %
# %...P .%
# %.%%%% %
# %.%    %
# %.% %%%%
# %.%    %
# %%%%%%%%
# ^ In the above layout, as the ClosestDotSearchAgent is greedy, it finds the suboptimal
# path of cost 16, while the AStarFoodSearchAgent finds the optimal path of cost 11.
# (You can test this - save the above layout in a file "nonOptimalClosestDotSearch.lay",
# and run the following commands:
# $ python pacman.py -l nonOptimalClosestDotSearch -p AStarFoodSearchAgent
# and
# $ python pacman.py -l nonOptimalClosestDotSearch -p ClosestDotSearchAgent
# You will see the results.)
#
################################################