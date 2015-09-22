#!/usr/bin/env python
import yaml
import os
from parser.YamlConstants import YamlConstants

class ConfigYamlParser:
    
    
    def __init__(self , absoluteConfigFilePath = '' , logger=None):
        self._yamlConfigFilePath = absoluteConfigFilePath
        self.logger = logger
        
    def configFilePath(self):
        return self._yamlConfigFilePath
   
    def databaseName(self):
        database_name = ''
        try:
            configFile = open(self.configFilePath() , 'r')
            if not configFile is None:
                config_file_ingest = configFile.read()
                config_yaml = yaml.load(config_file_ingest)
                database_name = config_yaml['databaseName']
            configFile.flush()
            configFile.close()
        except IOError, ioerr:
            self.logger.error( '***** ConfigYamlParser.databaseSchemaName: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #    print '***** ConfigYamlParser: Error occured - {0}'.format(str(err))
        return database_name
   
    def databaseSchemaName(self):
        database_schema_name = ''
        try:
            configFile = open(self.configFilePath() , 'r')
            if not configFile is None:
                config_file_ingest = configFile.read()
                config_yaml = yaml.load(config_file_ingest)
                database_schema_name = config_yaml['databaseSchemaName']
            configFile.flush()
            configFile.close()
        except IOError, ioerr:
            self.logger.error( '***** ConfigYamlParser.databaseSchemaName: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #    print '***** ConfigYamlParser: Error occured - {0}'.format(str(err))
        return database_schema_name
    
    
    def globalClassNameSpace(self):
        global_class_namespace = ''
        try:
            configFile = open(self.configFilePath() , 'r')
            if not configFile is None:
                config_file_ingest = configFile.read()
                config_yaml = yaml.load(config_file_ingest)
                global_class_namespace = config_yaml['globalClassNameSpace']
            configFile.flush()
            configFile.close()
        except IOError, ioerr:
            self.logger.error( '***** ConfigYamlParser.globalClassNameSpace: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #    print '***** ConfigYamlParser: Error occured - {0}'.format(str(err))
        
        return global_class_namespace
    
    
    def yamlModelFilePath(self , modelName):
        yaml_file_name = ''
        yaml_directory = ''
        try:
            if os.path.isfile(self.configFilePath()):
                config_file_obj = open(self.configFilePath() , 'rb')
                config_file_ingest = config_file_obj.read()
                yaml_object = yaml.load(config_file_ingest)
                config_file_obj.flush()
                config_file_obj.close()
                yaml_directory = self.deploymentDirectory(YamlConstants.YAMLCONFIG)
                if not yaml_object is None:
                    if modelName == YamlConstants.YAMLVALUEOBJECT:
                        yaml_file_name = yaml_object['yamlModelFiles']['valueObject']
                    elif modelName == YamlConstants.YAMLSCHEMA:
                        yaml_file_name = yaml_object['yamlModelFiles']['database']['schema']
                    elif modelName == YamlConstants.YAMLVIEW:
                        yaml_file_name = yaml_object['yamlModelFiles']['database']['view']
                    elif modelName == YamlConstants.YAMLSTOREDPROCEDURES:
                        yaml_file_name = yaml_object['yamlModelFiles']['database']['storedProcedures']
                    elif modelName == YamlConstants.YAMLPROFILE:
                        yaml_file_name = yaml_object['yamlModelFiles']['profile']
                    elif modelName == YamlConstants.YAMLDAO:
                        yaml_file_name = yaml_object['yamlModelFiles']['persistence']['dao']
                    elif modelName == YamlConstants.YAMLDAOIMPL:
                        yaml_file_name = yaml_object['yamlModelFiles']['persistence']['daoImpl']
                    elif modelName == YamlConstants.YAMLDAOFACTORY:
                        yaml_file_name = yaml_object['yamlModelFiles']['persistence']['daoFactory']
        except IOError, ioerr:
            self.logger.error( '***** ConfigYamlParser.yamlModelFilePath: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #   print '***** ConfigYamlParser: Error occured - {0}'.format(str(err))
        return yaml_directory + yaml_file_name
    
   
    def deploymentDirectory(self , directory_name):
        outputDirectory = ''
        try:
            if os.path.isfile(self.configFilePath()):
                config_file_obj = open(self.configFilePath() , 'rb')
                config_file_ingest = config_file_obj.read()
                config_file_obj.flush()
                config_file_obj.close()
                yaml_object = yaml.load(config_file_ingest)
                if not yaml_object is None:
                    if directory_name ==  YamlConstants.DEPLOYMODEL:
                        main_directory_name = yaml_object['directories']['main-deployment-dir']
                        subDirectory = yaml_object['directories']['deploy']['model']
                        outputDirectory = main_directory_name + subDirectory
                    elif directory_name == YamlConstants.DEPLOYPROFILE:
                        main_directory_name = yaml_object['directories']['main-deployment-dir']
                        subDirectory = yaml_object['directories']['deploy']['profile']
                        outputDirectory = main_directory_name + subDirectory
                    elif directory_name == YamlConstants.DEPLOYDAO:
                        main_directory_name = yaml_object['directories']['main-deployment-dir']
                        daoDirectory = yaml_object['directories']['deploy']['persistence']['dao']
                        outputDirectory = main_directory_name +  daoDirectory
                    elif directory_name == YamlConstants.DEPLOYDAOIMPL:
                        main_directory_name = yaml_object['directories']['main-deployment-dir']
                        daoImplDirectory = yaml_object['directories']['deploy']['persistence']['daoImpl']
                        outputDirectory = main_directory_name + daoImplDirectory
                    elif directory_name == YamlConstants.DEPLOYFACTORY:
                        main_directory_name = yaml_object['directories']['main-deployment-dir']
                        factoryDirectory = yaml_object['directories']['deploy']['persistence']['factory']
                        outputDirectory = main_directory_name + factoryDirectory 
                    elif directory_name == YamlConstants.DEPLOYSQL:
                        main_directory_name = yaml_object['directories']['main-deployment-dir']
                        subdirectory = yaml_object['directories']['deploy']['sql']
                        outputDirectory = main_directory_name + subdirectory
                    elif directory_name == YamlConstants.YAMLCONFIG:
                        main_directory_name = yaml_object['directories']['config']
                        outputDirectory = main_directory_name
        except IOError, ioerr:
            self.logger.error( '***** ConfigYamlParser.deploymentDirectory: IOError occurred - {0}'.format(str(ioerr)))
        #except Exception , err:
        #    print '***** ConfigYamlParser: Error occured - {0}'.format(str(err))
        return outputDirectory
                


    
    
    

