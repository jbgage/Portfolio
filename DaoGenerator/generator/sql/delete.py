import os
from parser.config import ConfigJsonParser
from parser.constant import JsonConstants
from parser.sql.schema import SchemaJsonParser

class DeleteDataScriptGenerator(object):
    
    def __init__(self , configFileObj = None , deploymentUtil=None , logger=None):
        self.__configFileObj = configFileObj
        self.__deploymentUtil = deploymentUtil
        self.__logger = logger
        
    def __using_database_block(self , database_name):
        sql_output = ''
        ls = os.linesep
        try:
            sql_output = 'USE {0};{1}'.format(database_name , ls)
            sql_output += 'GO' + ls 
            sql_output += ls
        except Exception , err:
            self.__logger.error( '******** DeleteDataScriptGenerator.__using_block: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def __generate_delete_statement(self , schema_name , table_name):
        sql_output = ''
        ls = os.linesep
        try:
            sql_output += 'DELETE FROM {0}.{1};{2}'.format(schema_name , table_name , ls) 
            sql_output += 'GO' + ls
            sql_output += ls
        except Exception , err:
            self.__logger.error( '******** DeleteDataScriptGenerator.__generate_delete_statement: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def assemble_components(self , database_name , schema_name , table_list):
        sql_output = ''
        try:
            sql_output += self.__using_database_block(database_name)
            for element in table_list:
                sql_output += self.__generate_delete_statement(schema_name, element.tableName)
        except Exception , err:
            self.__logger.error( '******** DeleteDataScriptGenerator.__generate_delete_statement: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def generateSqlScript(self):
        sql_file_name = 'DeleteAllDataFromTables.sql'
        table_list = []
        tableParser = SchemaJsonParser(self.__configFileObj, self.__logger)
        try:
            sql_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYSQL)
            self.__deploymentUtil.createDeploymentDirectory(sql_directory)
            with open(sql_directory + sql_file_name , 'w+') as sql_file:
                table_list = tableParser.listOfTables()
                sql_file.write(self.assemble_components(self.__configFileObj.databaseName(), self.__configFileObj.databaseSchemaName(), table_list))
        except Exception , err:
            self.__logger.error( '******** DeleteDataScriptGenerator.__generate_delete_statement: Exception occurred - Message = {0}'.format(str(err)))