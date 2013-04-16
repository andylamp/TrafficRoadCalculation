'''
Created on Apr 13, 2013

@author: agrammenos
'''

from Queue import PriorityQueue

'''
    This is a simple priority Queue that extends the functionality
    of the existing priority Queue that's built in Python already.
    The functionality to be added is to put and remove tuples of the
    form (item, priority) which is not available. 
'''

class SuperPriorityQueue(PriorityQueue):
    
    '''
        Constructor, it creates a Priority Queue object and 
        increases the counter
    '''
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    '''
        Put in the Queue
    '''
    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    '''
        Get it out of the Queue
    '''
    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item
    
    '''
        To check if our queue is empty
    '''
    def empty(self):
        return PriorityQueue.empty(self)