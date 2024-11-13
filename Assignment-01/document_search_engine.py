# Document Search Engine
# This script implements a simple document search engine using inverted indexes for efficient
# searching by title and content. Users can load and index text documents from a specified folder,
# and then search for keywords or phrases, with the results ranked based on the frequency of
# query terms in the documents. It also includes a simple command-line interface for user interaction.

import os
import time
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from simple_dictionary import SimpleDictionary

# Load English stopwords to filter out common words like "the", "and", etc.
stop_words = set(stopwords.words('english'))

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

class DocumentSearchEngine:
    def __init__(self, folder_path):
        """
        Initialize the DocumentSearchEngine class.
        - folder_path: Path to the folder containing documents to index.
        """
        self.folder_path = folder_path
        self.title_index = SimpleDictionary()
        self.content_index = SimpleDictionary()
        self.documents = {}

    def extract_nouns(self, text):
        """
        Extract nouns from the given text using heuristic rules.
        Lemmatize the words before indexing.
        """
        words = text.split()  
        noun_suffixes = (
            "ion", "ment", "ness", "ity", "ty", "ance", "ence", "ure", "ship", "hood", 
            "er", "or", "ist", "al", "age", "cy", "dom"
        )
        nouns = []
        
        for word in words:
            word = lemmatizer.lemmatize(word.lower())
            if word[0].isupper() or word.endswith(noun_suffixes):
                nouns.append(word)
        
        return nouns

    def load_and_index_documents(self):
        """
        Load and index documents from the specified folder.
        """
        print("Loading and indexing documents...")
        doc_id = 0
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    title = file.readline().strip()
                    content = file.read().strip()
                    self.documents[doc_id] = {"title": title, "content": content}
                    self.index_document(doc_id, title, content)
                    doc_id += 1
        print(f"Loaded and indexed {doc_id} documents.")

    def index_document(self, doc_id, title, content):
        """
        Index a single document by extracting and indexing nouns from its title and content.
        """
        title_nouns = self.extract_nouns(title)
        content_nouns = self.extract_nouns(content)
        
        for noun in title_nouns:
            self.title_index.add(noun, doc_id)
        
        for noun in content_nouns:
            self.content_index.add(noun, doc_id)

    def search(self, query, search_by):
        """
        Search the indexed documents for the query terms and rank results based on frequency.
        """
        query_words = query.lower().split()
        query_words = [lemmatizer.lemmatize(word) for word in query_words if word not in stop_words]
        
        if not query_words:
            return []

        index = self.title_index if search_by == "title" else self.content_index
        doc_scores = {}

        for word in query_words:
            doc_ids = index.get(word)
            for doc_id in doc_ids:
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = 0
                doc_scores[doc_id] += 1

        ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)
        
        return [doc_id for doc_id, score in ranked_docs]

    def display_results(self, doc_ids, search_by, query_time):
        """
        Display the search results to the user.
        """
        print("\n" + "="*50)
        print(f"Search Results for '{search_by}' query in {query_time:.2f} seconds")
        print("="*50)
        
        if not doc_ids:
            print("No matching documents found.")
        else:
            for i, doc_id in enumerate(doc_ids, start=1):
                title = self.documents[doc_id]["title"]
                content_snippet = self.documents[doc_id]["content"][:200]
                print(f"\nResult {i}:")
                print("-" * 50)
                print(f"Document ID: {doc_id+1}")
                print(f"Title: {title}")
                if search_by == "content":
                    print(f"Content Preview: {content_snippet}...")
                print("-" * 50)
            print(f"\nTotal Results Found: {len(doc_ids)}")

    def test_search_engine(self, queries, search_by):
        """
        Test the search engine with a list of queries.
        """
        for query in queries:
            print(f"Query: '{query}' (Search by: {search_by})")
            start_time = time.time()
            result_docs = self.search(query, search_by)
            query_time = time.time() - start_time
            self.display_results(result_docs, search_by, query_time)

if __name__ == "__main__":
    # Folder path for documents (change this to the correct path on your system)
    folder_path = 'documents'
    
    # Initialize the search engine
    search_engine = DocumentSearchEngine(folder_path)
    
    # Load and index documents from the folder
    search_engine.load_and_index_documents()

    # Command-line interface
    print("\nWelcome to the Simple Document Search Engine!\n")
    
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

        query = input("\nEnter search query: ").strip()
        if query:
            start_time = time.time()
            result_docs = search_engine.search(query, search_by)
            query_time = time.time() - start_time
            search_engine.display_results(result_docs, search_by, query_time)
        else:
            print("Please enter a non-empty query.")