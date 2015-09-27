#!/usr/bin/env python
import os
import yaml
from model.ViewModel import ViewModel
from parser.ConfigYamlParser import ConfigYamlParser
from parser.YamlConstants import YamlConstants

class ViewYamlParser:
    
    def __init__(self , pathToConfigFile = '' , logger=None):
        self._pathToConfigFile = pathToConfigFile
        self.logger = logger
    def listOfViews(self):
        view_list = []
        config = ConfigYamlParser(self._pathToConfigFile , self.logger)
        try:
            view_model_yaml_file_path = config.yamlModelFilePath(YamlConstants.YAMLVIEW)
            view_model_yaml_file = open(view_model_yaml_file_path , 'rb')
            view_model_yaml_ingest = view_model_yaml_file.read()
            view_model_yaml_file.close()
            for view_yaml_parser in yaml.load_all(view_model_yaml_ingest):
                viewModel = ViewModel()
                viewModel.name = view_yaml_parser['name']
                viewModel.selectClause = view_yaml_parser['select-clause']
                viewModel.fromClause = view_yaml_parser['from-clause']
                viewModel.whereClause = view_yaml_parser['where-clause']
                view_list.append(viewModel)
        except IOError, ioerr:
            self.logger.error( '***** ViewYamlParser.listOfViews: IO Error occured - {0}'.format(str(ioerr)))
        return view_list

