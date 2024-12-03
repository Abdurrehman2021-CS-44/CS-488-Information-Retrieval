import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Define preprocessing functions
def preprocess(text):
    """
    Preprocess text by tokenizing, lemmatizing, and removing stopwords.
    """
    words = text.lower().split()
    return [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

# Create an inverted index
def create_inverted_index(documents):
    """
    Create an inverted index mapping terms to the list of documents they appear in.
    """
    inverted_index = {}
    for doc_id, text in enumerate(documents):
        terms = preprocess(text)
        for term in terms:
            if term not in inverted_index:
                inverted_index[term] = []
            if doc_id not in inverted_index[term]:
                inverted_index[term].append(doc_id)
    return inverted_index

# Retrieve documents for a term
def retrieve_documents(term, inverted_index):
    """
    Retrieve the list of document IDs associated with a given term.
    """
    return inverted_index.get(term, [])

# Perform union of two lists without duplicates
def union_lists(list1, list2):
    """
    Combine two lists into a single list without duplicates.
    """
    result = list1[:]  # Make a copy of the first list
    for item in list2:
        if item not in result:
            result.append(item)
    return result

# Non-Overlapped List Retrieval
def non_overlapped_list_model(documents, terms_of_interest):
    """
    Retrieve a non-overlapping list of documents for the given terms of interest.
    """
    # Create an inverted index
    inverted_index = create_inverted_index(documents)
    
    # Retrieve documents for each term
    non_overlap_docs = []
    for term in terms_of_interest:
        term_docs = retrieve_documents(term, inverted_index)
        non_overlap_docs = union_lists(non_overlap_docs, term_docs)
    
    # Return the list of document IDs and their content
    return [(doc_id, documents[doc_id]) for doc_id in non_overlap_docs]

# Load documents from a folder
def load_documents(folder_path):
    """
    Load documents from the folder and return a list of their contents.
    """
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                documents.append(file.read().strip())
    print(f"Loaded {len(documents)} documents.")
    return documents

# CLI Interface
def main():
    # Load documents from the folder
    folder_path = "documents/"  # Set the folder path here
    documents = load_documents(folder_path)

    while True:
        print("\n---- Non-Overlapping Document Retrieval ----")
        print("1. Perform search query")
        print("2. Exit")
        
        choice = input("Enter your choice (1/2): ").strip()
        
        if choice == "1":
            # Perform search query
            terms_input = input("Enter terms of interest (space-separated): ").strip()
            terms_of_interest = terms_input.split()  # Split by spaces into individual terms
            results = non_overlapped_list_model(documents, terms_of_interest)
            
            print("\nNon-overlapping results:")
            for rank, (doc_id, doc) in enumerate(results, start=1):
                print(f"{rank}. Document ID: {doc_id} - Content: {doc}")
        
        elif choice == "2":
            print("Exiting the Document Retrieval System.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()