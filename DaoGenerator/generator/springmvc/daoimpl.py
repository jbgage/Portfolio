#!/usr/bin/env python
import os
from model.daoimpl import DaoImplModel
from model.daoimplmethod import DaoImplMethodModel
from util.constant import JsonConstants
from jinja2 import Environment , FileSystemLoader

class DaoImplClassGenerator(object):
    '''
    This class is charged with generating the DAOImpl class files (in Java)
    '''
    
    def __init__(self , configFileObj=None , deploymentUtil=None , logger=None):
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
        
    def listOfDaoImpls(self):
        '''
        This method is charged with extracting the attributes of the DAOImpl classes from the underlying JSON model
        files and creating a list model.DaoModel objects.
        
        @return: list
        '''
        daoImplList = []
        json_file_name = ''
        try:
            if self.__configFileObj is not None:
                for daoImplObj in self.__configFileObj.daoImpls():
                    daoImplModel = DaoImplModel()
                    daoImplModel.name = daoImplObj['name']
                    daoImplModel.daoImplemented = daoImplObj['dao-implemented']
                    daoImplModel.comment = daoImplObj['comment']
                    daoImplModel.methodList = self.listOfDaoImplMethods(daoImplObj['methods'])
                    daoImplList.append(daoImplModel)
        except Exception , error:
            self.__logger.error( '********** DaoImplObjectJsonParser.listOfDaoImpls: Error occurred - {0}'.format(str(error)))
        return daoImplList
    
    def listOfDaoImplMethods(self , methodList):
        '''
        This method assembles the associated method attributes for a given method as defined in the underlying 
        JSON config file and creates a list of DaoImplMethodModel objects.
        
        @param methodList: list of methods from model.DaoImplModel object
        @type methodList: list
        @return: list
        '''
        listOfDaoMethods = []
        try:
            if not methodList is None and len(methodList) > 0:
                for element in methodList:
                    implMethod = DaoImplMethodModel()
                    implMethod.methodName = element['method-name']
                    implMethod.comment = element['comment']
                    implMethod.valueObjectType = element['value-object-type']
                    implMethod.returnType = element['return-type']
                    implMethod.methodInputVariables = element['method-input-variables']
                    implMethod.storedProcedureName = element['stored-procedure-name']
                    implMethod.sqlCommandObjectInputVariables = element['sql-command-object-input-variables']
                    implMethod.resultSetParameters = element['result-set-parameters']
                    listOfDaoMethods.append(implMethod)
        except Exception , error:
            self.__logger.error( '********** DaoImplObjectJsonParser.listOfDaoImplMethods: Error occurred - {0}'.format(str(error)))
        return listOfDaoMethods   
        
    def generateClassFiles(self):
        '''
        This method assembles all of the attributes of the DAOImpl and writes them to a file based upon the associated template.
        '''
        try:
            daoImplList = self.listOfDaoImpls()
            deployment_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYDAOIMPL)
            self.__deploymentUtil.createDeploymentDirectory(deployment_directory)
            template_directory = os.path.abspath(self.__configFileObj.templateDirectoryName())
            env = Environment(loader=FileSystemLoader(template_directory))
            template = env.get_template(self.__configFileObj.daoImplTemplateFileName())
            if len(daoImplList) > 0:
                for element in daoImplList:
                    java_file_path = deployment_directory + self.__configFileObj.daoImplJavaTemplateOutputFileName().replace('{{ modelName }}' , element.name)
                    template.stream({'globalNameSpace':self.__configFileObj.globalClassNameSpace(), 
                                     'daoName': element.daoImplemented,
                                     'className': element.name, 
                                     'classComment': element.comment,
                                     'methodList':element.methodList}).dump(java_file_path)
        except Exception , error:
            self.__logger.error( '*********** DaoImplClassGenerator.generateClassFiles: Error occurred - {0}'.format(str(error)))    