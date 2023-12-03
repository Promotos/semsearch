# SemSearch
An application to [semantic search]([https://](https://en.wikipedia.org/wiki/Semantic_search)) your local documents.
You can search by meaning your local documents using a local large language model (example llama2) which produce no additional costs.
The embedding index is stored as local files using chroma.


The application is based on
* [chroma](https://github.com/chroma-core/chroma)
* [fastapi](https://github.com/tiangolo/fastapi)
* [langchain](https://github.com/langchain-ai/langchain)
* [django](https://github.com/django/django)

## Requirements & Installation
* Required is a python 3.x installation.

To install the python dependencies execute
```
pip install -r requirements.txt
```

## Execute the application
To execute the application run
```
streamlit run semsearch.py
```