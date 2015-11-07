#!/usr/bin/env python
import os
from model.valueobject import VoModel
from util.constant import JsonConstants
from jinja2 import Environment , FileSystemLoader

class ValueObjectClassGenerator(object):
    '''
    This class is charged to generate the ValueObject class files based upon the corresponding GOF design patter
    '''
 
    
    def __init__(self , configFileObject = None , deploymentUtil=None , logger=None):
        '''
        Constructor
        
        @param configFileObj: The parser.config.ConfigJsonParser object passed to this class
        @type configFileObj: parser.config.ConfigJsonParser
        @param deploymentUtil: The deploy.DeploymentUtil object passed to the Generator
        @type deploymentUtil:deploy.DeploymentUtil
        @param logger: The logger object
        @type logger: logger
        '''
        self.__configFileObj = configFileObject
        self.__deploymentUtil = deploymentUtil
        self.__logger = logger
        
    def listOfValueObjects(self):
        '''
        This method retrieves all of the VO attributes from the associated JSON file and returns a list of model.VoModel objects
        
        @return: list
        '''
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
        
        
    def generateClassFiles(self):
        '''
        This method assembles all of the attributes of the DAOImpl and writes them to a file based upon the associated template.
        '''
        voList = []
        try:
            voList = self.listOfValueObjects()
            deployment_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYMODEL)
            self.__deploymentUtil.createDeploymentDirectory(deployment_directory)
            template_directory = os.path.abspath(self.__configFileObj.templateDirectoryName())
            env = Environment(loader=FileSystemLoader(template_directory))
            template = env.get_template(self.__configFileObj.valueObjectTemplateFileName())
            if len(voList) > 0:
                for element in voList:
                    java_file_path = deployment_directory + self.__configFileObj.valueObjectJavaTemplateOutputFileName().replace('{{ modelName }}' , element.modelName)
                    template.stream({'globalNameSpace':self.__configFileObj.globalClassNameSpace(), 
                                     'className': element.modelName,
                                     'fieldsArray':element.fieldsArray}).dump(java_file_path)
        except Exception , error:
            self.__logger.error( '*********** ValueObjectClassGenerator.generateClassFiles: Error occurred - {0}'.format(str(error)))    