'''
Created on Sep 26, 2015

@author: bgage
'''
import os
import json
class JsonUtil(object):
    def __init__(self, inputFile='' , logger = None):
        self._inputFile = inputFile
        self.logger = logger
        
    def retrieveElementFromJsonConfig(self , elementName):
        parameter = ''
        json_data = self.retrieveJsonObjectFromJsonConfig()
        if json_data is not None:
            parameter = json_data[elementName]
        return parameter

    def retrieveJsonObjectFromJsonConfig(self):
        jsonObject = None
        try:
            if self._inputFile is not None and self._inputFile != '':
                absoluteFilePath = os.path.abspath(self._inputFile)
                if os.path.isfile(absoluteFilePath):
                    with open(absoluteFilePath , 'r') as jsonFile:
                        jsonObject = json.load(jsonFile)
        except Exception , error:
            self.logger.error("Error occurred - {0}".format(str(error)))
        return jsonObject
    
    def retrieveJsonObjectFromJsonConfigPath(self , inputFilePath=''):
        jsonObject = None
        try:
            if inputFilePath is not None and inputFilePath != '':
                absoluteFilePath = os.path.abspath(inputFilePath)
                if os.path.isfile(absoluteFilePath):
                    with open(absoluteFilePath , 'r') as jsonFile:
                        jsonObject = json.load(jsonFile)
        except Exception , error:
            self.logger.error("Error occurred - {0}".format(str(error)))
        return jsonObject