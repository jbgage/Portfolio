#!/usr/bin/env python
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants
from parser.sql.ViewJsonParser import ViewJsonParser

class SqlViewScriptGenerator:
    
    __sql_file_name = '4-CreateSchemaViews'
    
    def __init__(self , pathToConfigFile = '' , logger=None):
        self._pathToConfigFile = pathToConfigFile
        self.logger = logger
    def __using_database_block(self , database_name):
        sql_output = ''
        ls = '\r\n'
        try:
                sql_output = 'USE {0};{1}'.format(database_name , ls)
                sql_output += 'GO' + ls 
                sql_output += ls
        except Exception , err:
            self.logger.error( '******** SqlViewScriptGenerator.__using_block: Exception occured - Message = {0}'.format(str(err)))
        return sql_output

    def __generate_create_view_header(self , database_name ,  schema_name , view_name):
        sql_output = ''
        ls = '\r\n'
        try:
            sql_output += 'CREATE VIEW {0}.{1} {2}'.format(schema_name , view_name , ls)
            sql_output += 'AS {0}'.format(ls)
        except Exception , err:
            self.logger.error( '******** SqlViewScriptGenerator.__generate_create_view_header: Exception occured - Message = {0}'.format(str(err)))
        return sql_output
    
    def __generate_if_view_exists_block(self , database_name , schema_name , view_name):
        sql_output = ''
        ls = '\r\n'
        try:
            sql_output += 'IF (OBJECT_ID (\'{0}.{1}\', \'V\')) IS NOT NULL {2}'.format(schema_name , view_name , ls)
            sql_output += '\tDROP VIEW {0}.{1} {2}'.format( schema_name , view_name , ls)
            sql_output += 'GO' + ls
        except Exception , err:
            self.logger.error( '******** SqlViewScriptGenerator.__generate_if_view_exists_block: Exception occured - Message = {0}'.format(str(err)))
        return sql_output
    
    
    def __generate_view_select_clause(self , select_fields):
        sql_output = ''
        select_clause = 'SELECT '
        ls = '\r\n'
        try:
            for index , element in enumerate(select_fields):
                if not element['table-alias'] is None and element['table-alias'] != '':
                    select_clause += '{0}.{1}'.format(element['table-alias'] , element['select-field'])
                else:
                    select_clause += '{0}'.format( element['select-field'])
                if index < len(select_fields)- 1:
                    select_clause += ' , ' + ls + '\t\t   '
                else:
                    select_clause += ls 
        except Exception , err:
            self.logger.error( '******** SqlViewScriptGenerator.__generate_view_select_clause: Exception occured - Message = {0}'.format(str(err)))
        sql_output = select_clause
        return sql_output

    def __generate_view_from_clause(self , database_name , schema_name ,  from_table_list ):
        sql_output = ''
        from_clause = 'FROM '
        ls = '\r\n'
        try:
            for index , element in enumerate(from_table_list):
                if not element['table-alias'] is None and element['table-alias'] != '':
                    from_clause += '{0}.{1} {2}'.format( schema_name , element['from-table-name'] , element['table-alias'])
                else:
                    from_clause += '{0}.{1}'.format(schema_name , element['from-table-name'] )
                if index < len(from_table_list) - 1:
                    from_clause += ', ' + ls + '\t\t '
            sql_output = from_clause
        except Exception , err:
            self.logger.error( '******** SqlViewScriptGenerator.__generate_view_from_clause: Exception occured - Message = {0}'.format(str(err)))
        return sql_output
    
    def __generate_view_where_clause(self , schema_name ,  where_clause_fields):
        sql_output = ''
        ls = '\r\n'
        where_clause = ls + '\tWHERE '
        try:
            if not where_clause_fields is None and len(where_clause_fields) > 0: 
                for index, element in enumerate(where_clause_fields):
                    where_clause += '{0}.{1} {2} {3}.{4}'.format( element['l-table-name'] , element['l-field-name'] , element['evaluation'] , element['r-table-name'] , element['r-field-name'])
                    if index < len(where_clause_fields) - 1:
                        where_clause += ' AND ' + ls + '\t\t  '
                sql_output = where_clause + ';' + ls
        except Exception , err:
            self.logger.error( '******** SqlViewScriptGenerator.__generate_view_where_clause: Exception occured - Message = {0}'.format(str(err)))
        return sql_output
    
    def __assemble_components(self , database_name , schema_name , view_name , select_fields , from_table_list , where_clause):
        sql_output = ''
        ls = '\r\n'
        try:
            sql_output += self.__generate_if_view_exists_block(database_name , schema_name , view_name)
            if not self.__generate_create_view_header(database_name , schema_name , view_name) is None and self.__generate_create_view_header(database_name , schema_name , view_name) != '':
                sql_output += self.__generate_create_view_header(database_name , schema_name , view_name)
            if not self.__generate_view_select_clause(select_fields) is None and self.__generate_view_select_clause(select_fields) != '':
                sql_output += '\t' + self.__generate_view_select_clause(select_fields) 
            if not self.__generate_view_from_clause(database_name , schema_name , from_table_list) is None and self.__generate_view_from_clause(database_name , schema_name , from_table_list) != '':
                sql_output += '\t' + self.__generate_view_from_clause(database_name , schema_name , from_table_list)
            if not self.__generate_view_where_clause( schema_name , where_clause) is None and self.__generate_view_where_clause(  schema_name , where_clause) != '':
                sql_output += '\t' + self.__generate_view_where_clause( schema_name , where_clause)  
            else:
                sql_output += ';' + ls
            
            sql_output += 'GO' + ls + ls
        except Exception , err:
            self.logger.error( '******** SqlViewScriptGenerator.__assemble_components: Exception occured - Message = {0}'.format(str(err)))
        return sql_output
    
    def createSqlStatement(self ,database_name ,  database_schema_name , view):
        sql_output = ''
        try:
            if not view is None:
                sql_output += self.__assemble_components(database_name , database_schema_name , view.name , view.selectClause , view.fromClause , view.whereClause)
        except Exception , error:
            self.logger.error( '***** SqlViewScriptGenerator.createSqlStatement: Error occurred - {0}'.format(str(error)))
        return sql_output    
 
    
    def createSqlFile(self):
        config = ConfigJsonParser(self._pathToConfigFile, self.logger)
        viewParser = ViewJsonParser(config.configFilePath(), self.logger)
        sql_directory = ''
        sql_file_path = ''
        view_list = []
        try:
            view_list = viewParser.listOfViews()
            if not config is None:
                sql_directory = config.deploymentDirectory(JsonConstants.DEPLOYSQL)
                sql_file_path = '{0}{1}.sql'.format(sql_directory , self.__sql_file_name)
                sql_file_obj = open(sql_file_path , 'w+')
                if (not (sql_file_obj is None)):
                    sql_file_obj.write(self.__using_database_block(config.databaseName()))
                    for views in view_list:
                        sql_file_obj.write(self.createSqlStatement(config.databaseName() , config.databaseSchemaName() , views))
                        sql_file_obj.close() 
        except IOError, ioerror:
            self.logger.error( '***** SqlViewScriptGenerator.createSqlFile: IOError occurred - {0}'.format(str(ioerror)))
        
     