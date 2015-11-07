#!/usr/bin/env python
import os
from jinja2 import Environment , FileSystemLoader
from util.constant import JsonConstants
from model.storedproc import StoredProcedureModel

class SqlStoredProcedureGenerator(object):
    '''
    This class is charged with generating SQL files that create SQL stored procedures (in this case, using the T-SQL syntax)
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
    
    def listOfStoredProcedures(self):
        '''
         This method converts the JSON-derived values for the list of stored procedures into a list of model.StoredProcedureModel objects
        
        @return: list
        '''
        sp_list = []
        try:
            if not self.__configFileObj is None:
                for spObj in self.__configFileObj.sqlStoredProcedures():
                    sp = StoredProcedureModel()
                    sp.name = spObj['name']
                    sp.tableName = spObj['table-name']
                    sp.storedProcedureType = spObj['stored-procedure-type']
                    sp.viewName = spObj['view-name']
                    sp.inputVariables = spObj['input-variables']
                    sp.outputVariables = spObj['output-variables']
                    sp.selectStatementFields = spObj['select-statement-fields']
                    sp.insertStatementFields = spObj['insert-statement-fields']
                    sp.updateStatementFields = spObj['update-statement-fields']
                    sp.whereClause = spObj['where-clause']
                    sp_list.append(sp)
        except IOError , ioerr:
            self.__logger.error( '****** StoredProcedureJsonParser.listOfStoredProcedures: IOError occurred - {0}'.format(str(ioerr)))
        except Exception , ioerr:
            self.__logger.error( '****** StoredProcedureJsonParser.listOfStoredProcedures: Error occurred - {0}'.format(str(err)))
        return sp_list
        
        
    def createSqlFile(self):
        spList = []
        try:
            if self.__configFileObj is not None:
                sql_deployment_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYSQL)
                self.__deploymentUtil.createDeploymentDirectory(sql_deployment_directory)
                template_sql_file_name = self.__configFileObj.createStoredProcedureScriptFileName()
                template_directory = os.path.abspath(self.__configFileObj.templateDirectoryName())
                sql_file_path = sql_deployment_directory +  template_sql_file_name
                spList = self.listOfStoredProcedures()
                if len(spList) > 0:
                    env = Environment(loader=FileSystemLoader(template_directory))
                    template = env.get_template(self.__configFileObj.createStoredProceduresTemplateFileName())
                    template.stream({'schemaName':self.__configFileObj.databaseSchemaName() , 
                                     'databaseName':self.__configFileObj.databaseName() , 
                                     'storedProcList':spList}).dump(sql_file_path)  
        except IOError, ioerror:
            self.__logger.error( '***** SqlStoredProcedureGenerator.createSqlFile: IOError occurred - {0}'.format(str(ioerror)))
        except Exception , error:
            self.__logger.error( '****** StoredProcedureJsonParser.createSqlFile: Error occurred - {0}'.format(str(error)))