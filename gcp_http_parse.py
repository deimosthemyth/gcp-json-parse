#!/usr/bin/python
#Script to help parse GCP HTTP JSON data into a readable format
#Written by deimosthemyth https://github.com/deimosthemyth


import json
import base64
import time
from urllib import unquote
import csv

#Function to define user-supplied input (v2 expand to include what JSON vars they want to output vs static value)
def userInput():
    try:
        userFile = raw_input("Please input the path of the JSON file you want to parse: ")
        return userFile
    except IOError:
        print ("An error occured trying to import this file.  Please re-run the program with a valid filename and path.")

#Load JSON data (one line currently)
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
                    j = i
                    jsParse(i,j)
        return jsonData
    except IOError:
        print ('An error occured trying to read data from the file.')
    
#Function to parse the JSON into attributes
def jsParse(jsonData,j):
    print j
    #Grabs the payload from the request body
    reqBody = jsonData['request']['body']

    #Removes the three trailing milliseconds, and converts to local timestamp
    epoch = str(jsonData['tcp']['connectionStartNs'])[0: 10]
    epoch = time.strftime("%a, %b %d %Y %H:%M:%S %Z", time.localtime(float(epoch)))
    
    #NEED BASE64 CHECK HERE, LEN = 64 DOESN'T WORK
    #Base64 decode of the body payload, and URL unencode as well
    decodedReqBody = unquote(base64.decodestring(reqBody))
    
    #Print out values (static for now, change to requested in the future)
    timeStamp = epoch
    srcIP = jsonData['ip']['srcIp']
    dstIP = jsonData['ip']['dstIp']
    method = jsonData['request']['method']
    fullPath = jsonData['request']['url']['host'] + jsonData['request']['url']['path']
    decPayload = decodedReqBody
    #writer.writerow({'Timestamp': timeStamp, 'Source IP': srcIP, 'Destination IP': dstIP, 'Method': method, 'Full URL Path': fullPath, 'Decoded Payload': decPayload})
       
#output to CSV
#with open('converted_csv_output.csv', mode='w') as csv_file:
#    fieldnames = ['Timestamp', 'Source IP', 'Destination IP', 'Method','Full URL Path','Decoded Payload']            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#    writer.writeheader()

#Execute functions
userFile = userInput()
jsonData = jsLoad(userFile)
