'''
Created on Oct 23, 2012

@author: bgage
'''
from model.DaoModel import DaoModel
from model.DaoMethodModel import DaoMethodModel
from parser.constants import JsonConstants
from parser.ConfigJsonParser import ConfigJsonParser
from parser.pattern.DaoObjectJsonParser import DaoObjectJsonParser
import logging
class DaoClassGenerator(object):
   
    def __init__(self , configFilePath = '' , logger=None):
        self._configFilePath = configFilePath
        self.logger = logger
    
    def _import_block(self , global_namespace):
        ls = '\r\n'
        import_block = ''
        import_block += 'import java.util.List;' + ls
        import_block += 'import {0}.model;{1}'.format(global_namespace , ls)
        return import_block
    
    def _package_declaration(self , global_namespace):
        ls = '\r\n'
        namespace_block = ''
        namespace_block += 'package {0}.persistence.dao{1}'.format(global_namespace , ls)
        return namespace_block
    
    def _interface_definition_block(self , class_name , tab_char):
        ls = '\r\n'
        interface_declaration = '{0}public interface {1}  {2}'.format(tab_char , class_name , ls)
        return interface_declaration
    
    def _interface_comment_block(self , class_comment , tab_char):
        class_comment_output = ''
        ls = '\r\n'
        if not class_comment is None and class_comment != '':
            class_comment_output += tab_char + '/' + ('*' * (len(class_comment) + 1)) + ls
            class_comment_output += tab_char + '-  {0}{1}'.format(class_comment , ls)
            class_comment_output += tab_char + ('*' * (len(class_comment) + 1)) + '/' + ls
        return class_comment_output
       
    def _method_declaration(self , method_name , return_type ,  method_input_variables , tab_char):
        method_declaration = ''
        ls = '\r\n'
        input_variable_list = ''
        try:
            for index , element in enumerate(method_input_variables):
                variable_name = ''
                data_type = ''
                if not element['variable-name'] is None and element['variable-name'] != '':
                    variable_name = element['variable-name'] 
                if not element['data-type'] is None  and element['data-type'] != '':
                    data_type = element['data-type']
                input_variable_list += ' {0} {1} '.format(data_type , variable_name)
                if index < len(method_input_variables) -1:
                    input_variable_list += ','
                method_declaration = '{0} {1} {2} ( {3} ) ;{4}'.format(tab_char , return_type , method_name , input_variable_list , ls)
        except Exception , error:
            self.logger.error( '*********** DaoClassGenerator._method_declaration: Error occurred - {0}'.format(str(error)))
        return method_declaration
    
    def assemble_components(self , global_namespace , className , comment , method_list):
        assembled_components = ''
        ls = '\r\n'
        tab_char = '\t'
        assembled_components += self._import_block(global_namespace) + ls
        assembled_components += self._package_declaration(global_namespace)
        assembled_components += '{'+ ls
        assembled_components += self._interface_comment_block(comment , tab_char) + ls
        assembled_components += self._interface_definition_block(className , tab_char) + '{' + ls
        for element in method_list:
            assembled_components += self._method_declaration(element.methodName , element.returnType , element.inputVariables , (tab_char * 2))
        assembled_components += tab_char + '}' + ls
        assembled_components += '}' + ls
        return assembled_components
    
    def generateInterfaceFiles(self):
        config = ConfigJsonParser(self._configFilePath, self.logger)
        parser = DaoObjectJsonParser(config.configFilePath(), self.logger)
        daoList = parser.listOfDaos()
        for element in daoList:
            directory = config.deploymentDirectory(JsonConstants.DEPLOYDAO)
            fileName = element.name + '.java'
            dao_file_obj = open(directory + fileName , 'w+')
            dao_file_obj.flush()
            dao_file_obj.write(self.assemble_components(config.globalClassNameSpace(), element.name, element.comment, element.methodList))
            dao_file_obj.close()
    