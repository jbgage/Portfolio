#!/usr/bin/env python
class StoredProcedureModel(object):
 
    
    def __init__(self , name = '' , tableName = '' , viewName = '' , storedProcedureType = '' , inputVariables = [] , outputVariables = [] , selectStatementFields = [], insertStatementFields = [] , updateStatementFields = [] , whereClause = [] ):
        self._name = name
        self._tableName = tableName
        self._viewName = viewName
        self._storedProcedureType = storedProcedureType
        self._inputVariables = inputVariables
        self._outputVariables = outputVariables
        self._selectStatementFields = selectStatementFields
        self._insertStatementFields = insertStatementFields
        self._updateStatementFields = updateStatementFields
        self._whereClause = whereClause
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self , value):
        self._name = value
        
    @property
    def tableName(self):
        return self._tableName
    
    @tableName.setter
    def tableName(self , value):
        self._tableName = value
        
    @property
    def storedProcedureType(self):
        return self._storedProcedureType
    
    @storedProcedureType.setter
    def storedProcedureType(self , value):
        self._storedProcedureType = value
    
    @property
    def inputVariables(self):
        return self._inputVariables
    
    @inputVariables.setter
    def inputVariables(self , value):
        self._inputVariables = value
        
    @property
    def outputVariables(self):
        return self._outputVariables
    
    @outputVariables.setter
    def outputVariables(self , value):
        self._outputVariables = value
    
    @property
    def selectStatementFields(self):
        return self._selectStatementFields
    
    @selectStatementFields.setter
    def selectStatementFields(self , value):
        self._selectStatementFields = value
        
    @property
    def insertStatementFields(self):
        return self._insertStatementFields
    
    @insertStatementFields.setter
    def insertStatementFields(self , value):
        self._insertStatementFields = value
    
    @property
    def updateStatementFields(self):
        return self._updateStatementFields
    
    @updateStatementFields.setter
    def updateStatementFields(self , value):
        self._updateStatementFields = value
    
    @property
    def deleteStatementFields(self):
        return self._deleteStatementFields
    
    @property
    def whereClause(self):
        return self._whereClause
    
    @whereClause.setter
    def whereClause(self , value):
        self._whereClause = value
    
        
    
        
    
    
    
        
    
