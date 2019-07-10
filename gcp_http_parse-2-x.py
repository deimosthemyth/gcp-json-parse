#!/usr/bin/python
#Script to help parse GCP HTTP JSON data into a readable format
#Written for Python 2 by deimosthemyth https://github.com/deimosthemyth
#Function to define user-supplied input (v2 expand to include what JSON vars they want to output vs static value)

import json
import base64
import time
from urllib import unquote
import csv

#Start efficiency timing
#start = time.time()

#Open output file for writing - MOVE THIS TO A GLOBAL FUNCTION
outCSV = open('json-clean.csv', 'w')
fieldnames = ['Timestamp', 'Source IP', 'Destination IP', 'Method','Full URL Path','Decoded Payload']
writer = csv.DictWriter(outCSV, fieldnames=fieldnames)
writer.writeheader()

def userInput():
    try:
        userFile = raw_input("Please input the path of the JSON file you want to parse: ")
        return userFile
    except IOError:
        print ("An error occured trying to import this file.  Please re-run the program with a valid filename and path.")

#Load JSON data - all lines
def jsLoad(userFile):
    try:
        jsonData = []
        #opens JSON file
        with open(userFile, 'r') as f:
        #iterates through the malformed JSON to create a list object
            for line in f:
                jsonData.append(json.loads(line))
                #iterate over the list and pass each object to jsParse for parsing/output
                for i in jsonData:
                    jsParse(i)
        return jsonData
    except IOError:
        print ('An error occured trying to read data from the file.')
    
#Function to parse the JSON into attributes
def jsParse(jsonData):

    #Grabs the payload from the request body   
    reqBody = jsonData['request']['body']

    #Removes the three trailing milliseconds, and converts to local timestamp
    epoch = str(jsonData['tcp']['connectionStartNs'])[0: 10]
    epoch = time.strftime("%a, %b %d %Y %H:%M:%S %Z", time.localtime(float(epoch)))
    
    #Print out values (static for now, change to requested in the future)
    timeStamp = epoch
    srcIP = jsonData['ip']['srcIp']
    dstIP = jsonData['ip']['dstIp']
    method = jsonData['request']['method']
    fullPath = jsonData['request']['url']['host'] + jsonData['request']['url']['path']
    #Would be good to add a check so see if it is base64 encoded 
    #Base64 decode of the body payload, and URL unencode as well
    decodedReqBody = unquote(base64.decodestring(reqBody))
 
    #Write current row to CSV
    writer.writerow({'Timestamp': timeStamp, 'Source IP': srcIP, 'Destination IP': dstIP, 'Method': method, 'Full URL Path': fullPath, 'Decoded Payload': decodedReqBody})


#Execute functions

#Get file
userFile = userInput()

#Get data
jsonData = jsLoad(userFile)

#Close file
outCSV.close()

#Time the function for efficiency
#end = time.time()
#print(end - start)