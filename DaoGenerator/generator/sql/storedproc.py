#!/usr/bin/env python
import os
from parser.config import ConfigJsonParser
from parser.constant import JsonConstants
from parser.sql.storedproc import StoredProcedureJsonParser
class SqlStoredProcedureGenerator:
    def __init__(self , configFileObj=None , deploymentUtil=None , logger=None):
        self.__configFileObj = configFileObj
        self.__deploymentUtil = deploymentUtil
        self.__logger = logger
    def __use_database_block(self , database_name):
        sql_output = ''
        ls = os.linesep
        try:
            sql_output += 'USE {0};{1}'.format(database_name , ls)
            sql_output += 'GO' + ls
            sql_output += ls
        except Exception , error:
            self.__logger.error( '******* SqlStoredProcedureGenerator.__use_database_block: Error occurred - {0}'.format( str(error) ))
        return sql_output
    def __if_object_exists_block(self , schema_name , stored_proc_name):
        sql_output = ''
        ls = os.linesep
        try:
            sql_output += 'IF (OBJECT_ID(\'{0}.{1}\' , \'P\')) IS NOT NULL{2}'.format(schema_name , stored_proc_name, ls)
            sql_output += '\t DROP PROCEDURE {0}.{1};{2}'.format(schema_name , stored_proc_name , ls)
            sql_output += 'GO' + ls
        except Exception, error:
            self.__logger.error( '******* SqlStoredProcedureGenerator.__if_object_exists_block: Error occurred - {0}'.format( str(error) ))
        return sql_output
    def __create_procedure_statement_block(self , schema_name , stored_procedure_name):
        sql_output = ''
        ls = os.linesep
        try:
            sql_output += 'CREATE PROCEDURE {0}.{1} {2}'.format(schema_name , stored_procedure_name , ls)
        except Exception , error:
            self.__logger.error( '******* SqlStoredProcedureGenerator.__create_procedure_statement_block: Error occured - {0}'.format( str(error) ))
        return sql_output
    def __create_input_variables_block(self , input_variables):
        sql_output = ''
        ls = os.linesep
        _input_variables = []
        try:
            if not input_variables is None and len(input_variables) > 0:
                _input_variables = input_variables
                for index , element in enumerate(_input_variables):
                        if element['field-name'].startswith('@'):
                            sql_output += '{0} '.format(element['field-name'])
                            sql_output += '{0} '.format(element['data-type'])
                            if element['data-type'].upper() == 'VARCHAR':
                                sql_output += '({0})'.format(element['length'])
                            if index < len(_input_variables) - 1:
                                sql_output += ',' + ls
                            else:
                                sql_output += ls
        except Exception , error:
            self.__logger.error( '********** __create_input_variables_block.__create_procedure_statement_block: Error occurred - {0}'.format( str(error) ))
        return sql_output
    def __create_select_statement_block(self , schema_name , table_name , view_name , select_fields_statement , where_clause):
        sql_output = ''
        ls = os.linesep
        _where_statement_fields = []
        try:
            if not select_fields_statement is None and len(select_fields_statement) > 0:
                sql_output += '\t\tSELECT {0}'.format(ls)
                for index , element in enumerate(select_fields_statement):
                    sql_output += '\t\t{0}'.format( element['field-name'] )
                    if index < len(select_fields_statement)-1:
                        sql_output += ',' + ls
                    else:
                        sql_output += ls
            if not table_name is None and table_name != '':
                sql_output += '\t\tFROM {0}.{1} {2}'.format(schema_name , table_name , ls)
            elif not view_name is None and view_name != '':
                sql_output += '\t\tFROM {0}.{1} {2}'.format(schema_name , view_name , ls)
            if not where_clause is None and len(where_clause) > 0:
                _where_statement_fields = where_clause
                sql_output += '\t\tWHERE'
                for index , element in enumerate(_where_statement_fields):
                        field_name = ''
                        variable_name = ''
                        if not element['field-name'] is None and element['field-name'] != '':
                            field_name = element['field-name']
                        if not element['input-variable-name'] is None and element['input-variable-name'] != '':
                            variable_name = element['input-variable-name']
                        if field_name != '' and variable_name != '':
                            sql_output += ' {0} = {1} '.format(field_name , variable_name)
                        if index < len(_where_statement_fields) -1:
                            sql_output += ' AND ' + ls
                        else:
                            sql_output += ls
        except Exception , error:
            self.__logger.error( '******* SqlStoredProcedureGenerator.__create_select_statement_block: Error occurred - {0}'.format( str(error) ))
        return sql_output
    def __create_insert_statement_block(self , schema_name ,  table_name , input_variables , insert_statement_fields):
        sql_output = ''
        ls = os.linesep
        _input_variables = []
        _insert_statement_fields = []
        try:
            if not table_name is None and table_name != '':
                sql_output += '\tINSERT INTO {0}.{1} ( {2}'.format(schema_name , table_name ,  ls)
                if not insert_statement_fields is None and len(insert_statement_fields) > 0:
                    _insert_statement_fields = insert_statement_fields
                    for index , element in enumerate(_insert_statement_fields):
                        sql_output += '\t\t{0}'.format(element['field-name'])
                        if index < len(_insert_statement_fields) - 1:
                            sql_output += ',' + ls
                        else:
                            sql_output += ls
                sql_output += '\t)' + ls
                sql_output += '\tVALUES (' + ls
                if not input_variables is None and len(input_variables) > 0:
                    _input_variables = input_variables
                    for index , element in enumerate(_input_variables):
                        sql_output += '\t\t{0}'.format(element['field-name'])
                        if index < len(_input_variables) - 1:
                            sql_output += ',' + ls
                        else:
                            sql_output += ls
                sql_output += '\t);' + ls
        except Exception , error:
            self.__logger.error( '******* SqlStoredProcedureGenerator.__create_insert_statement_block: Error occurred - {0}'.format( str(error) ))
        return sql_output
    def __create_update_statement_block(self , schema_name , table_name , update_statement_fields , where_fields):
        sql_output = ''
        ls  = '\r\n'
        _update_statement_fields = []
        _where_fields = []
        try:
            if not table_name is None and table_name != '':
                sql_output += '\t\tUPDATE {0}.{1} {2}'.format(schema_name , table_name , ls)
                sql_output += '\t\tSET ' + ls
                if not update_statement_fields is None and len(update_statement_fields) > 0:
                    _update_statement_fields = update_statement_fields
                if not where_fields is None and len(where_fields) > 0:
                    _where_fields = where_fields
                if not _update_statement_fields is None and len(_update_statement_fields) > 0:
                    for index , element in enumerate(_update_statement_fields):
                        field_name = ''
                        variable_name = ''
                        if not element['field-name'] is None and element['field-name'] != '':
                            field_name = element['field-name']
                        if not element['input-variable-name'] is None and element['input-variable-name'] != '':
                            variable_name = element['input-variable-name']
                        if field_name != '' and variable_name != '':
                            sql_output += '\t\t\t{0} = {1} '.format(field_name , variable_name)
                        if index < len(_update_statement_fields) -1:
                            sql_output += ',' + ls
                        else:
                            sql_output += ls
                if len(_where_fields) > 0:
                    sql_output += '\t\tWHERE ' 
                    for index , element in enumerate(_where_fields):
                        field_name = ''
                        variable_name = ''
                        if not element['field-name'] is None and element['field-name'] != '':
                            field_name = element['field-name']
                        if not element['input-variable-name'] is None and element['input-variable-name'] != '':
                            variable_name = element['input-variable-name']
                        if field_name != '' and variable_name != '':
                            sql_output += ' {0} = {1} '.format(field_name , variable_name)
                        if index < len(_where_fields) -1:
                            sql_output += ',' + ls
                        else:
                            sql_output += ls
        except Exception , error:
            self.__logger.error( '******* SqlStoredProcedureGenerator.__create_update_statement_block: Error occurred - {0}'.format( str(error) ))
        return sql_output
    def __create_delete_statement_block(self , schema_name , table_name , where_clause_fields ):
        sql_output  = ''
        ls = os.linesep
        _where_clause_fields = []
        try:
            if not where_clause_fields is None and len(where_clause_fields) > 0:
                _where_clause_fields = where_clause_fields
            if not table_name is None and table_name != '':
                sql_output += '\t\tDELETE FROM {0}.{1} {2}'.format(schema_name , table_name , ls)
            if len(_where_clause_fields) > 0:
                sql_output += '\t\tWHERE '
                for index , element in enumerate(_where_clause_fields):
                    field_name = ''
                    variable_name = ''
                    if not element['field-name'] is None and element['field-name'] != '':
                            field_name = element['field-name']
                    if not element['input-variable-name'] is None and element['input-variable-name'] != '':
                        variable_name = element['input-variable-name']
                    if field_name != '' and variable_name != '':
                        sql_output += ' {0} = {1} '.format(field_name , variable_name)
                    if index < len(_where_clause_fields) -1:
                        sql_output += ' AND ' + ls
                    else:
                        sql_output += ls
        except Exception , error:
            self.__logger.error( '******* SqlStoredProcedureGenerator.__create_delete_statement_block: Error occurred - {0}'.format( str(error) ))
        return sql_output    
    def __assemble_components(self , schema_name , stored_proc_name , table_name , view_name , stored_procedure_type , select_fields_statement , insert_statement_fields , update_statement_fields , where_clause , input_variables):
        sql_output = ''
        ls = os.linesep
        try:
            sql_output += self.__if_object_exists_block(schema_name , stored_proc_name)
            sql_output += self.__create_procedure_statement_block(schema_name , stored_proc_name)
            if not input_variables is None and len(input_variables) > 0:
                sql_output += self.__create_input_variables_block(input_variables)
            sql_output += 'AS' + ls
            sql_output += 'BEGIN' + ls
            if not stored_procedure_type is None and stored_procedure_type != '':
                if stored_procedure_type.upper() == 'SELECT':
                    sql_output += self.__create_select_statement_block(schema_name , table_name , view_name , select_fields_statement , where_clause)
                elif stored_procedure_type.upper() == 'INSERT' :
                    sql_output += self.__create_insert_statement_block(schema_name , table_name, input_variables, insert_statement_fields)
                elif stored_procedure_type.upper() == 'UPDATE' :
                    sql_output += self.__create_update_statement_block(schema_name , table_name, update_statement_fields, where_clause)
                elif stored_procedure_type.upper() == 'DELETE':
                    sql_output += self.__create_delete_statement_block(schema_name , schema_name , table_name, where_clause)
            sql_output += 'END;' + ls
            sql_output += 'GO' + ls + ls
        except Exception , error:
            self.__logger.error( '******* SqlStoredProcedureGenerator.__assemble_components: Error occurred - {0}'.format( str(error) ))
        return sql_output
    def createSqlStatement(self):
        sp_list = []
        sql_output = ''
        try:
            sp_parser = StoredProcedureJsonParser(self.__configFileObj , self.__logger)
            if not sp_parser is None:
                sp_list = sp_parser.listOfStoredProcedures()
                if not sp_list is None and len(sp_list) > 0:
                    sql_output += self.__use_database_block(self.__configFileObj.databaseName())
                    for element in sp_list:
                        sql_output += self.__assemble_components(self.__configFileObj.databaseSchemaName() , element.name, element.tableName , element.viewName, element.storedProcedureType, element.selectStatementFields, element.insertStatementFields , element.updateStatementFields , element.whereClause, element.inputVariables)
        except Exception , error:
            self.__logger.error( '******* SqlStoredProcedureGenerator.createSqlStatement: Error occurred - {0}'.format( str(error) ) )
        return sql_output
    def createSqlFile(self):
        sql_file_name = '5-CreateStoredProcedures'
        try:
            stored_procedure_file_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYSQL)
            self.__deploymentUtil.createDeploymentDirectory(stored_procedure_file_directory)
            stored_procedure_path = '{0}{1}.sql'.format(stored_procedure_file_directory , sql_file_name)
            with open(stored_procedure_path , 'w+') as stored_procedure_file_obj:
                stored_procedure_file_obj.write(self.createSqlStatement())
        except IOError, ioerror:
            self.__logger.error( '***** SqlStoredProcedureGenerator.createSqlStatement: IOError occurred - {0}'.format(str(ioerror)))   