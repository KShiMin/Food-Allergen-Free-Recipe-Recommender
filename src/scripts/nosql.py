from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

# Database name
db = client["allergen-free-recipes"]

# Collections
recipes = db["Recipes"]
reviews = db["Reviews"]
recipeIngr = db["RecipeIngredient"]

# Datas
