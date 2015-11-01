import os
from model.dao import DaoModel
from model.daomethod import DaoMethodModel
from parser.constant import JsonConstants
from parser.config import ConfigJsonParser
from parser.pattern.dao import DaoObjectJsonParser
class DaoClassGenerator(object):
    def __init__(self , configFileObj = None , deploymentUtil=None , logger=None):
        self.__configFileObj = configFileObj
        self.__deploymentUtil = deploymentUtil
        self.__logger = logger
    def __import_block(self , global_namespace , tab_char=''):
        ls = os.linesep
        import_block = ''
        import_block += tab_char + 'import java.util.List;' + ls
        import_block += tab_char + 'import {0}.model;'.format(global_namespace) + ls
        return import_block
    def __package_declaration(self , global_namespace):
        ls = os.linesep
        namespace_block = ''
        namespace_block += 'package {0}.persistence.dao;'.format(global_namespace ) + ls
        return namespace_block
    def __interface_definition_block(self , class_name , tab_char):
        ls = os.linesep
        interface_declaration = '{0}public interface {1} {2}'.format(tab_char , class_name , '{' ) + ls
        return interface_declaration
    def __interface_comment_block(self , class_comment , tab_char):
        class_comment_output = ''
        ls = os.linesep
        if not class_comment is None and class_comment != '':
            class_comment_output += tab_char + '/' + ('*' * (len(class_comment) + 1)) + ls
            class_comment_output += tab_char + '-  {0}'.format(class_comment ) + ls
            class_comment_output += tab_char + ('*' * (len(class_comment) + 1)) + '/' + ls
        return class_comment_output
    def __method_declaration(self , method_name , return_type ,  method_input_variables , tab_char):
        method_declaration = ''
        ls = os.linesep
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
            self.__logger.error( '*********** DaoClassGenerator._method_declaration: Error occurred - {0}'.format(str(error)))
        return method_declaration
    def assemble_components(self , global_namespace , className , comment , method_list):
        assembled_components = ''
        ls = os.linesep
        tab_char = '\t'
        assembled_components += self.__package_declaration(global_namespace)
        assembled_components += self.__import_block(global_namespace , tab_char='') + ls
        assembled_components += self.__interface_comment_block(comment , tab_char) + ls
        assembled_components += self.__interface_definition_block(className , tab_char='')
        for element in method_list:
            assembled_components += self.__method_declaration(element.methodName , element.returnType , element.inputVariables , (tab_char * 2))
        assembled_components += '}' + ls
        return assembled_components
    def generateInterfaceFiles(self):
        try:
            parser = DaoObjectJsonParser(self.__configFileObj ,  self.__logger)
            if parser is not None:
                daoList = parser.listOfDaos()
                for element in daoList:
                    directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYDAO)
                    self.__deploymentUtil.createDeploymentDirectory(directory)
                    fileName = element.name + '.java'
                    with open(directory + fileName , 'w+') as dao_file_obj:
                         dao_file_obj.write(self.assemble_components(self.__configFileObj.globalClassNameSpace(), element.name, element.comment, element.methodList))
            else:
                self.__logger.error("DaoClassGenerator.generateInterfaceFiles: error retrieving configuration file object.")
        except Exception , error:
            self.__logger.error( '*********** DaoClassGenerator.generateInterfaceFiles: Error occurred - {0}'.format(str(error)))