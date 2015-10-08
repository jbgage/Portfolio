'''
Created on Oct 24, 2012

@author: bgage
'''
import yaml
from model.ProfileModel import ProfileModel
from model.ProfileMethodModel import ProfileMethodModel
from parser.ConfigYamlParser import ConfigYamlParser
from parser.YamlConstants import YamlConstants

class ProfileObjectYamlParser(object):
   
    def __init__(self , configFilePath = '' , logger=None):
        self._configFilePath = configFilePath
        self.logger = logger
    def listOfProfiles(self):
        profileList = []
        config = ConfigYamlParser(self._configFilePath , self.logger)
        try:
            profile_file_path = config.yamlModelFilePath(YamlConstants.YAMLPROFILE) 
            profile_file_obj = open(profile_file_path , 'rb')
            profile_ingest = profile_file_obj.read()
            profile_file_obj.close()
            for yaml_parser in yaml.load_all(profile_ingest):
                profModel = ProfileModel()
                profModel.name = yaml_parser['name']
                profModel.comment = yaml_parser['comment']
                profModel.methodList = self.listOfProfileMethods(yaml_parser['methods'])
                profileList.append(profModel) 
        except Exception , error:
            self.logger.error( '**************** ProfileObjectYamlParser.listOfProfiles(): Error occurred - {0}'.format(str(error)))
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
        
        