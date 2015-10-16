from flask import Flask
from flask_restful import Api 
from search import Search
from topics import TopicAnalyzer
from property import PropertyUtil
import os.path
import logging
import json
from logging.config import fileConfig
app = Flask(__name__)
api = Api(app)

@app.route('/topics/tfidf/<string:term>' , methods=['GET'])
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
                data = search.get(term)
                if data is not None and len(data) > 0:
                    topics = TopicAnalyzer(data , logger)
                    json_data = topics.get_tfidf_as_json()
    except Exception , error:
        logger.error('Exception occurred - {0}'.format(str(error)))
    return json_data


@app.route('/topics/lsi/<string:term>' , methods=['GET'])
def get_lsi(term):
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
                data = search.get(term)
                if data is not None and len(data) > 0:
                    topics = TopicAnalyzer(data , logger)
                    json_data = topics.get_lsi()
    except Exception , error:
        logger.error('Exception occurred - {0}'.format(str(error)))
    return json_data

@app.route('/topics/lda/<string:term>' , methods=['GET'])
def get_lda(term):
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
                data = search.get(term)
                if data is not None and len(data) > 0:
                    topics = TopicAnalyzer(data , logger)
                    json_data = topics.get_lda()
    except Exception , error:
        logger.error('Exception occurred - {0}'.format(str(error)))
    return json_data

@app.route('/topics/search/<string:term>' , methods=['GET'])
def search(term=''):
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
                data = search.get(term)
                json_data = json.dumps(data)
    except Exception , error:
        logger.error('Exception occurred - {0}'.format(str(error)))
    return json_data

if __name__ == '__main__':
    app.run()