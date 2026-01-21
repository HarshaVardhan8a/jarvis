import os
from jarvis_core import Jarvis

def ingest_data():
    jarvis = Jarvis()
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} not found.")
        return

    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if filename.endswith(".txt") or filename.endswith(".pdf"):
            print(f"Ingesting {filename}...")
            try:
                chunks = jarvis.add_document(file_path)
                print(f"Successfully added {filename} with {chunks} chunks.")
            except Exception as e:
                print(f"Error adding {filename}: {e}")

if __name__ == "__main__":
    ingest_data()
