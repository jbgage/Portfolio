
class DaoMethodModel(object):
    


    def __init__(self , method_name = '' , return_type = '' , input_variables = []):
        self._methodName = method_name
        self._returnType = return_type
        self._inputVariables = input_variables
        
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
    def inputVariables(self):
        return self._inputVariables
    
    @inputVariables.setter
    def inputVariables(self , value):
        self._inputVariables = value
        