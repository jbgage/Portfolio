#!/usr/bin/env python
import os
from model.dao import DaoModel
from model.daomethod import DaoMethodModel
from util.constant import JsonConstants
from jinja2 import Environment , FileSystemLoader

class DaoClassGenerator(object):
    '''
    This class is charged with generating the DAO interfaces in Java.
    '''
    
    def __init__(self , configFileObj = None , deploymentUtil=None , logger=None):
        '''
        Constructor
        
        @param configFileObj: The parser.config.ConfigJsonParser object passed to this class
        @type configFileObj: parser.config.ConfigJsonParser
        @param deploymentUtil: The deploy.DeploymentUtil object passed to the Generator
        @type deploymentUtil:deploy.DeploymentUtil
        @param logger: The logger object
        @type logger: logger
        '''
        self.__configFileObj = configFileObj
        self.__deploymentUtil = deploymentUtil
        self.__logger = logger
        
    def listOfDaos(self):
        '''
        This method loads the JSON-formatted Java DAO Interfaces into a list of model.DaoModel objects
        
        @return: list
        '''
        daoList = []
        try:
            for daoModelObj in self.__configFileObj.daos():
                daoModel = DaoModel()
                daoModel.name = daoModelObj['name']
                daoModel.comment = daoModelObj['comment']
                daoModel.methodList = self.listOfDaoMethods(daoModelObj['methods'])
                daoList.append(daoModel)
        except Exception , error:
            self.__logger.error( '**************** DaoObjectJsonParser.listOfDaos(): Error occurred - {0}'.format(str(error)))
        return daoList
    
    def listOfDaoMethods(self , method_list):
        '''
        This method loads the attributes of the interface methods as defined in the appropriate JSON model and creates a list of model.DaoMethodModel objects.
        
        @param method_list: List of methods
        @type method_list: list
        @return: list
        '''
        daoMethodList = []
        try:
            for element in method_list:
                daoMethodModel = DaoMethodModel()
                daoMethodModel.methodName = element['method-name']
                daoMethodModel.returnType = element['return-type']
                daoMethodModel.inputVariables = element['input-variables']
                daoMethodList.append(daoMethodModel)
        except Exception , error:
            self.__logger.error( '**************** DaoObjectJsonParser.listOfDaoMethods(): Error occurred - {0}'.format(str(error)))
        return daoMethodList
        
    
    
    def generateInterfaceFiles(self):
        daoList = []
        try:
            daoList = self.listOfDaos()
            if len(daoList) > 0:
                deployment_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYDAO)
                self.__deploymentUtil.createDeploymentDirectory(deployment_directory)
                template_directory = os.path.abspath(self.__configFileObj.templateDirectoryName())
                env = Environment(loader=FileSystemLoader(template_directory))
                template = env.get_template(self.__configFileObj.daoTemplateFileName())
                for element in daoList:
                    java_file_path = deployment_directory + self.__configFileObj.daoJavaTemplateOutputFileName().replace('{{ modelName }}' , element.name)
                    template.stream({'globalNameSpace':self.__configFileObj.globalClassNameSpace() , 
                                     'interfaceName': element.name , 
                                     'interfaceComment': element.comment,
                                     'methodList':element.methodList}).dump(java_file_path)  
        except Exception , error:
            self.__logger.error( '*********** DaoClassGenerator.generateInterfaceFiles: Error occurred - {0}'.format(str(error)))       