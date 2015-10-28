'''
Created on Oct 26, 2012

@author: bgage
'''
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants
from parser.sql.ViewJsonParser import ViewJsonParser
from parser.sql.SchemaJsonParser import SchemaJsonParser
class DropTableViewGenerator(object):
    '''
    classdocs
    '''
    def __init__(self , configFilePath , logger = None):
        self.__configFilePath = configFilePath
        self.logger = logger
    def __using_database_block(self , database_name):
        sql_output = ''
        ls = '\r\n'
        try:
            sql_output = 'USE {0};{1}'.format(database_name , ls)
            sql_output += 'GO' + ls 
        except Exception , err:
            self.logger.error( '******** DropTableViewGenerator.__using_block: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
        
    def __generate_drop_constraint_block(self , schema_name , table_name , field_list):
        sql_output = ''
        ls = '\r\n'
        try:
            for element in field_list:
                if element.isForeignKeyConstraint is True:
                    constraint_name = ''
                    constraint_name = '{0}_{1}_FK'.format(table_name.upper() , element.foreignKeyName.upper())
                    sql_output += 'IF (OBJECT_ID (\'{0}.{1}\', \'F\')) IS NOT NULL {2}'.format(schema_name , constraint_name , ls)
                    sql_output += 'BEGIN' + ls
                    sql_output += '\t ALTER TABLE {0}.{1}{2}'.format(schema_name , table_name , ls)
                    sql_output += '\t DROP CONSTRAINT {0};{1}'.format(constraint_name , ls)
                    sql_output += 'END;' + ls
                    sql_output += 'GO' + ls
                    sql_output += ls
        except Exception , err:
            self.logger.error( '******** DropTableViewGenerator.__generate_if_constraint_exists_block: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def __generate_drop_view_block(self , schema_name ,  view_name):
        sql_output = ''
        ls = '\r\n'
        try:
            sql_output += 'IF (OBJECT_ID (\'{0}.{1}\', \'V\')) IS NOT NULL {2}'.format(schema_name , view_name , ls)
            sql_output += 'BEGIN' + ls
            sql_output += '\t DROP VIEW {0}.{1};{2}'.format(schema_name , view_name , ls)
            sql_output += 'END;' + ls
            sql_output += 'GO' + ls
            sql_output += ls
        except Exception , err:
            print '******** DropTableViewGenerator.__generate_drop_view_block: Exception occurred - Message = {0}'.format(str(err))
        return sql_output
    
    def __generate_drop_table_block(self ,  schema_name , table_name):
        sql_output = ''
        ls = '\r\n'
        try:
            sql_output += 'IF (OBJECT_ID (\'{0}.{1}\', \'U\')) IS NOT NULL {2}'.format(schema_name , table_name , ls)
            sql_output += 'BEGIN' + ls
            sql_output += '\t DROP TABLE {0}.{1};{2}'.format(schema_name , table_name , ls)
            sql_output += 'END;' + ls
            sql_output += 'GO' + ls
            sql_output += ls
        except Exception , err:
            self.logger.error( '******** DropTableViewGenerator.__generate_drop_table_block: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def __generate_drop_schema_block(self ,  schema_name ):
        sql_output = ''
        ls = '\r\n'
        try:
           
            sql_output += 'DROP SCHEMA {0};{1}'.format(schema_name ,  ls)
            sql_output += 'GO' + ls
        except Exception , err:
            self.logger.error( '******** DropTableViewGenerator.__generate_drop_schema_block: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def __assemble_components(self , database_name , schema_name , view_list , table_list):
        sql_output =  ''
        try:
            sql_output += self.__using_database_block(database_name)
            for element in table_list:
                    sql_output += self.__generate_drop_constraint_block(schema_name, element.tableName, element.fieldsArray)
                    sql_output += self.__generate_drop_table_block(schema_name, element.tableName)
            for element in view_list:
                sql_output += self.__generate_drop_view_block(schema_name , element.name)
            sql_output += self.__generate_drop_schema_block(schema_name)
        except Exception , err:
            print '******** DropTableViewGenerator.__assemble_components: Exception occurred - Message = {0}'.format(str(err))
        return sql_output
    
    def generateSqlStatement(self , database_name , schema_name , table_list , view_list  ):
        sql_output = ''
        try:
            sql_output += self.__assemble_components(database_name, schema_name, view_list, table_list)
        except Exception , err:
            self.logger.error( '******** DropTableViewGenerator.generateSqlStatement: Exception occurred - Message = {0}'.format(str(err)))
        return sql_output
    
    def generateSqlScript(self):
        config = ConfigJsonParser(self.__configFilePath, self.logger)
        viewParser = ViewJsonParser(config.configFilePath(), self.logger)
        tableParser = SchemaJsonParser(config.configFilePath(), self.logger)
        view_list = []
        table_list = []
        database_name = ''
        schema_name = ''
        sql_file_name = '6-DropTablesAndViews.sql'
        sql_file_directory = config.deploymentDirectory(JsonConstants.DEPLOYSQL)
        try:
            view_list = viewParser.listOfViews()
            table_list = tableParser.listOfTables() 
            database_name = config.databaseName()
            schema_name = config.databaseSchemaName()
            sql_file_obj = open(sql_file_directory + sql_file_name , 'w+')
            sql_file_obj.write(self.generateSqlStatement(database_name , schema_name , table_list , view_list))
            sql_file_obj.close()
        except Exception , err:
            self.logger.error( '******** DropTableViewGenerator.generateSqlScript: Exception occurred - Message = {0}'.format(str(err)))
        
        
    
    
    
    