

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_PATH = os.path.join(BASE_DIR, "..", "data", "recipes_final.csv")

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# recipes_df = pd.read_csv(DATA_PATH)

# # Helper to safely get a value with fallback
# def safe_value(val, fallback="", cast=str):
#     if pd.isna(val):
#         return fallback
#     return cast(val)

# # Helper to convert string time to int time for storage
# def parse_time_to_minutes(time_str):
#     if pd.isna(time_str) or str(time_str).strip() == "":
#         return 0

#     text = str(time_str).lower()
#     total_minutes = 0

#     # Look for hours
#     hours_match = re.search(r"(\d+)\s*hrs", text)
#     if hours_match:
#         hours = int(hours_match.group(1))
#         total_minutes += hours * 60

#     # Look for minutes
#     mins_match = re.search(r"(\d+)\s*mins", text)
#     if mins_match:
#         mins = int(mins_match.group(1))
#         total_minutes += mins

#     # If no match, try if it's just a number (e.g., "15")
#     if total_minutes == 0:
#         num_match = re.match(r"^\s*(\d+)\s*$", text)
#         if num_match:
#             total_minutes = int(num_match.group(1))

#     # If still 0, consider as None
#     if total_minutes == 0:
#         return 0

#     return total_minutes

# # Helper to parse preparation notes
# def parse_preparation_notes(notes_raw):
#     if pd.isna(notes_raw):
#         return ""
    
#     notes = str(notes_raw).split("|")
#     notes = [n.strip() for n in notes]
#     if len(notes) > 1:
#         return [{"before": notes[0], "after": notes[1]}]
#     else:
#         return [{"before": notes[0]}]

# recipes = {}

# for recipe_id, group in recipes_df.groupby("recipe_id"):
#     first_item = group.iloc[0]

#     # Instructions split
#     directions_split = str(first_item.directions).split("\n")
#     instructions = [
#         {"step_id": idx, "instructions": step}
#         for idx, step in enumerate(directions_split, 1)
#         if step.strip()
#     ]

#     # Ingredients processing
#     ingredients = []
#     for row in group.itertuples():
#         # Quantity handling
#         quantity_raw = row.quantity
#         if pd.isna(quantity_raw) or str(quantity_raw).strip() == "":
#             quantity_str = "0"
#         else:
#             fraction_obj = Fraction(float(quantity_raw)).limit_denominator(10)  # Limits fractions from being too big
#             quantity_str = str(fraction_obj)

#         preparation_notes = parse_preparation_notes(row.preparation_notes)

#         ingredients.append({
#             "ingredient_id": str(row.ingredient_id),
#             "quantity": quantity_str,
#             "units": safe_value(row.units),
#             "preparation_notes": preparation_notes
#         })

#     # Final recipe document
#     recipe_doc = {
#         "_id": recipe_id,
#         "name": safe_value(first_item["recipe_name"]),
#         "prep_time": parse_time_to_minutes(first_item["prep_time"]),
#         "cook_time": parse_time_to_minutes(first_item["cook_time"]),
#         "servings": safe_value(first_item["servings"], fallback=None, cast=int),
#         "ingredients": ingredients,
#         "instruction": instructions,
#         "cusine_path": safe_value(first_item["cusine_path"]),
#         "img_src": safe_value(first_item["img_src"]),
#         "video_url": safe_value(first_item.get("youtube_url", None)),
#     }


#     recipes[recipe_id] = recipe_doc

# # Convert to list of documents
# recipe_documents = list(recipes.values())

# client = MongoClient("mongodb://localhost:27017/")

# # Database name
# db = client["allergen-free-recipes"]

# # Collections
# recipes = db["Recipes"]
# reviews = db["Reviews"]

# # recipes.delete_many({})

# # Inserting Data
# recipes.insert_many(recipe_documents)
# for doc in recipes.find():
#     print(doc)
#     print("\n")
import os
import re
import pandas as pd
from fractions import Fraction
from pymongo import MongoClient


class MongoCRUD:
    
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["allergen-free-recipes"]
        
    def insert(self, collection, data):
        if isinstance(data, dict):
            return self.db[collection].insert_one(data)
        elif isinstance(data, list):
            return self.db[collection].insert_many(data)
        else:
            raise ValueError("Data must be dict or list of dicts.")
        
    def find_one(self, collection, query):
        return self.db[collection].find_one(query)
    
    def find_many(self, collection, query):
        return list(self.db[collection].find(query))
    
    def update_one(self, collection, query, update):
        return self.db[collection].update_one(query, {"$set": update})

    def delete_one(self, collection: str, query):
        return self.db[collection].delete_one(query)
    
    # Graceful Closing - ensure proper exit
    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()