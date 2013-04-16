'''
Created on Apr 13, 2013

@author: agrammenos
'''

import os

class fileReader(object):
    '''
    classdocs
    '''
    global RANGE_DEPTH

    def __init__(self):
        '''
        Constructor
        '''
        self.RANGE_DEPTH = 80
    
    '''
        This is done due to the fact that the input
        files were created using Windows... and I 
        develop in a posix-compliant OS. This trick
        is used to parse the files correctly no matter
        the OS we are in.
    '''
    def getLineDelimiterBasedOnOS(self):
        if(os.name == 'nt'):
            return '\n'
        else:
            return '\r\n'
        
    '''
        This function filters the input of the file
        we just read
    '''
    def filterInput(self, filedata):

        # initialize the delimiters
        delim = self.getLineDelimiterBasedOnOS()        
        sdelim = '; '


        # parse Source & Destination Vertex

        # Filtering of the Source & Destination (extract it from the two first lines)
        destNode = filedata[1].replace('<Destination>','').replace('</Destination>'+delim,'')
        srcNode = filedata[0].replace('<Source>', '').replace('</Source>'+delim, '')
        
        #print(srcNode)
        #print(destNode)

        # initialize our graph
        providedRoads = {}
        providedCosts = {}
        
        # parse costs & road connections
        
        # use this trick to start from line 3 and onwards
        for l in filedata[3:]:
            # check if we reached the end
            if(l == '</Roads>'+delim):
                break;
            # if not parse
            
            # split the lines using the delimiter '; '
            t = l.split(sdelim)
            #print(t)
            # get the arithmetic value
            t[3] = int(t[3])
            
            # check if it's in our map and if it's
            # not add it
            if(t[1] not in providedRoads.keys()):
                providedRoads[t[1]]= []
            if(t[2] not in providedRoads.keys()):
                providedRoads[t[2]] = []
        
            # add it to the map that road 0 is linked with
            # the other two
            providedRoads[t[1]].append((t[0], t[2]))
            providedRoads[t[2]].append((t[0], t[1]))
            
            # update the cost for the road
            providedCosts[t[0]]=t[3]
        
        # prediction day line number, 6 is padding for non
        # actual information lines
        predline = len(providedCosts) + 6
        
        # parse predictions
        
        dayPredictions = []
        
        for j in range(self.RANGE_DEPTH):
            dayPredictions.append({})
            
            # necessary padding to start from the correct position
            for l in filedata[predline+j*(len(providedCosts)+2):]:
                # check if we reached the end
                if(l == '</Day>'+delim):
                    break
                # split the same way as above
                t = l.split(sdelim)
                # strip the newlines
                t[1] = t[1].strip(delim)
                
                # now check the traffic density and based on
                # the given values give the necessary values
                if(t[1] == 'heavy'):
                    # if the traffic is heavy it's 25 % more
                    # expensive so... it's 1.25
                    c_cost = 1.25
                elif(t[1] == 'low'):
                    # if the traffic is low it's 10 % less
                    # expensive than normal so... it's 0.9
                    c_cost = 0.9
                else:
                    # else we have a normal traffic and a
                    # normal cost
                    c_cost = 1.0
                # update the day predictions
                dayPredictions[j][t[0]] = c_cost
        
        
        # parse actual day measurements
                
        # in the same manner as above calculate the padding
        actualDayline = predline + 2 + 80*(len(providedCosts)+2)
        
        actualDayMeasurements = []
        
        # this is given from definition (the 80)
        for j in range(self.RANGE_DEPTH):
            actualDayMeasurements.append({})
            # necessary padding to start form the correct position
            for l in filedata[actualDayline+j*(len(providedCosts)+2):]:
                # check if we end
                if(l == '</Day>'+delim):
                    break;
                
                # if not, parse
                
                # same segment as above...
                
                # split using the correct delimiter
                t = l.split(sdelim)
                # strip newlines
                t[1] = t[1].strip(delim)
                
                # now check the traffic density and based on
                # the given values give the necessary values
                if(t[1] == 'heavy'):
                    # if the traffic is heavy it's 25 % more
                    # expensive so... it's 1.25
                    c_cost = 1.25
                elif(t[1] == 'low'):
                    # if the traffic is low it's 10 % less
                    # expensive than normal so... it's 0.9
                    c_cost = 0.9
                else:
                    # else we have a normal traffic and a
                    # normal cost
                    c_cost = 1.0
                    
                # update the costs
                actualDayMeasurements[j][t[0]] = c_cost
                
        #print(providedRoads)    
            
        # finally return
        return (destNode, srcNode, providedRoads, providedCosts, dayPredictions, actualDayMeasurements)
                    
                
        
    '''
        This function reads a file we have as an input
    '''
    def readInputFile(self, filename, verbose):
        
        #print('Reading Input files')
        
        # this is the files tuple, check it's size
        if filename == []:
            return 
        
        # try to open it
        print(filename)
        with open(filename, 'r') as fstream:
            # and... read it.
            filedata = fstream.readlines()
            
        # close stream, since we are done    
        fstream.closed
        # return this in the main program
        return self.filterInput(filedata)
        
        #print(filedata)
            
            