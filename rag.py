#!/usr/bin/env python3.10
"""
On mac:

$ brew install ollama
$ ollama pull llama3.2

"""
import chromadb
from chromadb.utils import embedding_functions
import ollama  # Requires: pip install ollama

def main():
    # --- SETUP (Vector DB) ---
    client = chromadb.EphemeralClient()
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.create_collection(name="office_rules", embedding_function=emb_fn)

    # --- DOCUMENT CHUNKING & STORAGE ---
    text = "PET POLICY: Well-behaved dogs are allowed in the office on Fridays. They must be leashed at all times and have up-to-date vaccinations."
    collection.add(
        documents=[text],
        ids=["pet_policy_01"]
    )

    # --- QUERY PROCESSING ---
    user_query = "Can I bring my golden retriever to work?"

    # --- VECTOR SEARCH ---
    results = collection.query(query_texts=[user_query], n_results=1)
    context = results['documents'][0][0]

    # --- CONTEXT AUGMENTATION & RESPONSE GENERATION ---
    # This is the "Grammar/Logic" engine.
    # We tell the AI exactly how to behave using a System Prompt.

    prompt = f"Context: {context}\n\nQuestion: {user_query}\n\nAnswer:"

    # This call sends the context to the LLM to generate the fluid sentence
    response = ollama.generate(
        model='llama3.2',
        prompt=f"Based on the context, answer the question naturally. {prompt}"
    )

    print(f"Generated Response: {response['response']}")

if __name__ == "__main__":
    # Note: This requires the Ollama app running and 'llama3' pulled.
    # If you don't have Ollama, you can use a Mock function or an API key.
    try:
        main()
    except Exception as e:
        print(f"To run this code, ensure Ollama is installed. Error: {e}")
