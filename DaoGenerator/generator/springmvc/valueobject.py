#!/usr/bin/env python
from parser.ConfigJsonParser import ConfigJsonParser
from parser.pattern.ValueObjectJsonParser import ValueObjectJsonParser
from parser.constants import JsonConstants
import os
import sys

class ValueObjectClassGenerator:
    
    __open_brace = "{"
    __close_brace = "}"
    __serializable_assertion = '[Serializable]'
    
    def __init__(self , pathToConfigFile = '' , logger=None):
        self._pathToConfigFile = pathToConfigFile
        self.logger = logger
    
    def _package_block(self):
        ls = '\r\n'
        config = ConfigJsonParser(self._pathToConfigFile)
        namespace_block = 'package {0}.model {1}'.format(config.globalClassNameSpace() , ls)
        return namespace_block
    
    def _interface_definition_block(self , valueObjectName):
        ls = '\r\n'
        class_def = 'public class {0}{1}'.format(valueObjectName , ls)
        return class_def
    
    def _method_definition_block(self , tab_char , field_array):
        method_definition = ''
        try:
            if not field_array is None:
                method_definition += self._generate_getters(tab_char, field_array)
                method_definition += self._generate_setters(tab_char, field_array)
        except Exception , err:
            self.logger.error( '****** ValueObjectClassGenerator._methodDefinitionBlock: Error occured - {0}'.format(str(err)))
        return method_definition
    
    def _generate_getters(self , tab_char , field_array):
        ls = '\r\n'
        method_definition = ''
        try:
            if not field_array is None:
                for element in field_array:
                    method_definition += 'public {0} get{1}{2}'.format(element['data-type'] , element['field-name'] , '{') + ls
                    method_definition += tab_char + 'return {0};'.format(element['field-name']) + ls
                    method_definition + '}'
        except Exception , err:
            self.logger.error( '****** ValueObjectClassGenerator._generate_getters: Error occured - {0}'.format(str(err))) 
        return method_definition
            
    def _generate_setters(self , tab_char , field_array):
        ls = '\r\n'
        method_definition = ''
        try:
            if not field_array is None:
                for element in field_array:
                    method_definition += 'public void set{1}({0} {1}){2}'.format(element['data-type'] , element['field-name'] , '{') + ls
                    method_definition += tab_char + 'this.{0} = {0};'.format(element['field-name']) + ls
                    method_definition + '}'
        except Exception , err:
            self.logger.error( '****** ValueObjectClassGenerator._generate_getters: Error occured - {0}'.format(str(err))) 
        return method_definition
            
    
    def __assemble_class_components(self , voName , fieldArr):
        ls = '\r\n'
        class_definition = ''
        class_definition += self._import_block()
        class_definition += ls
        class_definition += self.__namespace_block()
        class_definition += self.__open_brace + ls
        class_definition += '\t' + self.__serializable_assertion + ls
        class_definition += '\t' + self._class_definition_block(voName) + ls
        class_definition += '\t' + self.__open_brace + ls
        class_definition += self.__method_definition_block('\t\t' , fieldArr)
        class_definition += '\t' + self.__close_brace + ls
        class_definition += self.__close_brace + ls
        return class_definition
    
    def generateClassFiles(self):
        config = ConfigJsonParser(self._pathToConfigFile, self.logger)
        voParser = ValueObjectJsonParser(config.configFilePath(), self.logger)
        vo_list = []
        try:
            outputDirectory = config.deploymentDirectory(JsonConstants.DEPLOYMODEL)
            vo_list = voParser.listOfValueObjects()
            if not (vo_list is None):
                for element in vo_list:
                    classFile = open( '{0}{1}.java'.format(outputDirectory , element.modelName) , 'w+' )
                    classFile.write(self.__assemble_class_components(element.modelName , element.fieldsArray))
                    sys.stdout.flush()
                    os.fsync(classFile.fileno())
                    classFile.close()
        except IOError, ioerror:
            self.logger.error( '***** ValueObjectClassGenerator.generateInterfaceFiles: IOError occurred - {0}'.format(str(ioerror)))
        #except Exception, err:
        #    print '***** ValueObjectClassGenerator.generateClassFiles: Error occurred - {0}'.format(str(err))
        
    
    
        
        
        


