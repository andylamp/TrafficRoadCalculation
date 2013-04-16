'''
Created on Apr 14, 2013

@author: agrammenos
'''

import searchProblem
import random

class graphBuilder(searchProblem.GeneralSearchProblem):
    '''
    classdocs
    '''


    def __init__(self, searchData, day):
        '''
        
            Constructor
            
                initialize the class using the data
                
                We initialize the nodes of our graph based on
                our data as well as store the start/target 
                vertices
                 
        '''
        
        # if we visited a node
        self.visited = 0
        
        '''
            Based on our file reads
        '''
        self.startVertex = searchData[0]
        self.goalVertex = searchData[1]
        self.inputRoads = searchData[2]
        self.inputRoadCost = searchData[3]
        self.inputEstimationCosts = searchData[4]
        self.inputActualCosts = searchData[5]
        
        # days passed
        self.day = day
        
        # prob
        self.defProb = 0.6
        
    '''
        Function that returns the Start Vertex
    '''
    def getStartVertex(self):
        return(self.startVertex)
    '''
        Function that returns True if we have 
        reached our goal
    '''
    def goal_test(self, currentState):
        return(currentState == self.goalVertex)
     
    '''
        Function that returns the Goal Vertex
    '''
    def goalVertexTest(self):
        return(self.goalVertex)
    
    '''
        Function that builds up our successors based
        on a given state
    '''    
    def successorBuilder(self, currentState):
        
        c = self.inputEstimationCosts[self.day]
        successors = []
        
        for sucAction, sucState in self.inputRoads[currentState]:
            cost = self.inputRoadCost[sucAction]*c[sucAction]
            successors.append((sucState, sucAction, cost))
            
        # set expanded flag
        self.setExpanded()
        
        return successors
        
        
    '''
        This sets the provided node expanded status to 1
    '''
    def setExpanded(self):
        self.visited += 1
        
    '''
        Calculates the cost of edges in our graph
    '''
    def GetPathCost(self, actions, sflag = False):
        
        c = []
        cost = 0
        
        # no actions to make, return a very large value
        if(actions == None):
            return 1000000

        # loop through available actions in our bucket
        for action in actions:
            
            # calculation of actual costs
            if(sflag is True):
                c = self.inputActualCosts[self.day]
                cost += self.inputRoadCost[action]*c[action]
            # calculation of probabilistic costs
            else:
                c = self.inputEstimationCosts[self.day]
                
                c_weight = self.distributeCoef(c[action], self.defProb)
                cost += self.inputRoadCost[action]*c_weight

        # finally return
        return cost
        
    '''
        This distributes the probabilities and creates the necessary
        weights in our graph
    '''
    def distributeCoef(self, coef, probability):
        
        # generate a random number [0, 1]
        prob = random.random()
        
        
        # high traffic prob
        if(coef == 1.25):
            p1 = 1
            p2 = 1.25
        # normal traffic
        elif(coef == 1):
            p1 = 0.9
            p2 = 1.25
        # low traffic
        else:
            p1 = 1
            p2 = 1.25
            
        # this is to decide the actual traffic probs
        if(prob > (1+probability)/2):
            return p2
        else:
            return p1
            
            