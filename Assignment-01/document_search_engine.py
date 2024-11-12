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

        # Dictionary to store document scores based on the frequency of query words
        doc_scores = defaultdict(int)

        # Calculate a simple score for each document based on query term frequency
        for word in query_words:
            if word in index:
                for doc_id in index[word]:
                    doc_scores[doc_id] += 1  # Increase score for each occurrence of the query word

        # Sort documents by score in descending order (documents with higher scores appear first)
        ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)
        
        # Extract only the document IDs in ranked order
        return [doc_id for doc_id, score in ranked_docs]
    
    def display_results(self, doc_ids, search_by):
        if not doc_ids:
            print("No matching documents found.")
        else:
            for doc_id in doc_ids:
                title = self.documents[doc_id]["title"]
                content_snippet = self.documents[doc_id]["content"][:200]  # Show first 200 chars of content
                print(f"Document ID: {doc_id+1}")
                print(f"Title: {title}")
                if search_by == "content":
                    print(f"Content: {content_snippet}...")
                print()  # Blank line for readability
    
    def test_search_engine(self, queries, search_by):
        for query in queries:
            print(f"Query: '{query}' (Search by: {search_by})")
            result_docs = self.search(query, search_by)
            self.display_results(result_docs, search_by)

if __name__ == "__main__":
    # Folder path for documents
    folder_path = 'documents'
    
    # Initialize the search engine
    search_engine = DocumentSearchEngine(folder_path)
    
    # Load and index documents
    search_engine.load_and_index_documents()
    
    # Simple command-line interface
    print("Welcome to the Simple Document Search Engine!")
    
    # Ask the user for search preference: by title or by content
    while True:
        search_by = input("\nWould you like to search by 'title' or 'content'? (type 'exit' to quit): ").strip().lower()
        if search_by == 'exit':
            print("Exiting search engine. Goodbye!")
            break
        elif search_by not in {'title', 'content'}:
            print("Invalid option. Please enter 'title' or 'content'.")
            continue

        # Perform the search based on the user's preference
        query = input("Enter search query: ").strip()
        result_docs = search_engine.search(query, search_by)
        search_engine.display_results(result_docs, search_by)