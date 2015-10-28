from flask import Flask
from flask_restful import Api 
from search import Search
from lingo import LingoClustering
from property import PropertyUtil
import logging
import json
from logging.config import fileConfig
app = Flask(__name__)
api = Api(app)

@app.route('/lingo/<string:term>' , methods=['GET'])
def get_tfidf(term):
    fileConfig('config/logging.conf')
    prop = PropertyUtil('config/application.conf')
    logger = logging.getLogger(__name__)
    json_data = {}
    try:
        logger.info('Term = {0}'.format(term))
        if prop is not None:
            logger.info('Index Name = {0}'.format(prop.elasticSearchIndexName))
            search = Search(prop , logger )
            if term != '':
                data = search.get(term)
                if data is not None and len(data) > 0:
                    lingo = LingoClustering(data)
                    json_data = json.dumps(lingo.cluster_label_induction())
    except Exception , error:
        logger.error('Exception occurred - {0}'.format(str(error)))
    return json_data



if __name__ == '__main__':
    app.run()