#!/usr/bin/env python
import json
import os
from parser.constants import JsonConstants

class ConfigJsonParser:
    
    
    def __init__(self , absoluteConfigFilePath = '' , logger=None):
        self._jsonConfigFilePath = absoluteConfigFilePath
        self.logger = logger
        
    def configFilePath(self):
        return self._jsonConfigFilePath
   
    def databaseName(self):
        database_name = ''
        try:
            configFile = open(self.configFilePath() , 'r')
            if not configFile is None:
                config_file_ingest = configFile.read()
                config_json = json.load(config_file_ingest)
                database_name = config_json['databaseName']
            configFile.flush()
            configFile.close()
        except IOError, ioerr:
            self.logger.error( '***** ConfigJsonParser.databaseSchemaName: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #    print '***** ConfigJsonParser: Error occured - {0}'.format(str(err))
        return database_name
   
    def databaseSchemaName(self):
        database_schema_name = ''
        try:
            configFile = open(self.configFilePath() , 'r')
            if not configFile is None:
                config_file_ingest = configFile.read()
                config_json = json.load(config_file_ingest)
                database_schema_name = config_json['databaseSchemaName']
            configFile.flush()
            configFile.close()
        except IOError, ioerr:
            self.logger.error( '***** ConfigJsonParser.databaseSchemaName: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #    print '***** ConfigJsonParser: Error occured - {0}'.format(str(err))
        return database_schema_name
    
    
    def globalClassNameSpace(self):
        global_class_namespace = ''
        try:
            configFile = open(self.configFilePath() , 'r')
            if not configFile is None:
                config_file_ingest = configFile.read()
                config_json = json.load(config_file_ingest)
                global_class_namespace = config_json['globalClassNameSpace']
            configFile.flush()
            configFile.close()
        except IOError, ioerr:
            self.logger.error( '***** ConfigJsonParser.globalClassNameSpace: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #    print '***** ConfigJsonParser: Error occured - {0}'.format(str(err))
        
        return global_class_namespace
    
    
    def jsonModelFilePath(self , modelName):
        json_file_name = ''
        json_directory = ''
        try:
            if os.path.isfile(self.configFilePath()):
                config_file_obj = open(self.configFilePath() , 'rb')
                config_file_ingest = config_file_obj.read()
                json_object = json.load(config_file_ingest)
                config_file_obj.flush()
                config_file_obj.close()
                json_directory = self.deploymentDirectory(JsonConstants.YAMLCONFIG)
                if not json_object is None:
                    if modelName == JsonConstants.YAMLVALUEOBJECT:
                        json_file_name = json_object['jsonModelFiles']['valueObject']
                    elif modelName == JsonConstants.YAMLSCHEMA:
                        json_file_name = json_object['jsonModelFiles']['database']['schema']
                    elif modelName == JsonConstants.YAMLVIEW:
                        json_file_name = json_object['jsonModelFiles']['database']['view']
                    elif modelName == JsonConstants.YAMLSTOREDPROCEDURES:
                        json_file_name = json_object['jsonModelFiles']['database']['storedProcedures']
                    elif modelName == JsonConstants.YAMLPROFILE:
                        json_file_name = json_object['jsonModelFiles']['profile']
                    elif modelName == JsonConstants.YAMLDAO:
                        json_file_name = json_object['jsonModelFiles']['persistence']['dao']
                    elif modelName == JsonConstants.YAMLDAOIMPL:
                        json_file_name = json_object['jsonModelFiles']['persistence']['daoImpl']
                    elif modelName == JsonConstants.YAMLDAOFACTORY:
                        json_file_name = json_object['jsonModelFiles']['persistence']['daoFactory']
        except IOError, ioerr:
            self.logger.error( '***** ConfigJsonParser.jsonModelFilePath: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #   print '***** ConfigJsonParser: Error occured - {0}'.format(str(err))
        return json_directory + json_file_name
    
   
    def deploymentDirectory(self , directory_name):
        outputDirectory = ''
        try:
            if os.path.isfile(self.configFilePath()):
                config_file_obj = open(self.configFilePath() , 'rb')
                config_file_ingest = config_file_obj.read()
                config_file_obj.flush()
                config_file_obj.close()
                json_object = json.load(config_file_ingest)
                if not json_object is None:
                    if directory_name ==  JsonConstants.DEPLOYMODEL:
                        main_directory_name = json_object['directories']['main-deployment-dir']
                        subDirectory = json_object['directories']['deploy']['model']
                        outputDirectory = main_directory_name + subDirectory
                    elif directory_name == JsonConstants.DEPLOYPROFILE:
                        main_directory_name = json_object['directories']['main-deployment-dir']
                        subDirectory = json_object['directories']['deploy']['profile']
                        outputDirectory = main_directory_name + subDirectory
                    elif directory_name == JsonConstants.DEPLOYDAO:
                        main_directory_name = json_object['directories']['main-deployment-dir']
                        daoDirectory = json_object['directories']['deploy']['persistence']['dao']
                        outputDirectory = main_directory_name +  daoDirectory
                    elif directory_name == JsonConstants.DEPLOYDAOIMPL:
                        main_directory_name = json_object['directories']['main-deployment-dir']
                        daoImplDirectory = json_object['directories']['deploy']['persistence']['daoImpl']
                        outputDirectory = main_directory_name + daoImplDirectory
                    elif directory_name == JsonConstants.DEPLOYFACTORY:
                        main_directory_name = json_object['directories']['main-deployment-dir']
                        factoryDirectory = json_object['directories']['deploy']['persistence']['factory']
                        outputDirectory = main_directory_name + factoryDirectory 
                    elif directory_name == JsonConstants.DEPLOYSQL:
                        main_directory_name = json_object['directories']['main-deployment-dir']
                        subdirectory = json_object['directories']['deploy']['sql']
                        outputDirectory = main_directory_name + subdirectory
                    elif directory_name == JsonConstants.YAMLCONFIG:
                        main_directory_name = json_object['directories']['config']
                        outputDirectory = main_directory_name
        except IOError, ioerr:
            self.logger.error( '***** ConfigJsonParser.deploymentDirectory: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #    print '***** ConfigJsonParser: Error occured - {0}'.format(str(err))
        return outputDirectory
                


    
    
    

