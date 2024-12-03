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

# Create a binary term-document matrix
def create_term_document_matrix(documents):
    """
    Create a term-document matrix where each term is assigned a binary weight (1 if present, 0 if absent).
    """
    vocabulary = set()
    for doc in documents:
        vocabulary.update(preprocess(doc))
    
    vocabulary = sorted(vocabulary)
    term_index = {term: idx for idx, term in enumerate(vocabulary)}

    matrix = [[0] * len(vocabulary) for _ in range(len(documents))]

    for doc_idx, doc in enumerate(documents):
        terms = preprocess(doc)
        for term in terms:
            matrix[doc_idx][term_index[term]] = 1

    return matrix, vocabulary

# Represent query as a binary vector
def query_vector(query, vocabulary):
    """
    Represent the query as a binary vector based on the vocabulary.
    """
    query_terms = preprocess(query)
    return [1 if term in query_terms else 0 for term in vocabulary]

# Compute similarity score (Dice coefficient)
def compute_similarity(doc_vector, query_vector):
    """
    Compute similarity using Dice coefficient.
    """
    intersection = sum(1 for d, q in zip(doc_vector, query_vector) if d == q == 1)
    doc_sum = sum(doc_vector)
    query_sum = sum(query_vector)
    dice_score = (2 * intersection) / (doc_sum + query_sum) if (doc_sum + query_sum) > 0 else 0
    print(f"Intersection: {intersection}, Document sum: {doc_sum}, Query sum: {query_sum}, Dice score: {dice_score}")  # Debug
    return dice_score

# Rank documents based on similarity scores
def rank_documents(term_document_matrix, query_vec):
    """
    Rank documents based on similarity scores.
    """
    scores = [(idx, compute_similarity(doc, query_vec)) for idx, doc in enumerate(term_document_matrix)]
    return sorted(scores, key=lambda x: x[1], reverse=True)

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

# Main BIM retrieval function
def bim_retrieval(documents, query):
    """
    Perform Binary Independence Model (BIM) retrieval.
    """
    term_document_matrix, vocabulary = create_term_document_matrix(documents)
    query_vec = query_vector(query, vocabulary)
    ranked_docs = rank_documents(term_document_matrix, query_vec)
    return [(documents[idx], score) for idx, score in ranked_docs]

# CLI Interface
def main():
    # Automatically load documents
    folder_path = "documents/"  # Set the folder path here
    documents = load_documents(folder_path)

    while True:
        print("\n---- BIM Retrieval System ----")
        print("1. Perform search query")
        print("2. Exit")
        
        choice = input("Enter your choice (1/2): ").strip()
        
        if choice == "1":
            # Perform search query
            query = input("Enter your search query: ").strip()
            # top_k = int(input("Enter the number of top results to display (default 5): ").strip() or 5)
            results = bim_retrieval(documents, query)
            print("\nTop results:")
            for rank, (doc, score) in enumerate(results, start=1):
                print(f"{rank}. Score: {score:.3f} - Document: {doc}")
        
        elif choice == "2":
            print("Exiting the BIM Retrieval System.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()