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

# Initialize lemmatizer for word normalization
lemmatizer = WordNetLemmatizer()

class DocumentSearchEngine:
    def __init__(self, folder_path):
        """
        Initialize the DocumentSearchEngine class with a folder path containing documents to index.
        - folder_path: Path to the folder containing documents to index.
        """
        self.folder_path = folder_path
        # Using SimpleDictionary to store inverted indexes for title and content
        self.title_index = SimpleDictionary()
        self.content_index = SimpleDictionary()
        # Store documents in a dictionary with their ID as key
        self.documents = {}

    def extract_nouns(self, text, isTitle):
        """
        Extract nouns from the given text using heuristic rules.
        Lemmatize the words before indexing.
        Nouns are identified by specific suffixes or capitalized letters (proper nouns).
        """
        words = text.split()  # Split text into individual words
        noun_suffixes = (
            "ion", "ment", "ness", "ity", "ty", "ance", "ence", "ure", "ship", "hood", 
            "er", "or", "ist", "al", "age", "cy", "dom"
        )
        nouns = []
        
        for word in words:
            word = lemmatizer.lemmatize(word.lower())  # Lemmatize to normalize words
            # Check if the word is capitalized (proper noun) or ends with known noun suffix
            if isTitle:
                nouns.append(word)
            else:
                if word[0].isupper() or word.endswith(noun_suffixes):
                    nouns.append(word)
        
        return nouns

    def load_and_index_documents(self):
        """
        Load documents from the specified folder and index them by extracting nouns
        from both titles and content for fast searching.
        """
        print("Loading and indexing documents...")
        doc_id = 0
        # Iterate over each file in the folder and process it
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):  # Process only files
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Read title and content from the document
                    title = file.readline().strip()
                    content = file.read().strip()
                    # Store the document in the dictionary with a unique ID
                    self.documents[doc_id] = {"title": title, "content": content}
                    # Index the document by extracting nouns from title and content
                    self.index_document(doc_id, title, content)
                    doc_id += 1
        print(f"Loaded and indexed {doc_id} documents.")

    def index_document(self, doc_id, title, content):
        """
        Index a single document by extracting and indexing nouns from its title and content.
        This helps in creating inverted indices for efficient searching.
        """
        title_nouns = self.extract_nouns(title, isTitle=True)  # Extract nouns from the title
        content_nouns = self.extract_nouns(content, isTitle=False)  # Extract nouns from the content
        
        # Add the nouns from the title to the title index
        for noun in title_nouns:
            self.title_index.add(noun, doc_id)
        
        # Add the nouns from the content to the content index
        for noun in content_nouns:
            self.content_index.add(noun, doc_id)

    def search(self, query, search_by):
        """
        Search the indexed documents for the query terms and rank results based on frequency.
        The search can be performed either on the title or content based on the user's choice.
        """
        # Preprocess the query by converting to lowercase, removing stopwords, and lemmatizing
        query_words = query.lower().split()
        query_words = [lemmatizer.lemmatize(word) for word in query_words if word not in stop_words]
        
        if not query_words:  # If query is empty or contains only stopwords
            return []

        # Choose the correct index based on the search type (title or content)
        index = self.title_index if search_by == "title" else self.content_index
        doc_scores = {}

        # For each query word, check which documents contain it and increment their score
        for word in query_words:
            doc_ids = index.get(word)  # Get the document IDs that contain the word
            for doc_id in doc_ids:
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = 0
                doc_scores[doc_id] += 1  # Increment score for each occurrence of the word

        # Rank the documents by their scores (higher score means more relevant)
        ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)
        
        # Return the document IDs ordered by their relevance
        return [doc_id for doc_id, score in ranked_docs]

    def display_results(self, doc_ids, search_by, query_time):
        """
        Display the search results to the user, showing the document title and a snippet of content
        along with the search query time.
        """
        print("\n" + "="*50)
        print(f"Search Results for '{search_by}' query in {query_time:.2f} seconds")
        print("="*50)
        
        if not doc_ids:
            print("No matching documents found.")
        else:
            # Display information for each document
            for i, doc_id in enumerate(doc_ids, start=1):
                title = self.documents[doc_id]["title"]
                content_snippet = self.documents[doc_id]["content"][:200]  # Preview first 200 characters of content
                print(f"\nResult {i}:")
                print("-" * 50)
                print(f"Document ID: {doc_id+1}")
                print(f"Title: {title}")
                if search_by == "content":
                    print(f"Content Preview: {content_snippet}...")
                print("-" * 50)
            print(f"\nTotal Results Found: {len(doc_ids)}")

def run_ui(search_engine):
    """
    Command-line user interface for interacting with the Document Search Engine.
    Allows the user to search by title or content and displays the results.
    """
    print("\nWelcome to the Simple Document Search Engine!\n")
    
    while True:
        print("\nOptions:\n1. Search by Title\n2. Search by Content\n3. Exit")
        choice = input("Select an option (1, 2, or 3): ").strip()
        
        if choice == '3':
            print("\nExiting search engine. Goodbye!")
            break
        elif choice == '1':
            search_by = 'title'  # Search by title
        elif choice == '2':
            search_by = 'content'  # Search by content
        else:
            print("Invalid option. Please select 1, 2, or 3.")
            continue

        query = input("\nEnter search query: ").strip()  # User enters search query
        if query:
            start_time = time.time()
            result_docs = search_engine.search(query, search_by)  # Perform the search
            query_time = time.time() - start_time  # Measure the query time
            search_engine.display_results(result_docs, search_by, query_time)  # Display the results
        else:
            print("Please enter a non-empty query.")

if __name__ == "__main__":
    # Folder path for documents (change this to the correct path on your system)
    folder_path = 'documents'
    
    # Initialize the search engine
    search_engine = DocumentSearchEngine(folder_path)
    
    # Load and index documents from the folder
    search_engine.load_and_index_documents()

    # Run the user interface
    run_ui(search_engine)