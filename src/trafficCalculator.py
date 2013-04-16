'''
Created on Apr 13, 2013

@author: agrammenos
'''

import os
import time
import sys

from fileReader import fileReader
import searchProblem
from graphBuilder import graphBuilder

'''
    This is for samples only [generate the sample 
    graph names that was provided as a sample 
    database for our program]
'''
def datasetNameCreator():
    # create the files
    files = []
    # now append
    for i in range(6):
        files.append('dataset/sampleGraph'+str(i+1)+'.txt')
    
    # now return it
    return files

def processDay(data, day):
    
    print('\nStarting Processing Day: ' + str(day+1) + '\n')
    
    # problem builder
    sp = graphBuilder(data, day)
    
    str_ucs = '\nUCS Result for Day ' + str(day+1) + ': \n'
    str_ida = '\nIDA* Result for Day ' + str(day+1) + ': \n'
    
    # UCS Segment
    t0 = time.time()
    availActions = searchProblem.ucs(sp)
    t1 = time.time()
    ucstDiff = t1-t0
    actualCost = sp.GetPathCost(availActions, sflag = True)
    ucsCost = actualCost
    
    # day result
    ucsResult = (sp.visited, ucstDiff, sp.GetPathCost(availActions), actualCost, availActions)
    print('UCS Result: \n')
    print('\t' + str(ucsResult))
    str_ucs += ('\t' + str(ucsResult) + '\n')
    ucsPerf = (sp.visited, ucstDiff)
    # End of UCS Segment
    
    # IDA* Segment
    t0 = time.time()
    availActions, costEstimation = searchProblem.idaStarCallback(sp)
    t1 = time.time()
    idatDiff = t1-t0
    actualCost = sp.GetPathCost(availActions, sflag = True)
    idaCost = actualCost
    
    idaResult = (sp.visited, idatDiff, costEstimation, actualCost, availActions)
    print('\nIDA Result: \n')
    print('\t' + str(idaResult))
    str_ida += ('\t' + str(idaResult)+'\n')
    idaPerf = (sp.visited, idatDiff)
    # End of IDA* Segment
    
    print('\nDone for day: ' + str(day+1) + '\n\n')
    
    # return is for processing
    return (ucsCost, idaCost, str_ucs, str_ida, ucsPerf, idaPerf)


'''
    This function parses the files and generates the required
    results (provided the files exist and are valid)
'''
def processFiles(files, bench):
    
    # create the names
    if(bench is True):
        files = datasetNameCreator()
    
    # get count
    #percentage = len(files) * 80
    
    
    # construct the file reader
    r = fileReader()
    
    # this is for global average
    ucsSamples = []
    idaSamples = []
    
    #ucsPerfGlob = []
    #idaPerfGlob = []
    

    
    # now loop for each file
    for f in files:
        # reset costs for each run
        ucsCost = 0
        idaCost = 0
        
        # performance counts
        ucsPerfTime = 0
        ucsVisited = 0
        
        idaPerfTime = 0
        idaVisited = 0
        # reset the files
        str_ida = ''
        str_ucs = ''
        # read data
        fdat = r.readInputFile(f, 0)
        for i in range(DAYS_RANGE_MAX):
            # process each day and return
            (tucsCost, tidaCost, t1, t2, tp1, tp2) = processDay(fdat, i)
            # now add
            # average costs
            ucsCost += tucsCost
            idaCost += tidaCost
            # string data
            str_ucs += t1
            str_ida += t2
            
            # performance
            ucsPerfTime += tp1[1]
            idaPerfTime += tp2[1]
            
            ucsVisited += tp1[0]
            idaVisited += tp2[0]
        
        # when 80-day simulation finishes normalize
        ucsCost /= DAYS_RANGE_MAX
        idaCost /= DAYS_RANGE_MAX
        
        ucsPerfTime /= DAYS_RANGE_MAX
        idaPerfTime /= DAYS_RANGE_MAX
            
        ucsVisited /= DAYS_RANGE_MAX
        idaVisited /= DAYS_RANGE_MAX
        
        # file header
        str_fheader = 'Results for file: ' + str(f) + '\n' + '\nAverage Results for this file: \n' + '\tUCS: ' + str(ucsCost) + '\n\tIDA*: ' + str(idaCost) + '\n'
        
        str_fheader += '\n\nAverage Performance for this file:\n\t UCS:\n\t\tVisited Nodes (Avg): ' + str(ucsVisited)
        str_fheader += '\n\t\tExecution Time (Avg): ' + str(ucsPerfTime) + '\n\n' 
        
        str_fheader += '\n\nAverage Performance for this file:\n\t IDA*:\n\t\tVisited Nodes (Avg): ' + str(idaVisited)
        str_fheader += '\n\t\tExecution Time (Avg): ' + str(idaPerfTime) + '\n\n' 
        
        
        str_filename = str(f).replace('dataset/', '') + '.result'
        
        # write it to the corresponding file
        writeOutput(str_ucs, str_ida, str_fheader, str_filename)
        
        
        # now add it
        ucsSamples.append(ucsCost)
        idaSamples.append(idaCost)
    
    # when all 6 files finish print Average Costs
    print('Average UCS cost for all data sets (in an 80-day simulation period): ')
    print('\n\t' + str(ucsSamples))

    print('Average IDA* cost for all data sets (in an 80-day simulation period): ')
    print('\n\t' + str(idaSamples))
    
    # output it to a file
    global_str_header = 'Accumulated Results for all Parsed files:\n\n'
    global_str_header += 'Average UCS cost for all data sets (in an 80-day simulation period): \n'
    global_str_header += '\n\t' + str(ucsSamples) + '\n'
    global_str_header += '\nAverage IDA* cost for all data sets (in an 80-day simulation period): \n'
    global_str_header += '\n\t' + str(idaSamples)
    global_str_filename = 'global_results.txt'
    
    writeOutput('', '', global_str_header, global_str_filename)

def writeOutput(ucsStr, idaStr, header, filename):
    
    # ensure we have created the output directory
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
        
    # now open it
    with open(OUTPUT_PATH + filename, 'w') as f:
        # write in the following order
        #
        #    1) file header
        #    2) UCS results
        #    3) IDA results
        f.write(header)
        f.write(ucsStr)
        f.write(idaStr)
        
        # close file
        f.close()
        
        
        

'''
    Progress bar
'''
def update_progress(amtDone):
    #print(amtDone)
    #sys.stdout.write('\r[{0}] {1}%'.format('#'*(progress/10), progress))
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
    sys.stdout.flush()

'''
    Our main function
'''

def main(bench, files):

    # by definition
    global DAYS_RANGE_MAX
    global OUTPUT_PATH
    
    DAYS_RANGE_MAX = 80
    OUTPUT_PATH = 'output/'

    '''
        Check our input and decide what to do
    '''

    # check if we have to benchmark our software
    if(bench is True):
        print('Benchmarking program with provided dataset from "dataset/" folder')
        processFiles(0, bench)
    # parse input and process it 
    else:
        print('Parsing provided files')
        processFiles(files, 0)


if __name__ == '__main__':
    
    
    '''
        Library used for easy command line parsing
    '''
    import argparse
    
    '''
        Command line arguments Parser
    '''
    parser = argparse.ArgumentParser(description='Search for the best possible route between roads based on their traffic level')
    group = parser.add_mutually_exclusive_group()

    '''
        Add mutually exclusive options
    '''
    
    group.add_argument('-b','--bench', action='store_true', help='benchmark the software using the provided data-set which is located in the "dataset" folder')
    group.add_argument('-f', '--files', nargs='*', help='provide your own files for analysis (separate each one with commas) [ a.txt, b.txt ... ]')
    
    '''
        Update the parser
    '''
    
    args = parser.parse_args()


    '''
        Ensure we have the correct input combination
    '''

    if(args.bench):
        print('Got bench')
        main(args.bench, 0)
    elif(args.files):
        print('Got files')
        main(0, args.files)
    else:
        print("Wrong input arguments... please use --help argument")

    
    pass