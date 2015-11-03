#!/usr/bin/env python
from model.profile import ProfileModel
from model.profilemethod import ProfileMethodModel


class ProfileObjectJsonParser(object):
    '''
    This class is charged with assembling the different values used to generate Profile class files.
    '''
    
    def __init__(self , configFileObj=None , logger=None):
        '''
        Constructor
        
        @param configFileObject: The configuration object that is passed to this class
        @type configFileObject: config.ConfigJsonParser
        @param logger: logger
        @type logger: logger
        '''
        self.__configFileObj = configFileObj
        self.__logger = logger
    
    def listOfProfiles(self):
        profileList = []
        try:
            if self.__configFileObj is not None:
                for profileObj in self.__configFileObj.profiles():
                        profModel = ProfileModel()
                        profModel.name = profileObj['name']
                        profModel.comment = profileObj['comment']
                        profModel.methodList = self.listOfProfileMethods(profileObj['methods'])
                        profileList.append(profModel) 
        except Exception , error:
            self.logger.error( '**************** ProfileObjectJsonParser.listOfProfiles(): Error occurred - {0}'.format(str(error)))
        return profileList
    
    def listOfProfileMethods(self , method_list):
        profileMethodList = []
        for element in method_list:
            profileMethod = ProfileMethodModel()
            profileMethod.methodName = element['method-name']
            profileMethod.comment = element['comment']
            profileMethod.returnType = element['return-type']
            profileMethod.daoReferenced = element['dao-referenced']
            profileMethod.inputVariableList = element['input-variables-list']
            profileMethod.daoMethodName = element['dao-method-name']
            profileMethod.daoInputParameters = element['dao-input-parameters']
            profileMethodList.append(profileMethod)
        return profileMethodList