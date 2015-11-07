import os
from util.constant import JsonConstants
from model.table import TableModel
from model.tablefield import TableFieldModel
from jinja2 import Environment , FileSystemLoader

class DeleteDataScriptGenerator(object):
    '''
    This class is charged with generating a SQL script that contains DELETE statements against the associated schema.
    '''
    
    def __init__(self , configFileObj = None , deploymentUtil=None , logger=None):
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
        
    def listOfTables(self):
        '''
        This method converts the JSON dictionary of SQL TABLE properties into a list of model.TableModel objects.
        
        @return: list
        '''
        table_model_list = []
        try:
            for tableObj in self.__configFileObj.sqlTables():
                    tablemodel = TableModel()
                    tablemodel.tableName = tableObj['name']
                    table_model_list.append(tablemodel)
        except IOError, ioerr:
            self.__logger.error( '***** DeleteDataScriptGenerator.listOfTables: IO Error occured - {0}'.format(str(ioerr)))
        except Exception, err:
            self.__logger.error( '***** DeleteDataScriptGenerator.listOfTables: Error occured - {0}'.format(str(err)))
        return table_model_list
    
    def listOfTableField(self , method_list):
        '''
        This method further decomposes the table fields into a list of model.TableFieldModel objects
        
        @param method_list: This is the list of fields from the model.TableModel.fieldsArray object
        @type method_list: list
        @return: list
        '''
        tableMethodList = []
        for element in method_list:
            field = TableFieldModel()
            field.fieldName = element['field-name']
            field.dataType = element['data-type']
            field.length = element['length']
            field.isPrimaryKey = element['is-primary-key']
            field.autoIncrement = element['auto-increment']
            field.isForeignKeyConstraint = element['is-foreign-key-constraint']
            field.foreignKeyName = element['foreign-key-name']
            field.foreignKeyTable = element['foreign-key-table']
            tableMethodList.append(field)
        return tableMethodList
        
    def createSqlFile(self):
        '''
        This method loads the template from the util.ConfigurationProperties object and creates a 'DELETE' SQL script.
        '''
        tableList = []
        try:
            sql_deployment_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYSQL)
            self.__deploymentUtil.createDeploymentDirectory(sql_deployment_directory)
            template_sql_file_name = self.__configFileObj.deleteAllDataFromTablesAndViewsScriptFileName()
            template_directory = os.path.abspath(self.__configFileObj.templateDirectoryName())
            sql_file_path = sql_deployment_directory +  template_sql_file_name
            tableList = self.listOfTables()
            if len(tableList) > 0:
                env = Environment(loader=FileSystemLoader(template_directory))
                template = env.get_template(self.__configFileObj.deleteAllDataFromTablesTemplateFileName())
                template.stream({'schemaName':self.__configFileObj.databaseSchemaName() , 
                                 'databaseName':self.__configFileObj.databaseName() , 
                                 'tableList':tableList}).dump(sql_file_path)  
        except IOError , ioerror:
            self.__logger.error( '***** DeleteDataScriptGenerator.createSqlFile: IOError occurred - {0}'.format(str(ioerror)))
        except Exception , error:
            self.__logger.error( '***** DeleteDataScriptGenerator.createSqlFile: Error occurred - {0}'.format(str(error)))