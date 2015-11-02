#!/usr/bin/env python
from model.valueobject import VoModel
from parser.config import ConfigJsonParser
from parser.constant import JsonConstants

class ValueObjectJsonParser:
    
    def __init__(self , configFileObj = None , logger=None):
        self.__configFileObj = configFileObj
        self.__logger = logger
    
    def listOfValueObjects(self):
        voList = []
        try:
            if self.__configFileObj is not None:
                for voObj in self.__configFileObj.valueObjects():
                        vomodel = VoModel()
                        vomodel.modelName = voObj['name']
                        vomodel.fieldsArray = voObj['fields']
                        voList.append(vomodel)
        except IOError, ioerr:
            self.__logger.error( '********* ValueObjectJsonParser.GetListOfValueObjects: IO Error occurred - {0}'.format(str(ioerr)))
        return voList