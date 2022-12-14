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

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        foodList = []
        ghostList = []
        newFoods = []

        for food in currentGameState.getFood().asList():
            foodList.append(manhattanDistance(food, currentGameState.getPacmanPosition()))
        nearestFood = min(foodList)

        for state in newGhostStates:
            ghostList.append(manhattanDistance(state.getPosition(), newPos))
        minGhost = min(ghostList)

        for food in newFood.asList():
            newFoods.append(manhattanDistance(food, newPos))
        if (not newFoods):
            newNearestFood = 0
        else:
            newNearestFood = min(newFoods)

        if action == Directions.STOP or minGhost <= 1: return 0
        if action == currentGameState.getPacmanState().getDirection(): return 2
        if nearestFood - newNearestFood > 0: return 4
        if successorGameState.getScore() - currentGameState.getScore() > 0: return 8
        return 1

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minValue(state, i, depth):
            successors = []
            actions = state.getLegalActions(i)
            if not actions: return self.evaluationFunction(state)

            if i == state.getNumAgents() - 1:
                for action in actions:
                    successors.append(maxValue(state.generateSuccessor(i, action), depth))
                return min(successors)
            else:
                for action in actions:
                    successors.append(minValue(state.generateSuccessor(i, action), i+1, depth))
                return min(successors)

        def maxValue(state, depth):
            successors = []
            actions = state.getLegalActions(0)
            if depth == self.depth or not actions:
                return self.evaluationFunction(state)
            for action in actions:
                successors.append(minValue(state.generateSuccessor(0, action), 1, depth + 1))
            return max(successors)

        return max(gameState.getLegalActions(0), key=lambda action: minValue(gameState.generateSuccessor(0, action), 1, 1))

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maximum(gameState,depth,alpha, beta):
            currDepth = depth + 1
            if currDepth==self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            maxvalue = -999999
            actions = gameState.getLegalActions(0)
            newAlpha = alpha
            for action in actions:
                successor= gameState.generateSuccessor(0,action)
                maxvalue = max(maxvalue,minimum(successor,currDepth,1,newAlpha,beta))
                if maxvalue > beta:
                    return maxvalue
                newAlpha = max(newAlpha, maxvalue)
            return maxvalue
        
        def minimum(gameState,depth,i,alpha,beta):
            minFound = 999999
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            newBeta = beta
            actions = gameState.getLegalActions(i)
            for action in actions:
                successor = gameState.generateSuccessor(i,action)
                if i == (gameState.getNumAgents()-1):
                    minFound = min(minFound, maximum(successor,depth,alpha,newBeta))
                    if minFound < alpha: return minFound
                    newBeta = min(minFound, newBeta)
                else:
                    minFound = min(minFound,minimum(successor,depth,i+1,alpha,newBeta))
                    if minFound < alpha: return minFound
                    newBeta = min(minFound, newBeta)
            return minFound

        beta = 999999
        alpha = -999999
        score = -999999
        actions = gameState.getLegalActions(0)
        finalAction = ''
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            newScore = minimum(nextState, 0, 1, alpha, beta)
            if newScore > score:
                score = newScore
                finalAction = action
            if newScore > beta:
                return finalAction
            alpha = max(newScore, alpha)
        return finalAction

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
        def expect(state, i, depth):
            sum = 0
            actions = state.getLegalActions(i)
            if not actions: return self.evaluationFunction(state)

            for action in actions:
                newState = state.generateSuccessor(i, action)
                if i == state.getNumAgents() - 1:
                    sum += maximum(newState, depth) * (1.0 / len(actions))
                else:
                    sum += expect(newState, i + 1, depth) * (1.0 / len(actions))
            return sum

        def maximum(state, depth):
            successors = []
            actions = state.getLegalActions(0)
            if depth == self.depth or not actions:
                return self.evaluationFunction(state)

            for action in actions:
                successors.append(expect(state.generateSuccessor(0, action), 1, depth + 1))
            return max(successors)

        return max(gameState.getLegalActions(), key=lambda action: expect(gameState.generateSuccessor(0, action), 1, 1))

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodList = newFood.asList()
    score = 0
    dists = [0]
    ghosts = []
    ghostsDist = [0]
    
    for ghost in newGhostStates:
        ghosts.append(ghost.getPosition())
    for ghost in ghosts:
        ghostsDist.append(manhattanDistance(newPos,ghost))
    for food in foodList:
        dists.append(manhattanDistance(newPos, food))

    score += len(newFood.asList(False)) + currentGameState.getScore()
    if sum(dists) > 0: score += 1.0 / sum(dists)

    if sum(newScaredTimes) > 0:    
        score += sum(newScaredTimes) + (-sum(ghostsDist)) + (-len(currentGameState.getCapsules()))
    else:
        score += sum(ghostsDist) + len(currentGameState.getCapsules())
    return score

# Abbreviation
better = betterEvaluationFunction
