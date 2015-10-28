# Portfolio

***Preamble***

This GitHub repo consists of a series of code-bases which I have created to demonstrate the types of projects that I enjoy coding and developing. My current interests pertain to building advanced analytics utilizing unstructured text processing methodologies (e.g NLP, NER, amongst others).

While much of my professional expertise surrounds traditional web-application creation/building/maintenance/etc., there are many powerful tools in the Python and Java "universes" which align with my stated interests above.

The code in this repo is free to use, however I make no claims as its efficacy or whether it can be used within Production environments; it is merely for illustrative purposes and to provide context for how I would solve specific analysis problems. In other words, please feel free to use this code - but, do so at your own risk...

***Files in this Repository***

The first project in this repo is a Python 2.7-based project called 'DaoGenerator' which I created to generate SQL scripts and Java objects (utilizing Spring conventions) from a series of JSON files. This project represents my first foray into "polyglottal" code generation.

The second project is also a Python 2.7-based project called "CorpusGenerator" that uses the NLTK's HiddenMarkovModelTrainer object with a sample corpus from the NLTK's 'corpora' text-store to generate novel text. The functionality then indexes the resulting CSV file into Elasticsearch. There is additional functionality I am working on that uses NLTK's Chomsky-normalized CFG's and FCFG's to generate novel text as well. These additional features are currently a work in progress.

The third project is called '"AngularD3Voronoi". It is a "transformation" of the d3.js ["Voronoi" tesselation](https://github.com/mbostock/d3/wiki/Voronoi-Geom) into an AngularJS directive so that it can be ported into an AngularJS app. It was written in CoffeeScript and then `grunt` was used to compile it into POJS. The `Gruntfile.js` itself is written in CoffeeScript. `coffee-contrib-coffee` is required to compile these files. It does not have a mechanism to color the cells in the tesselation yet. This will be a future enhancement that either accepts a list of rgb() values or randomly generates colors "on the fly".

The fourth project is an RESTful topic extraction tool called "FlaskTopicSearch". It is oriented around REST-like endpoints facilitated by a small Python 2.7-based Flask app. It uses the gensim stack to perform 'JSON-ified' TF-IDF, LDA and LSI operations against a corpus of text and is currently designed to search Elasticsearch indexes. It is functional, provided Elasticsearch is online and an index has been created; ideally with the content generated from the "CorpusGenerator" project. However, it should generate topics against any Elasticsearch store (assuming the search signature API calls are correctly formed).

The fifth project is a Python 2.7 and Flask-based clustering tool that is based on the ["Lingo" clustering algorithm](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.9.5370&rep=rep1&type=pdf). It uses NLTK, Numpy and scikit-learn and ***is currently a work in progress***. The known gaps are: it does not yet calculate cosine similarities between candidate labels, identify label groups that exceed the label similarity threshold or create cluster label candidates. My tentative plan is to incorporate hypernym and meronym detection once the base functionality is completed. ***I have provided this for illustration purposes only***.
