# CorpusGenerator

This project is a culmination of different ideas I've had over the years, namely fusing my interest in NLP techniques and libraries and my linguistics background. When MIT's [SciGen](https://pdos.csail.mit.edu/archive/scigen/) project came into being, I became really intrigued by the prospect of generating text from a series of context free grammars (CFGs). Since the NLTK library available in the Python stack is very comprehensive, I chose to use a bulk of it for my purposes.

What intrigued me even more than just the usage of CFGs to generate text, was the prospect of using Hidden Markov models to randomly select text from a training corpus and generating "novel" (read: unique) sentences. Thus, this project came into being.

The intent is to create a corpus of novel text based upon running training samples through the various 'engines' available:

| Engine | Description | Comments |
|--------|-------------|----------|
| `direct`| Directly access text from the file-system | *Not fully tested* |
| `hiddenmarkovmodel` | Uses the NLTK's HiddenMarkovModelTrainer object to sample text | Requires NLTK to be fully installed |
| `simplifiedmarkovchain` | A simplified Markov implementation to randomly select text | *Not fully tested* |
| `cfg`  | Generate novel text from a context free grammar | *Requires NLTK to be installed; this functionality has also not been fully tested*|


I've been heavily involved in a lot of Apache Lucene-based search engine work in the past and thought Elasticsearch would be a great search store to index these novel sentence-based corpora through.
