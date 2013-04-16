'''
Created on Apr 13, 2013

@author: agrammenos
'''
from util import SuperPriorityQueue


'''
    We use the AIMA-Python Code approach for our Search problem,
    that is create a General-Abstract class for the problems we
    want to solve and then derive from that one.
'''
class GeneralSearchProblem:
    """The abstract class for a formal problem.  You should subclass this and
    implement the method successor, and possibly __init__, goal_test, and
    path_cost. Then you will create instances of your subclass and solve them
    with the various search functions."""

    #def __init__(self, initial, goal):
    #    """The constructor specifies the initial state, and possibly a goal
    #    state, if there is a unique goal.  Your subclass's constructor can add
    #    other arguments."""
    #    self.initial = initial; self.goal = goal
        
    def successorBuilder(self, currentState):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        
    def getStartVertex(self):
        """
            This returns the start state of our graph
        """
    
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Implement this
        method if checking against a single self.goal is not enough."""
        #return state == self.goal
        
    def goalVertexTest(self):
        '''
            This is nice
        '''
    
    def GetPathCost(self, bucketOfActions):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        

    def setExpanded(self):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        
        
'''
    Search Algorithms General Functions
'''
        
'''
    This is the code for Uniform-Cost Search function.
    This was derived from Wikipedia code is in the
    corresponding article. Translation from pseudocode
    to Python was trivial
'''
        
def ucs(searchProblem, currentState = None):
    
    # Create our queue and set
    pq = SuperPriorityQueue()
    ucsSet = set()
    
    # now initialize our problem
    if(currentState == None):
        pq.put((searchProblem.getStartVertex(),[]), 0)
    else:
        pq.put((currentState,[]), 0)
        
    # Searching
    while (not pq.empty()):
        vertex = pq.get()
        
        # check the if we have reached our destination
        if(searchProblem.goal_test(vertex[0])):
            # return the destination vertex
            return vertex[1]
        
        # if not, search
        
        # first check if our vertex is in the set
        if(vertex[0] not in ucsSet):
            # if not add it
            ucsSet.add(vertex[0])
            # and run a for loop for each of the vertex successors
            # and calculate the costs
            for successorVertices in searchProblem.successorBuilder(vertex[0]):
                bucketOfActions = list(vertex[1])
                bucketOfActions.append(successorVertices[1])
                # actual cost calculation
                pr = searchProblem.GetPathCost(bucketOfActions)
                # put it back in the queue
                pq.put((successorVertices[0],bucketOfActions), pr)
            

'''
    This method is used due to a hint that the Professor gave us; 
    we use the UCS search as the heuristic function of our IDA*
'''
def ucsBasedIDAHeuristic(currentState, searchProblem = None):
    '''
        We take each 'snapshot' of IDA* and apply a new UCS
        on that 'snapshot' in order to get the heuristic costs
        
        This is quite slow as in each turn of the algorithm we
        have to apply both IDA* and UCS at the same time.
        
        It is also expected to give approximately the same results
        (since we are using UCS to grade our paths)
    '''
    
    
    # we search here using UCS
    bucketOfPosibleActions = ucs(searchProblem, currentState)
    
    # and here we return the path costs calculated using the
    # formula above
    return searchProblem.GetPathCost(bucketOfPosibleActions)

'''
    This is the wrapper of the IDA* algorithm that is used to call
    the actual recursion
    
    Code was derived from Wikipedia IDA* algorithm pseudocode, 
    translation to Python was trivial
    
    Heuristic function used is the UCS algorithm
'''

def idaStarCallback(searchProblem, hf=ucsBasedIDAHeuristic):
    
    # get our initial state
    snode = (searchProblem.getStartVertex(), [])
    # now pass it to our heuristic function to find the
    # cutoff point
    cutoff = hf(snode[0], searchProblem)
    
    # our starting vertex
    vertex = [None,]
    
    # run the loop
    while vertex[0] == None:
        # vertex, cost tuple return from idaStar
        (vertex, cost) = idaStar(searchProblem, snode, hf, cutoff)
        # update the cutoff point
        cutoff = cost
        
        # check if we reached the end
        if(searchProblem.goal_test(vertex[0])):
            # if so return the tuple of (vertex,cost)
            # that is returned by ida*
            return(vertex[1], cost)

'''
    This function returns the costs of the edges
'''
def pf(searchProblem, snode, hf):
    # the f = g + h
    g = searchProblem.GetPathCost(snode[1])
    h = hf(snode[0], searchProblem)
    # now return it
    return (g+h)

'''
    Actual idaStar function. Takes as parameters
    the required search problem, the starting vertex
    the heuristic function [which we defined above as
    the UCS] as well as the cutoff limit
'''
def idaStar(searchProblem, snode, hf, cutoff):
    
    # get the costs
    costs = pf(searchProblem, snode, hf)
    
    # check what we got
    
    # if our costs are greater than our cutoff value
    # just return
    if(costs > cutoff):
        return((None, snode[1]), costs)
    
    # now check if we are at a goal state
    if(searchProblem.goal_test(snode[0])):
        # return the node and the cost
        return(snode,costs)
    
    # if not, continue searching
    l = 1000000 # very large
    # now loop
    for successor in searchProblem.successorBuilder(snode[0]):
        # our bucket of actions
        bucket = list(snode[1])
        bucket.append(successor[1])
        
        # now pass it
        (sucNode, sucCost) = idaStar(searchProblem, (successor[0], bucket), hf, cutoff)
        # check if we are at the end
        if(searchProblem.goal_test(sucNode[0])):
            # if so return the required tuple
            return(sucNode, sucCost)
        # update the limit
        l = min(l, sucCost)
    
    # now return the tuple with the updated node and limit
    return((None, snode[1]), l)
        