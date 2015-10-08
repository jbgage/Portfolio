import os
class DeploymentUtil(object):
    def __init__(self ,  logger=None):
        self.logger = logger
        
    def createDeploymentDirectory(self , directoryName=''):
        try:
            if directoryName.count('/') > 0:
                if not os.path.isdir(os.path.abspath(directoryName)):
                    os.makedirs(os.path.abspath(directoryName))
        except IOError , ioerror:
            self.logger.error( '***** DeploymentUtil.createDeploymentDirectory: IOError occurred - {0}'.format(str(ioerror)))
        except Exception , error:
            self.logger.error( '***** DeploymentUtil.createDeploymentDirectory: Error occurred - {0}'.format(str(error)))