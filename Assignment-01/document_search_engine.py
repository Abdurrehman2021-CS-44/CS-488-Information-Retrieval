import os
from collections import defaultdict
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

class DocumentSearchEngine:
    def __init__(self, folder_path):
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
    
    def index_document(self, doc_id, title, content):
        # Clean and tokenize title
        title_words = title.lower().split()
        filtered_title_words = [word for word in title_words if word not in stop_words]
        
        # Clean and tokenize content
        content_words = content.lower().split()
        filtered_content_words = [word for word in content_words if word not in stop_words]
        
        # Index title words
        for word in filtered_title_words:
            self.title_index[word].append(doc_id)
        
        # Index content words
        for word in filtered_content_words:
            self.content_index[word].append(doc_id)

    def search(self, query, search_by):
        query_words = query.lower().split()
        query_words = [word for word in query_words if word not in stop_words]
        
        if not query_words:
            return []

        # Choose the correct index based on the search preference
        index = self.title_index if search_by == "title" else self.content_index

        # Find documents containing all query words
        result_docs = set(index[query_words[0]])
        for word in query_words[1:]:
            result_docs &= set(index[word])
        
        return list(result_docs)

if __name__ == "__main__":
    folder_path = 'documents'
    search_engine = DocumentSearchEngine(folder_path)
    search_engine.load_and_index_documents()
    print(search_engine.search("artificial", "content"))