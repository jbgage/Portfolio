#!/usr/bin/env python
import os
from jinja2 import Environment , FileSystemLoader
from util.constant import JsonConstants
from model.table import TableModel
from model.tablefield import TableFieldModel

class SqlTableScriptGenerator(object):
    '''
    This class is charged with creating a SQL script from the underlying template that
    contains a series of CREATE TABLE statements.
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
        
    def listOfTables(self):
        '''
        This method converts the JSON-derived values for the list of tables into a list of model.TableModel objects
        
        @return: list
        '''
        table_model_list = []
        try:
            for tableObj in self.__configFileObj.sqlTables():
                    tablemodel = TableModel()
                    tablemodel.tableName = tableObj['name']
                    tablemodel.fieldsArray = self.listOfTableField(tableObj['fields'])
                    table_model_list.append(tablemodel)
        except IOError, ioerr:
            self.__logger.error( '***** SqlTableScriptGenerator.listOfTables: IO Error occured - {0}'.format(str(ioerr)))
        except Exception, err:
            self.__logger.error( '***** SqlTableScriptGenerator.listOfTables: Error occured - {0}'.format(str(err)))
        return table_model_list
    
    def listOfTableField(self , method_list=[]):
        '''
        This method further decomposes the table fields into a list of model.TableFieldModel objects
        
        @param method_list: This is the list of fields from the model.TableModel.fieldsArray object
        @type method_list: list
        @return: list
        '''
        tableMethodList = []
        for element in method_list:
            field = TableFieldModel()
            field.fieldName = element['field-name']
            field.dataType = element['data-type']
            field.length = element['length']
            field.isPrimaryKey = element['is-primary-key']
            field.autoIncrement = element['auto-increment']
            field.isForeignKeyConstraint = element['is-foreign-key-constraint']
            field.foreignKeyName = element['foreign-key-name']
            field.foreignKeyTable = element['foreign-key-table']
            tableMethodList.append(field)
        return tableMethodList
        
    def createSqlFile(self):
        '''
        This method assembles all of the values that comprise the CREATE TABLE SQL script and renders the corresponding Jinja template.
        It then writes this file to the operating system per the underlying directory specifications.
        '''
        template_sql_file_name = ''
        sql_deployment_directory = ''
        sql_file_name = ''
        tableList = []
        try:
            if self.__configFileObj is not None:
                sql_deployment_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYSQL)
                self.__deploymentUtil.createDeploymentDirectory(sql_deployment_directory)
                template_sql_file_name = self.__configFileObj.createTablesScriptFileName()
                sql_file_path = sql_deployment_directory +  template_sql_file_name
                tableList = self.listOfTables()
                if len(tableList) > 0:
                    template_directory = os.path.abspath(self.__configFileObj.templateDirectoryName())
                    env = Environment(loader=FileSystemLoader(template_directory))
                    template = env.get_template(self.__configFileObj.createTablesTemplateFileName())
                    template.stream({'schemaName':self.__configFileObj.databaseSchemaName() , 
                                     'databaseName':self.__configFileObj.databaseName() , 
                                     'tableList':tableList}).dump(sql_file_path)  
        except IOError , ioerror:
            self.__logger.error( '***** SqlTableScriptGenerator.createSqlFile: IOError occurred - {0}'.format(str(ioerror)))
        except Exception , error:
            self.__logger.error( '***** SqlTableScriptGenerator.createSqlFile: Error occurred - {0}'.format(str(error)))