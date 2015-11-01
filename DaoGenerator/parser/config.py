#!/usr/bin/env python
import json
import os
from constant import JsonConstants
from util.configutil import ConfigurationUtil
class ConfigJsonParser:
    def __init__(self , configFileObj=None , logger=None):
        self.__configFileObj = configFileObj
        self.__logger = logger
    def databaseName(self):
        return self.__configFileObj['main-config']['databaseName']   
    def databaseSchemaName(self):
        return self.__configFileObj['main-config']['databaseSchemaName']
    def globalClassNameSpace(self):
        return self.__configFileObj['main-config']['globalClassNameSpace']
    def sqlTables(self):
        return self.__configFileObj['database']['schema']['table']
    def sqlViews(self):
        return self.__configFileObj['database']['views']['view']
    def sqlStoredProcedures(self):
        return self.__configFileObj['database']['stored-procedures']['stored-procedure']
    def profiles(self):
        return self.__configFileObj['profile']
    def valueObjects(self):
        return self.__configFileObj['value-object']['value-object']
    def daos(self):
        return self.__configFileObj['persistence']['dao']['dao']
    def daoImpls(self):
        return self.__configFileObj['persistence']['dao-impl']['dao-impl']
    def daoFactories(self):
        return self.__configFileObj['persistence']['dao-factory']
    def jsonModelFilePath(self , modelName):
        json_file_name = ''
        json_directory = ''
        try:
            json_directory = self.deploymentDirectory(JsonConstants.JSONCONFIG)
            if not self.__configFileObj is None:
                if modelName == JsonConstants.JSONVALUEOBJECT:
                    json_file_name = self.__configFileObj['jsonModelFiles']['valueObject']
                elif modelName == JsonConstants.JSONSCHEMA:
                    json_file_name = self.__configFileObj['jsonModelFiles']['database']['schema']
                elif modelName == JsonConstants.JSONVIEW:
                    json_file_name = self.__configFileObj['jsonModelFiles']['database']['view']
                elif modelName == JsonConstants.JSONSTOREDPROCEDURES:
                    json_file_name = self.__configFileObj['jsonModelFiles']['database']['storedProcedures']
                elif modelName == JsonConstants.JSONPROFILE:
                    json_file_name = self.__configFileObj['jsonModelFiles']['profile']
                elif modelName == JsonConstants.JSONDAO:
                    json_file_name = self.__configFileObj['jsonModelFiles']['persistence']['dao']
                elif modelName == JsonConstants.JSONDAOIMPL:
                    json_file_name = self.__configFileObj['jsonModelFiles']['persistence']['daoImpl']
                elif modelName == JsonConstants.JSONDAOFACTORY:
                    json_file_name = self.__configFileObj['jsonModelFiles']['persistence']['daoFactory']
        except IOError, ioerr:
            self.__logger.error( '***** ConfigJsonParser.jsonModelFilePath: IOError occurred - {0}'.format(str(ioerr)))
        return json_directory + json_file_name
    def mainDeploymentDirectory(self):
        return self.__configFileObj['main-config']['directories']['main-deployment-dir']
    def deploymentDirectory(self , directory_name):
        outputDirectory = ''
        try:
            if not self.__configFileObj is None:
                if directory_name ==  JsonConstants.DEPLOYMODEL:
                    main_directory_name = self.__configFileObj['main-config']['directories']['main-deployment-dir']
                    subDirectory = self.__configFileObj['main-config']['directories']['deploy']['model']
                    outputDirectory = main_directory_name + subDirectory
                elif directory_name == JsonConstants.DEPLOYPROFILE:
                    main_directory_name = self.__configFileObj['main-config']['directories']['main-deployment-dir']
                    subDirectory = self.__configFileObj['main-config']['directories']['deploy']['profile']
                    outputDirectory = main_directory_name + subDirectory
                elif directory_name == JsonConstants.DEPLOYDAO:
                    main_directory_name = self.__configFileObj['main-config']['directories']['main-deployment-dir']
                    daoDirectory = self.__configFileObj['main-config']['directories']['deploy']['persistence']['dao']
                    outputDirectory = main_directory_name +  daoDirectory
                elif directory_name == JsonConstants.DEPLOYDAOIMPL:
                    main_directory_name = self.__configFileObj['main-config']['directories']['main-deployment-dir']
                    daoImplDirectory = self.__configFileObj['main-config']['directories']['deploy']['persistence']['daoImpl']
                    outputDirectory = main_directory_name + daoImplDirectory
                elif directory_name == JsonConstants.DEPLOYFACTORY:
                    main_directory_name = self.__configFileObj['main-config']['directories']['main-deployment-dir']
                    factoryDirectory = self.__configFileObj['main-config']['directories']['deploy']['persistence']['factory']
                    outputDirectory = main_directory_name + factoryDirectory 
                elif directory_name == JsonConstants.DEPLOYSQL:
                    main_directory_name = self.__configFileObj['main-config']['directories']['main-deployment-dir']
                    subdirectory = self.__configFileObj['main-config']['directories']['deploy']['sql']
                    outputDirectory = main_directory_name + subdirectory
                elif directory_name == JsonConstants.JSONCONFIG:
                    main_directory_name = self.__configFileObj['main-config']['directories']['config']
                    outputDirectory = main_directory_name
        except IOError, ioerr:
            self.__logger.error( '***** ConfigJsonParser.deploymentDirectory: IOError occurred - {0}'.format(str(ioerr)))
        return outputDirectory