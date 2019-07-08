#!/usr/bin/python
#Script to help parse GCP HTTP JSON data into a readable format
#Written by deimosthemyth https://github.com/deimosthemyth


import json
import base64
import time
from urllib import unquote
#import pprint

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
        with open(userFile, 'r') as f:
            jsonData = json.load(f)
    #pprint(jsonData) - need to import the file module too
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
    
    #NEED BASE64 CHECK HERE, LEN = 64 DOESN'T WORK
    #Base64 decode of the body payload, and URL unencode as well
    decodedReqBody = unquote(base64.decodestring(reqBody))
    
    #Print out values (static for now, change to requested in the future)
    print "\nTimestamp: " + epoch + "\n"
    print "Source IP: " + jsonData['ip']['srcIp'] + "\n"
    print "Destination IP: " + jsonData['ip']['dstIp'] + "\n"
    print "Method: " + jsonData['request']['method'] + "\n"
    print "Full URL Path - Host: " + jsonData['request']['url']['host'] + "  Path: " + jsonData['request']['url']['path'] + "\n"
    print "Decoded Payload: " + decodedReqBody + "\n"
       
       
#Execute functions
userFile = userInput()
jsonData = jsLoad(userFile)
jsParse(jsonData)