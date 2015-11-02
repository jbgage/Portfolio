#!/usr/bin/env python
class ProfileModel(object):
    
    def __init__(self , name = '' , comment = '' , method_list = []):
        self._name = name
        self._comment = comment
        self._methodList = method_list
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self , value):
        self._name = value
    
    @property
    def comment(self):
        return self._comment
    
    @comment.setter
    def comment(self , value):
        self._comment = value
   
    @property
    def methodList(self):
        return self._methodList
    
    @methodList.setter
    def methodList(self , value):
        self._methodList = value