#!/usr/bin/env python
import os
from parser.sql.schema import SchemaJsonParser
from parser.constant import JsonConstants

class SqlTableScriptGenerator(object):
    '''
    This class is charged with creating a SQL script that contains a series of CREATE TABLE statements.
    '''
    
    __open_brace = '('
    __close_brace = ')'
    __end_statement = ';'
    
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
        
    def __using_database_block(self , database_name , schema_name):
        sql_output = ''
        ls = os.linesep
        try:
                sql_output = 'USE {0};{1}'.format(database_name , ls)
                sql_output += 'GO' + ls
                sql_output += 'CREATE SCHEMA {0};'.format(schema_name) + ls
        except Exception , err:
            self.__logger.error( '******** SqlTableScriptGenerator.__using_database_block: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def __generate_create_table_header(self , tableName , tab_char):
        sql_output = ''
        ls = os.linesep
        try:
            sql_output += tab_char +  'CREATE TABLE {0} {1}'.format(tableName , ls)
        except Exception , err:
            self.__logger.error( '******** SqlTableScriptGenerator.__generate_create_table_header: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def __generate_table_field_contents(self , fieldArray  , tab_char):
        ls = os.linesep
        sql_output = ''
        fields_definition = ''
        try:
            if not fieldArray is None:
                if len(fieldArray) > 0:
                    sql_output += tab_char + self.__open_brace + ls
                    for index , element in enumerate(fieldArray):
                        fields_definition += tab_char + tab_char + element.fieldName.upper() + ' '
                        if (element.dataType.upper() == 'VARCHAR'):
                            fields_definition += ' {0} ({1}) '.format(element.dataType.upper() , element.length)
                        else:
                            fields_definition +=  ' {0} '.format(element.dataType.upper())
                        if element.isPrimaryKey == True:
                            fields_definition += ' PRIMARY KEY '
                        if element.autoIncrement == True:
                            fields_definition += ' IDENTITY '
                        if index < len(fieldArray) - 1:
                            fields_definition += ',' + ls
                        else:
                            fields_definition += ls
                    sql_output += fields_definition
                    sql_output += tab_char + self.__close_brace + ls
        except Exception , err:
            self.__logger.error( '******** SqlTableScriptGenerator.__generate_table_field_contents: Exception occured - Message = {0}'.format(str(err)))
        return sql_output
    
    def __assemble_components(self , tableName , fieldArr , tab_char):
        component_definition = ''
        component_definition += self.__generate_create_table_header(tableName , tab_char)
        component_definition += self.__generate_table_field_contents(fieldArr , tab_char)
        return component_definition
    
    def createSqlStatement(self):
        table_parser = SchemaJsonParser(self.__configFileObj , self.__logger)
        table_list = []
        ls = os.linesep
        tab_char = '\t'
        sql_output = ''
        try:
            if not table_parser is None:
                table_list = table_parser.listOfTables()
                sql_output += self.__using_database_block(self.__configFileObj.databaseName() , self.__configFileObj.databaseSchemaName())
                if not table_list is None and len(table_list) > 0:
                    for element in table_list:
                        sql_output += self.__assemble_components(element.tableName, element.fieldsArray , tab_char)
                    sql_output += 'GO;'
        except Exception , error:
            self.__logger.error( '***** SqlTableScriptGenerator.createSqlStatement: Error occurred - {0}'.format(str(error)))
        return sql_output
    
    def createSqlFile(self):
        template_sql_file_name = '2-CreateSchemaTables'
        sql_deployment_directory = ''
        sql_file_name = ''
        try:
            sql_deployment_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYSQL)
            self.__deploymentUtil.createDeploymentDirectory(sql_deployment_directory)
            sql_file_name = '{0}/{1}.sql'.format(sql_deployment_directory , template_sql_file_name)
            with open(sql_file_name , 'w+') as sql_file_obj:
                sql_file_obj.write(self.createSqlStatement())
        except IOError , ioerror:
            self.__logger.error( '***** SqlTableScriptGenerator.createSqlFile: Error occurred - {0}'.format(str(ioerror)))