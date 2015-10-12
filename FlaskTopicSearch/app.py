from flask import Flask
from flask_restful import Api 
from search import Search
from topics import TopicAnalyzer
from property import PropertyUtil
import os.path
import logging
from logging.config import fileConfig
app = Flask(__name__)
api = Api(app)

@app.route('/topics/tfidf/<term>' , methods=['GET'])
def get_tfidf(term):
    fileConfig('config/logging.conf')
    prop = PropertyUtil('config/application.conf')
    logger = logging.getLogger(__name__)
    topics = None
    json_data = {}
    try:
        logger.info('Term = {0}'.format(term))
        if prop is not None:
            logger.info('Index Name = {0}'.format(prop.elasticSearchIndexName))
            search = Search(prop , logger )
            if term != '':
                logger.info( 'search is null' + str(search == None))
                data = search.get(term)
                logger.info('Main.get_tfidf: data size = {0}'.format(len(data)))
                topics = TopicAnalyzer(data , logger)
                json_data = topics.getTfIdf()
    except Exception , error:
        logger.error('Exception occurred - {0}'.format(str(error)))
    return json_data




if __name__ == '__main__':
    app.run()