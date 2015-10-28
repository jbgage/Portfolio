'''
Created on Oct 24, 2012

@author: bgage
'''
import json
from model.ProfileModel import ProfileModel
from model.ProfileMethodModel import ProfileMethodModel
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants

class ProfileObjectJsonParser(object):
   
    def __init__(self , configFilePath = '' , logger=None):
        self._configFilePath = configFilePath
        self.logger = logger
    def listOfProfiles(self):
        profileList = []
        config = ConfigJsonParser(self._configFilePath , self.logger)
        try:
            profile_file_path = config.jsonModelFilePath(JsonConstants.YAMLPROFILE) 
            profile_file_obj = open(profile_file_path , 'rb')
            profile_ingest = profile_file_obj.read()
            profile_file_obj.close()
            for json_parser in json.load_all(profile_ingest):
                profModel = ProfileModel()
                profModel.name = json_parser['name']
                profModel.comment = json_parser['comment']
                profModel.methodList = self.listOfProfileMethods(json_parser['methods'])
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
        
        