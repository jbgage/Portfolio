# Portfolio

***Preamble***

This GitHub repo consists of a series of code-bases which I have created to demonstrate the types of projects that I enjoy coding and developing. My current interests pertain to building advanced analytics utilizing unstructured text processing methodologies (e.g NLP, NER, amongst others).

While much of my professional expertise surrounds traditional web-application creation/building/maintenance/etc., there are many powerful tools in the Python and Java "universes" which align with my stated interests above.

The code in this repo is free to use, however I make no claims as its efficacy or whether it can be used within Production environments; it is merely for illustrative purposes and to provide context for how I would solve specific analysis problems. In other words, please feel free to use this code - but, do so at your own risk...

***Files in this Repository***

The first project in this repo is a Python 2.7-based project called 'DaoGenerator' which I created to generate SQL scripts and Java objects (utilizing Spring conventions) from a series of JSON files. This project represents my first foray into "polyglottal" code generation.

The second project is also a Python 2.7-based project called "CorpusGenerator" that uses the NLTK's HiddenMarkovModelTrainer object with a sample corpus from the NLTK's 'corpora' text-store to generate novel text. The functionality then indexes the resulting CSV file into Elasticsearch. There is additional functionality I am working on that uses NLTK's Chomsky-normalized CFG's and FCFG's to generate novel text as well. These features are currently a work in progress.

The third project is a Java-based project that is called "SpringBootTopicSearch". This project uses Spring-Boot, Elasticsearch and Mallet's ML library to generate LDA-based topics against the Elasticsearch store that was populated via the "CorpusGenerator" project above. This is provided for illustrative purposes only. There are currently some Autowiring bugs that I am sorting out, but this project gives a good overview of how I would solve a topic extraction problem.
