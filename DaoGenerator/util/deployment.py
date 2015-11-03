#!/usr/bin/env python
import os

class DeploymentUtil(object):
    '''
    This is a utility class used to create the underlying deployment directories on the system for the generators
    to write their respective files to.
    '''
    
    def __init__(self ,  logger=None):
        self.__logger = logger
        
    def createDeploymentDirectory(self , directoryName=''):
        try:
            if directoryName.count('/') > 0:
                if not os.path.isdir(os.path.abspath(directoryName)):
                    os.makedirs(os.path.abspath(directoryName))
        except IOError , ioerror:
            self.__logger.error( '***** DeploymentUtil.createDeploymentDirectory: IOError occurred - {0}'.format(str(ioerror)))
        except Exception , error:
            self.__logger.error( '***** DeploymentUtil.createDeploymentDirectory: Error occurred - {0}'.format(str(error)))