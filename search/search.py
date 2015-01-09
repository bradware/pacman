# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import pacman

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


class Node:
    state = None
    parent = None
    direction = None
    pathcost = 0

    def __init__(self, newstate, newparent, newdirection, newpathcost):
        self.state = newstate
        self.parent = newparent
        self.direction = newdirection
        self.pathcost = newpathcost

    def __eq__(self,otherNode):
        if isinstance(otherNode, Node):
            if(self.state == otherNode.state):
                return True
            return False

        else:
            if self.state == otherNode[2].state:
                return True
            
            return False


    def totalPathCost(self):
        totalcost = 0
        temp = self
        while temp.parent != None:
            totalcost += temp.pathcost
            temp = temp.parent
        return totalcost


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #node store state and as well as parents & child node references, fringe store nodes
    #node data structure to wrap action list and state
    #once goal state is found, make a node out of it
    #then iterate back up tree of family of nodes that led to that one, then make the action list by
    #either iterating back down or finding a clever way of doing it
    from game import Directions
    initstate = problem.getStartState()
    actionlist = []
    if problem.isGoalState(initstate):
        return actionlist
    stack = util.Stack()	#this could be called the open list
    visitedset = set([]) #holds a bunch of states that have been explored could be called closed list
    startnode = Node(initstate, None, None, 0)
    stack.push(startnode)
    while not stack.isEmpty():
        tempnode = stack.pop()
        visitedset.add(tempnode.state)  #made the visited set hold state's instead of nodes
        if problem.isGoalState(tempnode.state):
            return getTotalActions(tempnode)
        successorlist = problem.getSuccessors(tempnode.state)
        for state,dir,cost in successorlist:
            newnode = Node(state, tempnode, dir, cost)
            if newnode.state not in visitedset: ###and newnode not in stack.list: ##ASK ABOUT THIS
                stack.push(newnode)

    return actionlist


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    initstate = problem.getStartState()
    actionlist = []
    if problem.isGoalState(initstate):
        return actionlist
    queue = util.Queue()           #holds all of the nodes used
    visitedset = set([])           #holds a bunch of states that have been explored
    startnode = Node(initstate, None, None, 0)
    queue.push(startnode)
    while not queue.isEmpty():
        tempnode = queue.pop()
        visitedset.add(tempnode.state)  #made the visited set hold state's instead of nodes
        if problem.isGoalState(tempnode.state):
            return getTotalActions(tempnode)
        successorlist = problem.getSuccessors(tempnode.state)
        for state,dir,cost in successorlist:
            newnode = Node(state, tempnode, dir, cost)
            if newnode.state not in visitedset and newnode not in queue.list: ##ASK ABOUT THIS
                queue.push(newnode)

    return actionlist



def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    initstate = problem.getStartState()
    actionlist = []
    if problem.isGoalState(initstate):
        return actionlist
    pqueue = util.PriorityQueue()        #holds all of the nodes used
    visitedset = set([])           #holds a bunch of states that have been explored
    startnode = Node(initstate, None, None, 0)
    pqueue.push(startnode, startnode.pathcost)
    while not pqueue.isEmpty():
        tempnode = pqueue.pop()
        visitedset.add(tempnode.state)  #made the visited set hold state's instead of nodes
        if problem.isGoalState(tempnode.state):
            return getTotalActions(tempnode)
        successorlist = problem.getSuccessors(tempnode.state)
        for state,dir,cost in successorlist:
            newnode = Node(state, tempnode, dir, cost + tempnode.pathcost)  #this puts cost as total cost from start state
            if newnode.state not in visitedset:
                if newnode not in pqueue.heap:
                    pqueue.push(newnode, newnode.pathcost)
                else:
                    for node in pqueue.heap:
                        if newnode == node[2] and newnode.pathcost < node[2].pathcost: ###May need to compare states here instead of nodes
                            index = pqueue.heap.index(node)
                            del pqueue.heap[index]
                            pqueue.push(newnode, newnode.pathcost)

    return actionlist


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    initstate = problem.getStartState()
    actionlist = []
    if problem.isGoalState(initstate):
        return actionlist
    pqueue = util.PriorityQueue()        #holds all of the nodes used
    visitedset = set([])           #holds a bunch of states that have been explored
    startnode = Node(initstate, None, None, 0)
    pqueue.push(startnode, startnode.pathcost)
    while not pqueue.isEmpty():
        tempnode = pqueue.pop()
        visitedset.add(tempnode.state)  #made the visited set hold state's instead of nodes
        if problem.isGoalState(tempnode.state):
            return getTotalActions(tempnode)
        successorlist = problem.getSuccessors(tempnode.state)
        for state,dir,cost in successorlist:
            newnode = Node(state, tempnode, dir, cost + tempnode.pathcost)  #this puts cost as total cost from start state
            if newnode.state not in visitedset:
                if newnode not in pqueue.heap:
                    pqueue.push(newnode, newnode.pathcost + heuristic(newnode.state, problem))
                else:
                    for node in pqueue.heap:
                        if newnode == node[2] and newnode.pathcost < node[2].pathcost: ###May need to compare states here instead of nodes
                            index = pqueue.heap.index(node)
                            del pqueue.heap[index]
                            pqueue.push(newnode, newnode.pathcost + heuristic(newnode.state, problem))

    return actionlist


def getTotalActions(node):
    actionlist = []
    while(node.parent != None):
        actionlist.append(node.direction)
        node = node.parent
    actionlist.reverse()
    return actionlist


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
