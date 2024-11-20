import os
import time
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from simple_dictionary import SimpleDictionary

# Download NLTK resources if not already present
nltk.download('stopwords')
nltk.download('wordnet')

# Load English stopwords and initialize lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

class DocumentSearchEngine:
    def __init__(self, folder_path):
        """
        Initialize the Document Search Engine with SimpleDictionary.
        """
        self.folder_path = folder_path
        self.documents = SimpleDictionary()  # Use SimpleDictionary for documents
        self.inverted_index = SimpleDictionary()  # Use SimpleDictionary for inverted index
        self.tf_idf_scores = SimpleDictionary()  # Use SimpleDictionary for TF-IDF scores

    def load_documents(self):
        """
        Load documents from the folder and store them in the documents dictionary.
        """
        doc_id = 0
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    title = file.readline().strip()
                    content = file.read().strip()
                    self.documents.add(doc_id, {"title": title, "content": content})
                    doc_id += 1
        print(f"Loaded {doc_id} documents.")

    def preprocess(self, text):
        """
        Preprocess text by tokenizing, lemmatizing, and removing stopwords.
        """
        words = text.lower().split()
        return [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

    def build_inverted_index(self):
        """
        Build an inverted index from the loaded documents.
        """
        for doc_id in range(len(self.documents.buckets)):
            doc_data = self.documents.get(doc_id)
            if doc_data:
                doc = doc_data[0]
                content = doc["title"] + " " + doc["content"]
                terms = self.preprocess(content)
                for term in terms:
                    self.inverted_index.add(term, doc_id)
        print("Inverted index built.")

    def search(self, query):
        """
        Perform a search using the inverted index and rank results by term frequency.
        """
        query_terms = self.preprocess(query)
        doc_scores = {}

        for term in query_terms:
            matching_docs = self.inverted_index.get(term)
            for doc_id in matching_docs:
                doc_scores[doc_id] = doc_scores.get(doc_id, 0) + 1

        # Sort results by score in descending order
        return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    def display_results(self, ranked_docs, query_time):
        """
        Display search results to the user.
        """
        print("\n" + "=" * 50)
        print(f"Search Results (Query Time: {query_time:.2f} seconds)")
        print("=" * 50)

        if not ranked_docs:
            print("No matching documents found.")
        else:
            for i, (doc_id, score) in enumerate(ranked_docs, start=1):
                doc = self.documents.get(doc_id)[0]
                print(f"\nResult {i}:")
                print(f"Title: {doc['title']}")
                print(f"Content Preview: {doc['content'][:200]}...")
                print(f"Score: {score:.2f}")
        print("=" * 50)

def run_ui(search_engine):
    """
    Run a command-line user interface for the search engine.
    """
    print("\nWelcome to the Document Search Engine!\n")

    while True:
        print("\nOptions:\n1. Search by Term Frequency\n2. Exit")
        choice = input("Select an option (1, or 2): ").strip()

        if choice == '2':
            print("\nExiting the search engine. Goodbye!")
            break
        elif choice in {'1'}:
            query = input("\nEnter search query: ").strip()
            if query:
                start_time = time.time()
                results = search_engine.search(query)
                query_time = time.time() - start_time
                search_engine.display_results(results, query_time)
            else:
                print("Please enter a non-empty query.")
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    folder_path = "documents"  # Update with the correct path
    search_engine = DocumentSearchEngine(folder_path)

    # Load and index documents
    search_engine.load_documents()
    search_engine.build_inverted_index()

    # Start the user interface
    run_ui(search_engine)