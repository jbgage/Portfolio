from parser.ConfigYamlParser import ConfigYamlParser
from parser.pattern.DaoImplObjectYamlParser import DaoImplObjectYamlParser
from parser.YamlConstants import YamlConstants

class DaoImplClassGenerator:
    def __init__(self , configFilePath = '' , logger=None):
        self._configFilePath = configFilePath
        self.logger = logger
       
    def _import_block(self , global_namespace='' , model_name='' , mapper_name='' , dao_name=''):
        ls = '\r\n'
        import_block = ''
        import_block += 'import java.util.List;' + ls
        import_block += 'import java util.LinkedList;' + ls
        import_block += 'import java.util.HashMap;' + ls
        import_block += 'import javax.annotation.Resource;' + ls
        import_block += 'import org.apache.tomcat.jdbc.pool.DataSource;' + ls
        import_block += 'import org.springframework.beans.factory.annotation.Autowired;' + ls
        import_block += 'import org.springframework.jdbc.core.JdbcTemplate;' + ls
        import_block += 'import org.springframework.jdbc.core.simple.SimpleJdbcCall;' + ls
        import_block += 'import org.springframework.jdbc.core.BeanPropertyRowMapper;' + ls
        import_block += 'import org.slf4j.Logger;' + ls
        import_block += 'import org.slf4j.LoggerFactory;' + ls
        import_block += 'import {0}.model.{1};{2}'.format(global_namespace , model_name , ls)
        import_block += 'import {0}.persistence.dao.{1}; {2}'.format(global_namespace , dao_name , ls)
        return import_block
    
    def _package_declaration(self , global_namespace):
        ls = '\r\n'
        namespace_block = ''
        namespace_block += 'package {0}.persistence.dao.daoImpl{1}'.format(global_namespace , ls)
        return namespace_block
    
    def _class_definition_block(self , class_name , dao_impl_name , tab_char):
        ls = '\r\n'
        class_declaration = '{0}public class {1} : {2} {3}'.format(tab_char , class_name , dao_impl_name , ls)
        return class_declaration
    
    def _class_comment_block(self , class_comment , tab_char):
        class_comment_output = ''
        ls = '\r\n'
        if not class_comment is None and class_comment != '':
            class_comment_output += tab_char + '/' + ('*' * (len(class_comment) + 1)) + ls
            class_comment_output += tab_char + '-  {0}{1}'.format(class_comment , ls)
            class_comment_output += tab_char + ('*' * (len(class_comment) + 1)) + '/' + ls
        return class_comment_output
    
    def __method_comment_block(self , method_comment , tab_char):
        method_comment_output = ''
        ls = '\r\n'
        if not method_comment is None and method_comment != '':
            method_comment_output += tab_char + '/' + ('*' * (len(method_comment) + 1)) + ls
            method_comment_output += tab_char + '-  {0}{1}'.format(method_comment , ls)
            method_comment_output += tab_char + ('*' * (len(method_comment) + 1)) + '/' + ls
        return method_comment_output
    
    def _method_declaration(self , method_name , return_type , value_object_type, method_input_variables , tab_char):
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
                if not return_type is None and return_type != '':
                    if return_type == 'list':
                        if not value_object_type is None and value_object_type != '':
                            method_declaration = '{0}public List<{1}>  {2} ( {3} ) {4}'.format(tab_char , value_object_type , method_name , input_variable_list , ls)
                        else:
                            method_declaration = '{0}public List  {1} ( {2} ) {3}'.format(tab_char ,  method_name , input_variable_list , ls)
                    elif return_type == 'vo':
                        if not value_object_type is None  and value_object_type != '':
                            method_declaration = '{0}public {1} {2} ( {3} ) {4}'.format(tab_char , value_object_type , method_name , input_variable_list , ls)
                    else:
                        method_declaration = '{0}public {1} {2} ( {3} ) {4}'.format(tab_char , return_type , method_name , input_variable_list , ls)
        except Exception , error:
            self.logger.error( '*********** DaoImplClassGenerator._method_declaration: Error occurred - {0}'.format(str(error)))
        return method_declaration
    
    def _generate_constructor(self , class_name , tab_char):
        constructor = ''
        ls = '\r\n'
        constructor += '{0}public {1} ()'.format(tab_char , class_name) + ls
        constructor += '{0}{{'.format(tab_char) + ls
        constructor += '{0}}}'.format(tab_char) + ls
        constructor += ls
        return constructor
    
    def _generate_autowired_block(self):
        ls = '\r\n'
        block = ''
        block += '@Autowired'+ls
        block += '@Resource(name="jdbcTemplate")' + ls
        block += 'private JdbcTemplate jdbcTemplate;' + ls
        block += ls
        block += '@Autowired' + ls
        block += '@Resource(name="dataSource")' + ls
        block += 'private DataSource dataSource;'         
        return block;
    
    def _generate_logger_block(self , class_name=''):
        ls = '\r\n'
        block = 'private Logger logger = LoggerFactory.getLogger({0}.class.getName())'.format(class_name) + ls
        return block
    
    def __method_construction(self , class_name , method_name , value_object_type , return_type , stored_procedure_name , sql_command_input_variables , result_set_parameters  , tab_char):
        method_construct = ''
        ls = '\r\n'
        try:
            if not return_type is None  and return_type != '':
                if return_type == 'list':
                    method_construct += tab_char + 'List<{0}> list = null;'.format(value_object_type) + ls
                elif return_type == 'int':
                    method_construct += tab_char + 'int returnId = 0;' + ls
                elif return_type == 'vo':
                    method_construct += tab_char + '{0} vo = new {0}();'.format(value_object_type) + ls
            method_construct += tab_char + 'try' + ls
            method_construct += tab_char + '{' + ls
            if not sql_command_input_variables is None and len(sql_command_input_variables) > 0:
                method_construct += self.__construct_sql_command_section(value_object_type , return_type , stored_procedure_name, sql_command_input_variables, result_set_parameters  , tab_char)
            method_construct += tab_char + '}' + ls    
            method_construct += tab_char + 'catch (Exception ex)' + ls
            method_construct += tab_char + '{' + ls
            method_construct += tab_char + tab_char + 'logger.error("****** ' + class_name + '.' + method_name + ': Error occurred - {0}", ex.Message());' + ls
            method_construct += tab_char + '}' + ls 
            if not return_type is None  and return_type != '':
                if return_type == 'list':
                    method_construct += tab_char + 'return list;' + ls
                elif return_type == 'int':
                    method_construct += tab_char + 'return returnId;' + ls
                elif return_type == 'vo':
                    method_construct += tab_char + 'return vo;' + ls
        except Exception , error:
            self.logger.error( '************* DaoImplClassGenerator.__methodConstruction: Error occurred - {0}'.format(str(error)))
        return method_construct
    
    def __construct_sql_command_section(self , value_object_type , stored_procedure_name  , return_type , tab_char):
        sql_command_construct = ''
        ls = '\r\n'
        try:
            if  return_type == 'list' :
                if not value_object_type is None and value_object_type != '':
                    sql_command_construct += tab_char + tab_char + tab_char + 'list = new List<{0}>();'.format(value_object_type) + ls
            sql_command_construct += 'SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)' + ls
            sql_command_construct += tab_char + '.withProcedureName({0})'.format(stored_procedure_name) + ls
            sql_command_construct += tab_char + '.returningResultSet("{0}" , BeanPropertyRowMapper.newInstance({0}.class));'.format(value_object_type) + ls 
            sql_command_construct += tab_char + 'Map m = jdbcCall.execute(new HashMap<String , Object>(0));' + ls
            sql_command_construct += tab_char + 'list = (List) m.get("{0}");'.format(value_object_type) + ls 
        except Exception , error:
            self.logger.error( '************* DaoImplClassGenerator.__construct_sql_command_section: Error occurred - {0}'.format(str(error)))
        return sql_command_construct
        
    def _assemble_components(self , global_namespace , className , class_comment , daoName , method_list):
        assembled_components = ''
        ls = '\r\n'
        tab_char = '\t'
        assembled_components += self._import_block(global_namespace) + ls
        assembled_components += self._package_declaration(global_namespace)
        assembled_components += '{'+ ls
        assembled_components += self._class_comment_block(class_comment , tab_char) + ls
        assembled_components += self._class_definition_block(className , daoName , tab_char)
        assembled_components += tab_char + '{'+ ls
        assembled_components += self._generate_constructor(className , (tab_char * 2))
        for element in method_list:
            assembled_components += self.__method_comment_block(element.comment , (tab_char * 2))
            assembled_components += self._method_declaration(element.methodName ,  element.returnType , element.valueObjectType, element.methodInputVariables , (tab_char * 2))
            assembled_components += (tab_char * 2) + '{'+ ls
            assembled_components += self.__method_construction(className, element.methodName, element.valueObjectType, element.returnType, element.storedProcedureName, element.sqlCommandObjectInputVariables, element.resultSetParameters, (tab_char * 3))
            assembled_components += (tab_char * 2) +'}' + ls
            assembled_components += ls
        assembled_components += tab_char + '}' + ls
        assembled_components += '}' + ls
        
        return assembled_components
    
    
    def generateClassFiles(self):
        config = ConfigYamlParser(self._configFilePath, self.logger)
        daoImplParser = DaoImplObjectYamlParser(config.configFilePath(), self.logger)
        daoImplList = daoImplParser.listOfDaoImpls()
        for element in daoImplList:
            output_dir = config.deploymentDirectory(YamlConstants.DEPLOYDAOIMPL)
            fileName = element.name + '.java'
            daoImplFile = open(output_dir + fileName , 'w+')
            daoImplFile.flush()
            daoImplFile.write(self.assemble_components(config.globalClassNameSpace(), element.name, element.comment, element.daoImplemented, element.methodList))
            daoImplFile.close()