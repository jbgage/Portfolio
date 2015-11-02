#!/usr/bin/env python
from model.view import ViewModel
from parser.config import ConfigJsonParser
from parser.constant import JsonConstants
class ViewJsonParser:
    
    def __init__(self , configFileObj = None , logger=None):
        self.__configFileObj = configFileObj
        self.__logger = logger
    
    def listOfViews(self):
        view_list = []
        try:
            for viewObj in self.__configFileObj.sqlViews():
                viewModel = ViewModel()
                viewModel.name = viewObj['name']
                viewModel.selectClause = viewObj['select-clause']
                viewModel.fromClause = viewObj['from-clause']
                viewModel.whereClause = viewObj['where-clause']
                view_list.append(viewModel)
        except IOError, ioerr:
            self.__logger.error( '***** ViewJsonParser.listOfViews: IO Error occured - {0}'.format(str(ioerr)))
        return view_list