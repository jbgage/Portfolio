#!/usr/bin/env python
class ProfileMethodModel(object):
    
    def __init__(self , method_name = '' , comment = '' , return_type = '' , daoReferenced = '' , input_variable_list = [] , daoMethodName = '' , dao_input_parameters = []):
        self._methodName = method_name
        self._comment = comment
        self._returnType = return_type
        self._daoReferenced = daoReferenced
        self._inputVariableList = input_variable_list
        self._daoMethodName = daoMethodName
        self._daoInputParameters = dao_input_parameters
    
    @property
    def methodName(self):
        return self._methodName
    
    @methodName.setter
    def methodName(self , value):
        self._methodName = value
    
    @property
    def comment(self):
        return self._comment
    
    @comment.setter
    def comment(self , value):
        self._comment = value
    
    @property
    def returnType(self):
        return self._returnType
    
    @returnType.setter
    def returnType(self , value):
        self._returnType = value 
    
    @property
    def daoReferenced(self):
        return self._daoReferenced
    
    @daoReferenced.setter
    def daoReferenced(self , value):
        self._daoReferenced = value
    
    @property
    def inputVariableList(self):
        return self._inputVariableList
    
    @inputVariableList.setter
    def inputVariableList(self , value):
        self._inputVariableList = value
    
    @property
    def daoMethodName(self):
        return self._daoMethodName
    
    @daoMethodName.setter
    def daoMethodName(self , value):
        self._daoMethodName = value
   
    @property
    def daoInputParameters(self):
        return self._daoInputParameters
   
    @daoInputParameters.setter
    def daoInputParameters(self , value):
        self._daoInputParameters = value