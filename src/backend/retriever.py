import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# Load the embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


# Load the food database
with open("data/menu.json", "r") as file:
    menu = json.load(file)


# Convert food items into text documents
documents = []

for item in menu:
    text = f"""
    Name: {item.get('name', 'Unknown')}
    Price: {item.get('price', 'N/A')}
    Category: {item.get('category', 'N/A')}
    Ingredients: {', '.join(item.get('ingredients', []))}
    Protein: {item.get('protein', 'N/A')}
    Calories: {item.get('calories', 'N/A')}
    """

    documents.append(text)


# Create vector database
db = Chroma.from_texts(
    documents,
    embedding_model,
    persist_directory="food_database"
)


def search_food(query):
    results = db.similarity_search(
        query,
        k=2
    )

    return results

if __name__ == "__main__":
    results = search_food(
        "I want cheap high protein food"
    )

    for result in results:
        print(result.page_content)