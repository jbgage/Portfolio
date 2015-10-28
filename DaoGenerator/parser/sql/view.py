#!/usr/bin/env python
import os
import json
from model.ViewModel import ViewModel
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants

class ViewJsonParser:
    
    def __init__(self , pathToConfigFile = '' , logger=None):
        self._pathToConfigFile = pathToConfigFile
        self.logger = logger
    def listOfViews(self):
        view_list = []
        config = ConfigJsonParser(self._pathToConfigFile , self.logger)
        try:
            view_model_json_file_path = config.jsonModelFilePath(JsonConstants.YAMLVIEW)
            view_model_json_file = open(view_model_json_file_path , 'rb')
            view_model_json_ingest = view_model_json_file.read()
            view_model_json_file.close()
            for view_json_parser in json.load_all(view_model_json_ingest):
                viewModel = ViewModel()
                viewModel.name = view_json_parser['name']
                viewModel.selectClause = view_json_parser['select-clause']
                viewModel.fromClause = view_json_parser['from-clause']
                viewModel.whereClause = view_json_parser['where-clause']
                view_list.append(viewModel)
        except IOError, ioerr:
            self.logger.error( '***** ViewJsonParser.listOfViews: IO Error occured - {0}'.format(str(ioerr)))
        return view_list

