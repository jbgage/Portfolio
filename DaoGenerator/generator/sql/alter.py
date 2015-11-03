import os
from parser.constant import JsonConstants
from parser.sql.schema import SchemaJsonParser

class AlterTableScriptGenerator(object):
    '''
    This class is charged with generating a SQL 'alter' script that contains ALTER statements
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
        
    def __use_database_block(self , database_name):
        sql_output = ''
        ls = os.linesep
        try:
            sql_output += 'USE {0};{1}'.format(database_name , ls)
            sql_output += 'GO' + ls
        except Exception , error:
            self.__logger.error( '******* AlterTableScriptGenerator.__use_database_block: Error occurred - {0}'.format( str(error) ))
        return sql_output
    
    def __if_object_exists_block(self , schema_name , table_name ,  constraint_name):
        sql_output = ''
        ls = os.linesep
        try:
            sql_output += 'IF  (OBJECT_ID(\'{0}.{1}\' , \'F\')) IS NOT NULL{2}'.format(schema_name , constraint_name, ls)
            sql_output += 'BEGIN' + ls
            sql_output += '\t ALTER TABLE {0}.{1}{2}'.format(schema_name , table_name , ls)
            sql_output += '\t DROP CONSTRAINT {0};{1}'.format(constraint_name , ls)
            sql_output += 'END;' + ls
            sql_output += 'GO' + ls
        except Exception, error:
            self.__logger.error( '******* AlterTableScriptGenerator.__if_object_exists_block: Error occurred - {0}'.format( str(error) ))
        return sql_output
    
    def __create_alter_table_statement(self , schema_name ,  table_name , constraint_name , foreign_key_name , foreign_key_table):
        alter_table_stmt = ''
        ls = os.linesep
        alter_table_stmt += 'ALTER TABLE {0}.{1}'.format(schema_name , table_name) + ls
        alter_table_stmt += 'ADD CONSTRAINT {0}'.format(constraint_name) + ls
        alter_table_stmt += 'FOREIGN KEY({0})'.format(foreign_key_name) + ls
        alter_table_stmt += 'REFERENCES {0}.{1}({2})'.format(schema_name , foreign_key_table  , foreign_key_name) + ls
        alter_table_stmt += 'GO' + ls
        return alter_table_stmt
    
    def assembleComponents(self , schema_name , table_name , field_list):
        assembled_components = ''
        ls = os.linesep
        for element in field_list:
            if element.isForeignKeyConstraint is True:
                constraint_name = ''
                constraint_name = '{0}_{1}_FK'.format(table_name.upper() , element.foreignKeyName.upper())
                assembled_components += self.__if_object_exists_block(schema_name , table_name, constraint_name)
                assembled_components += self.__create_alter_table_statement(schema_name , table_name, constraint_name, element.foreignKeyName, element.foreignKeyTable)
                assembled_components += ls
        return assembled_components
    
    def generateAlterTableScript(self):
        sql_file_name = '3-AlterSchemaTables'
        tableParser = SchemaJsonParser(self.__configFileObj , self.__logger)
        alterGen = AlterTableScriptGenerator(self.__configFileObj , self.__logger)
        tableList = []
        tableList = tableParser.listOfTables()
        file_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYSQL)
        self.__deploymentUtil.createDeploymentDirectory(file_directory)
        file_name = sql_file_name + '.sql'
        with open(file_directory + file_name , 'w+') as alter_file_obj:
            alter_file_obj.write(self.__use_database_block(self.__configFileObj.databaseName()))
            for element in tableList:
                alter_file_obj.write( alterGen.assembleComponents(self.__configFileObj.databaseSchemaName(), element.tableName , element.fieldsArray))