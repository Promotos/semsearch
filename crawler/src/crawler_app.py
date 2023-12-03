from pathlib import Path
from os import environ
import hashlib
from chromadb import Collection, PersistentClient
from chromadb.utils import embedding_functions
from pypdf import PdfReader

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

def get_env(name:str) -> str:
    val = environ.get(name)
    if not val:
        raise ValueError(f"Environment variable '{name}' not set.")
    return val

INDEX_ROOT = get_env('SEMSEARCH_INDEX_ROOT')
DB_PATH = get_env('SEMSEARCH_DB')

def filehash(file:str) -> str:
    with open(file, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def get_files_to_index(root:str) -> [str]:
    result = []
    for path in Path(root).rglob('*'):
        if path.suffix.lower() == ".pdf":
            result.append(path)
    return result

def index_file(file_col:Collection, file:str, hash:str):
    print(f"Index file {file} ... ", end="")
    try:
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if len(text) < 10: # avoid too small content
                continue
            file_col.add(
                documents=[text],
                metadatas=[{'hash': hash, 'file': str(file)}],
                ids=[f"{hash}-{page.page_number}"]
            )
        print("ok")
    except:
        print("error")

def index_missing(file_col:Collection, files:[str]):
    for file in files:
        hash = filehash(file)
        res = file_col.get(where={'hash': {'$eq': hash}})
        if len(res['ids']) == 0:
            index_file(file_col, file=file, hash=hash)

print(f"Load database from '{DB_PATH}' ... ", end="")
client = PersistentClient(path=DB_PATH)
print("ok")

print(f"List files to index in {INDEX_ROOT} ... ", end="")
files = get_files_to_index(INDEX_ROOT)
print(f"found {len(files)} files")

file_collection = client.get_or_create_collection(name="files")
print(f"{file_collection.count()} indexed elements")

index_missing(file_collection, files)

#res = file_collection.query(query_texts=['Who is Dietmar Spangl?'])
#print(res)
