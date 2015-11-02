#!/usr/bin/env python
class DaoImplMethodModel(object):
    
    def __init__(self, method_name = '' , comment = '' , return_type = '' , value_object_type = '' , method_input_variables = [] , stored_procedure_name = '' , sql_command_object_input_variables = [] , result_set_parameters= []):
        self._methodName = method_name
        self._comment = comment
        self._returnType = return_type
        self._value_object_type = value_object_type
        self._methodInputVariables = method_input_variables
        self._storedProcedureName = stored_procedure_name
        self._sql_command_object_input_variables = sql_command_object_input_variables
        self._result_set_parameters = result_set_parameters
    
    @property
    def methodName(self):
        return self._methodName
    
    @methodName.setter
    def methodName(self , value):
        self._methodName = value
    
    @property
    def returnType(self):
        return self._returnType
   
    @returnType.setter
    def returnType(self , value):
        self._returnType = value
    
    @property
    def valueObjectType(self):
        return self._value_object_type
    
    @valueObjectType.setter
    def valueObjectType(self , value):
        self._value_object_type = value
    
    @property 
    def comment(self):
        return self._comment
    @comment.setter
    def comment(self , value):
        self._comment = value
    @property
    def methodInputVariables(self):
        return self._methodInputVariables
    
    @methodInputVariables.setter
    def methodInputVariables(self , value):
        self._methodInputVariables = value
    
    @property
    def storedProcedureName(self):
        return self._storedProcedureName
   
    @storedProcedureName.setter
    def storedProcedureName(self , value):
        self._storedProcedureName = value
    
    @property
    def sqlCommandObjectInputVariables(self):
        return self._sql_command_object_input_variables
    
    @sqlCommandObjectInputVariables.setter
    def sqlCommandObjectInputVariables(self , value):
        self._sql_command_object_input_variables = value
    
    @property
    def resultSetParameters(self):
        return self._result_set_parameters
    
    @resultSetParameters.setter
    def resultSetParameters(self , value):
        self._result_set_parameters = value