from pathlib import Path
from os import environ
import chromadb

def get_env(name:str) -> str:
    val = environ.get(name)
    if not val:
        raise ValueError(f"Environment variable '{name}' not set.")
    return val

INDEX_ROOT = get_env('SEMSEARCH_INDEX_ROOT')
DB_PATH = get_env('SEMSEARCH_DB')

def get_files_to_index(root:str) -> [str]:
    result = []
    for path in Path(root).rglob('*'):
        if path.suffix.lower() == ".pdf":
            result.append(path)
    return result

print(f"Load database from '{DB_PATH}' ... ", end="")
client = chromadb.PersistentClient(path=DB_PATH)
print("ok")

print(f"List files to index in {INDEX_ROOT} ... ", end="")
files = get_files_to_index(INDEX_ROOT)
print(f"found {len(files)} files")


