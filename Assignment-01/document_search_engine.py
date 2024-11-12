import os
from collections import defaultdict
import re
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

class DocumentSearchEngine:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.title_index = defaultdict(list)    # Index for titles
        self.content_index = defaultdict(list)  # Index for content
        self.documents = {}  # Document ID to title and content mapping
    
    def load_and_index_documents(self):
        doc_id = 0
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    title = file.readline().strip()  # Assume first line is the title
                    content = file.read().strip()    # Remaining lines are the content
                    self.documents[doc_id] = {"title": title, "content": content}
                    self.index_document(doc_id, title, content)
                    doc_id += 1

        print(f"{len(self.documents)} documents loaded successfully.")
        print(f"Title: {self.title_index}")
        print(f"Content: {self.content_index}")
    
    def index_document(self, doc_id: int, title: str, content: str):
        # Clean and tokenize title
        title_words = re.findall(r'\w+', title.lower())
        filtered_title_words = [word for word in title_words if word not in stop_words]
        
        # Clean and tokenize content
        content_words = re.findall(r'\w+', content.lower())
        filtered_content_words = [word for word in content_words if word not in stop_words]
        
        # Index title words
        for word in filtered_title_words:
            self.title_index[word].append(doc_id)
        
        # Index content words
        for word in filtered_content_words:
            self.content_index[word].append(doc_id)

if __name__ == "__main__":
    folder_path = 'documents'
    search_engine = DocumentSearchEngine(folder_path)
    search_engine.load_and_index_documents()