import streamlit as st
from os import environ
from chromadb import Collection, PersistentClient
from chromadb.utils import embedding_functions

#sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def get_env(name:str) -> str:
    val = environ.get(name)
    if not val:
        raise ValueError(f"Environment variable '{name}' not set.")
    return val

DB_PATH = get_env('SEMSEARCH_DB')

client = PersistentClient(path=DB_PATH)
file_collection = client.get_or_create_collection(name="files")

query = st.text_input(f"Query on {file_collection.count()} elements")

if query:
    with st.spinner("Processing"):
        result = file_collection.query(query_texts=query)
        ids = result['ids'][0]
        meta = result['metadatas'][0]
        docs = result['documents'][0]
        count = len(ids)
        st.text (f"Found {count} results")
        for i in range(0,count):
            st.subheader(meta[i]['file'])
            st.markdown(docs[i])
    
