#!/usr/bin/env python
class ViewModel(object):
    
    def __init__(self , name = '' , selectClause = [] , fromClause = [], whereClause = []):
        self._name = name
        self._selectClause = selectClause
        self._fromClause = fromClause
        self._whereClause = whereClause
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self , value):
        self._name = value
    
    @property
    def selectClause(self):
        return self._selectClause
    
    @selectClause.setter
    def selectClause(self , value):
        self._selectClause = value
    
    @property
    def fromClause(self):
        return self._fromClause
    
    @fromClause.setter
    def fromClause(self , value):
        self._fromClause = value
    
    @property
    def whereClause(self):
        return self._whereClause
    
    @whereClause.setter
    def whereClause(self , value):
        self._whereClause = value