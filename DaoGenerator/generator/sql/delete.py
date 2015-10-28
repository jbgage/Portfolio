'''
Created on Oct 27, 2012

@author: bgage
'''
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants
from parser.sql.SchemaJsonParser import SchemaJsonParser
class DeleteDataScriptGenerator(object):
    '''
    classdocs
    '''
    def __init__(self , configFilePath = '' , logger=None):
        self._configFilePath = configFilePath
        self.logger = logger
    def __using_database_block(self , database_name):
        sql_output = ''
        ls = '\r\n'
        try:
            sql_output = 'USE {0};{1}'.format(database_name , ls)
            sql_output += 'GO' + ls 
            sql_output += ls
        except Exception , err:
            self.logger.error( '******** DeleteDataScriptGenerator.__using_block: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def __generate_delete_statement(self , schema_name , table_name):
        sql_output = ''
        ls = '\r\n'
        try:
            sql_output += 'DELETE FROM {0}.{1};{2}'.format(schema_name , table_name , ls) 
            sql_output += 'GO' + ls
            sql_output += ls
        except Exception , err:
            self.logger.error( '******** DeleteDataScriptGenerator.__generate_delete_statement: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def assemble_components(self , database_name , schema_name , table_list):
        sql_output = ''
        try:
            sql_output += self.__using_database_block(database_name)
            for element in table_list:
                sql_output += self.__generate_delete_statement(schema_name, element.tableName)
        except Exception , err:
            self.logger.error( '******** DeleteDataScriptGenerator.__generate_delete_statement: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def generateSqlScript(self):
        config = ConfigJsonParser(self._configFilePath)
        sql_file_name = 'DeleteAllDataFromTables.sql'
        table_list = []
        tableParser = SchemaJsonParser(config.configFilePath(), self.logger)
        try:
            sql_directory = config.deploymentDirectory(JsonConstants.DEPLOYSQL)
            sql_file = open(sql_directory + sql_file_name , 'w+')
            table_list = tableParser.listOfTables()
            sql_file.write(self.assemble_components(config.databaseName(), config.databaseSchemaName(), table_list))
            sql_file.close()
        except Exception , err:
            self.logger.error( '******** DeleteDataScriptGenerator.__generate_delete_statement: Exception occurred - Message = {0}'.format(str(err)))
        
        
        