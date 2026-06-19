import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


with open("data/menu.json") as f:
    menu = json.load(f)


documents = []

for item in menu:
    text = f"""
    Name: {item['name']}
    Price: {item['price']}
    Category: {item['category']}
    Ingredients: {item['ingredients']}
    Nutrition: {item['nutrition']}
    """

    documents.append(text)


embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


db = Chroma.from_texts(
    documents,
    embedding,
    persist_directory="food_database"
)


print("Database created")