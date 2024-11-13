import os
import time
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
        print("Loading and indexing documents...")
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
        print(f"Loaded and indexed {doc_id} documents.")
    
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
        # Clean and tokenize query
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
    
    def display_results(self, doc_ids, search_by, query_time):
        print("\n" + "="*50)
        print(f"Search Results for '{search_by}' query in {query_time:.2f} seconds")
        print("="*50)
        
        if not doc_ids:
            print("No matching documents found.")
        else:
            for i, doc_id in enumerate(doc_ids, start=1):
                title = self.documents[doc_id]["title"]
                content_snippet = self.documents[doc_id]["content"][:200]  # Show first 200 chars of content
                print(f"\nResult {i}:")
                print("-" * 50)
                print(f"Document ID: {doc_id+1}")
                print(f"Title: {title}")
                if search_by == "content":
                    print(f"Content Preview: {content_snippet}...")
                print("-" * 50)
            print(f"\nTotal Results Found: {len(doc_ids)}")
    
    def test_search_engine(self, queries, search_by):
        for query in queries:
            print(f"Query: '{query}' (Search by: {search_by})")
            start_time = time.time()
            result_docs = self.search(query, search_by)
            query_time = time.time() - start_time
            self.display_results(result_docs, search_by, query_time)

if __name__ == "__main__":
    # Folder path for documents
    folder_path = 'documents'
    
    # Initialize the search engine
    search_engine = DocumentSearchEngine(folder_path)
    
    # Load and index documents
    search_engine.load_and_index_documents()
    
    # Simple command-line interface
    print("\nWelcome to the Simple Document Search Engine!\n")
    
    # Ask the user for search preference: by title or by content
    while True:
        print("\nOptions:\n1. Search by Title\n2. Search by Content\n3. Exit")
        choice = input("Select an option (1, 2, or 3): ").strip()
        
        if choice == '3':
            print("\nExiting search engine. Goodbye!")
            break
        elif choice == '1':
            search_by = 'title'
        elif choice == '2':
            search_by = 'content'
        else:
            print("Invalid option. Please select 1, 2, or 3.")
            continue

        # Perform the search based on the user's preference
        query = input("\nEnter search query: ").strip()
        if query:
            start_time = time.time()
            result_docs = search_engine.search(query, search_by)
            query_time = time.time() - start_time
            search_engine.display_results(result_docs, search_by, query_time)
        else:
            print("Please enter a non-empty query.")