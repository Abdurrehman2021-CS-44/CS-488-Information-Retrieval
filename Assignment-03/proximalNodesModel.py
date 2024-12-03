import os
import json
from itertools import combinations
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Preprocessing utilities
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    """
    Preprocess text by tokenizing, lemmatizing, and removing stopwords.
    """
    words = text.lower().split()
    return [lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words]

# Build a graph of terms and documents
def build_graph(documents):
    """
    Build a graph connecting terms to documents and terms to terms within the same document.
    """
    graph = {}
    
    def add_node(node):
        if node not in graph:
            graph[node] = set()
    
    def add_edge(node1, node2):
        add_node(node1)
        add_node(node2)
        graph[node1].add(node2)
        graph[node2].add(node1)

    for doc_id, doc_content in enumerate(documents):
        terms = preprocess(doc_content)
        document_node = f"doc_{doc_id}"
        
        # Link terms to document
        for term in terms:
            add_edge(term, document_node)
        
        # Link terms to other terms within the document
        for term1, term2 in combinations(terms, 2):
            add_edge(term1, term2)
    
    return graph

def retrieve_documents(proximal_nodes, graph, documents):
    """
    Retrieve documents strongly connected to the given proximal nodes using BFS.
    """
    visited = set()
    connected_documents = set()
    queue = list(proximal_nodes)
    
    while queue:
        current_node = queue.pop(0)
        if current_node not in visited:
            visited.add(current_node)
            for neighbor in graph.get(current_node, []):
                if neighbor.startswith("doc_"):  # Document node
                    # Check if the document contains any of the proximal nodes
                    doc_index = int(neighbor.split("_")[1])
                    doc_content = documents[doc_index].lower()
                    if any(term in doc_content for term in proximal_nodes):
                        connected_documents.add(neighbor)
                else:  # Continue exploring term nodes
                    queue.append(neighbor)
    
    return connected_documents

# Load documents from a folder
def load_documents(folder_path):
    """
    Load documents from the folder and return a list of their contents.
    """
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                documents.append(" ".join(section["content"] for section in data.get("sections", [])))
    print(f"Loaded {len(documents)} documents.")
    return documents

# CLI Interface
def main():
    # Load documents
    folder_path = "json_documents/"  # Set the folder path here
    documents = load_documents(folder_path)

    print(documents)
    input()

    # Build graph
    print("Building the graph...")
    graph = build_graph(documents)
    print("Graph built successfully!")

    while True:
        print("\n---- Proximal Nodes Document Retrieval ----")
        print("1. Perform search query")
        print("2. Exit")
        
        choice = input("Enter your choice (1/2): ").strip()
        
        if choice == "1":
            # Perform search query
            terms_input = input("Enter terms of interest (space-separated): ").strip()
            terms_of_interest = terms_input.split()  # Split by spaces into individual terms
            terms_of_interest = [term.lower() for term in terms_of_interest]
            connected_docs = retrieve_documents(terms_of_interest, graph, documents)
            
            print("\nConnected Documents:")
            if connected_docs:
                for doc_id in sorted(connected_docs):
                    doc_index = int(doc_id.split("_")[1])
                    print(f"Document ID: {doc_id} - Content: {documents[doc_index][:100]}...")
            else:
                print("No documents found for the specified proximal nodes.")
        
        elif choice == "2":
            print("Exiting the Proximal Nodes Document Retrieval System.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()