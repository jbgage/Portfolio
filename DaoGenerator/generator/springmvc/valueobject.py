#!/usr/bin/env python
import os
from parser.pattern.valueobject import ValueObjectJsonParser
from parser.constant import JsonConstants

class ValueObjectClassGenerator(object):
    '''
    This class is charged to generate the ValueObject class files based upon the corresponding GOF design patter
    '''
    
    __open_brace = "{"
    __close_brace = "}"
    
    def __init__(self , configFileObject = None , deploymentUtil=None , logger=None):
        '''
        Constructor
        
        @param configFileObj: The parser.config.ConfigJsonParser object passed to this class
        @type configFileObj: parser.config.ConfigJsonParser
        @param deploymentUtil: The deploy.DeploymentUtil object passed to the Generator
        @type deploymentUtil:deploy.DeploymentUtil
        @param logger: The logger object
        @type logger: logger
        '''
        self.__configFileObj = configFileObject
        self.__deploymentUtil = deploymentUtil
        self.__logger = logger
        
    def __import_block(self , tab_char='\t'):
        ls = os.linesep
        import_block = tab_char + 'import java.util.Serializable;' + ls
        return import_block
    
    def __package_block(self):
        ls = os.linesep
        namespace_block = 'package {0}.model; {1}'.format(self.__configFileObj.globalClassNameSpace() , ls)
        return namespace_block
    
    def __class_definition_block(self , valueObjectName):
        ls = os.linesep
        class_def = 'public class {0} implements Serializable'.format(valueObjectName)
        return class_def
    
    def __instance_variables_block(self , tab_char , field_array):
        instance_variables = ''
        ls = os.linesep
        if field_array is not None:
            for element in field_array:
                instance_variables += tab_char + 'private {0} {1};'.format(element['data-type'] , element['field-name']) + ls
        return instance_variables
    
    def __constructor(self , valueObjectName):
        return 'public {0}() '.format(valueObjectName)     
       
    def __method_definition_block(self , tab_char , field_array):
        method_definition = ''
        try:
            if not field_array is None:
                method_definition += self.__generate_getters(tab_char, field_array)
                method_definition += self.__generate_setters(tab_char, field_array)
        except Exception , err:
            self.__logger.error( '****** ValueObjectClassGenerator._methodDefinitionBlock: Error occured - {0}'.format(str(err)))
        return method_definition
    
    def __generate_getters(self , tab_char , field_array):
        ls = os.linesep
        method_definition = ''
        try:
            if not field_array is None:
                for element in field_array:
                    method_definition += tab_char + 'public {0} get{1}(){2}'.format(element['data-type'] , element['field-name'] , self.__open_brace) + ls
                    method_definition += tab_char + tab_char + 'return {0};'.format(element['field-name']) + ls
                    method_definition += tab_char + self.__close_brace + ls
        except Exception , err:
            self.__logger.error( '****** ValueObjectClassGenerator._generate_getters: Error occured - {0}'.format(str(err))) 
        return method_definition
    
    def __generate_setters(self , tab_char , field_array):
        ls = os.linesep
        method_definition = ''
        try:
            if not field_array is None:
                for element in field_array:
                    method_definition += tab_char + 'public void set{1}({0} {1}){2}'.format(element['data-type'] , element['field-name'] , self.__open_brace) + ls
                    method_definition += tab_char + tab_char + 'this.{0} = {0};'.format(element['field-name']) + ls
                    method_definition += tab_char + self.__close_brace + ls
        except Exception , err:
            self.__logger.error( '****** ValueObjectClassGenerator._generate_getters: Error occured - {0}'.format(str(err))) 
        return method_definition
    
    def __assemble_class_components(self , voName , fieldArr):
        ls = os.linesep
        class_definition = ''
        class_definition += self.__package_block() + ls
        class_definition += self.__import_block(tab_char='') + ls
        class_definition += self.__class_definition_block(voName) + ls
        class_definition += self.__open_brace + ls
        class_definition += self.__instance_variables_block( '\t\t' , fieldArr)
        class_definition += '\t\t' + self.__constructor(voName) + self.__open_brace + ls
        class_definition += '\t\t' + self.__close_brace + ls
        class_definition += self.__method_definition_block('\t\t' , fieldArr)
        class_definition += self.__close_brace + ls
        return class_definition
    
    def generateClassFiles(self):
        voParser = ValueObjectJsonParser(self.__configFileObj, self.__logger)
        vo_list = []
        try:
            outputDirectory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYMODEL)
            self.__deploymentUtil.createDeploymentDirectory(outputDirectory)
            vo_list = voParser.listOfValueObjects()
            if not (vo_list is None):
                for element in vo_list:
                    with open( '{0}{1}.java'.format(outputDirectory , element.modelName) , 'w+' ) as classFile:
                        classFile.write(self.__assemble_class_components(element.modelName , element.fieldsArray))
        except IOError, ioerror:
            self.__logger.error( '***** ValueObjectClassGenerator.generateInterfaceFiles: IOError occurred - {0}'.format(str(ioerror)))        