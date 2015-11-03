#!/usr/bin/env python
from model.valueobject import VoModel


class ValueObjectJsonParser(object):
    '''
    This class is charged with assembling the different values used to create the ValueObject java files.
    '''
    
    def __init__(self , configFileObj = None , logger=None):
        '''
        Constructor
        
        @param configFileObject: The configuration object that is passed to this class
        @type configFileObject: config.ConfigJsonParser
        @param logger: logger
        @type logger: logger
        '''
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