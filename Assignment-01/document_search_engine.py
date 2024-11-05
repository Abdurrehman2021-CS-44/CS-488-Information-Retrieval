import os
from collections import defaultdict

class DocumentSearchEngine:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.documents = {}  # Document ID to title and content mapping
    
    def load_documents(self):
        doc_id = 0
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    title = file.readline().strip()  # Assume first line is the title
                    content = file.read().strip()    # Remaining lines are the content
                    self.documents[doc_id] = {"title": title, "content": content}
                    doc_id += 1
        print(f"{len(self.documents)} documents loaded successfully.")

if __name__ == "__main__":
    folder_path = 'documents'
    search_engine = DocumentSearchEngine(folder_path)
    search_engine.load_documents()