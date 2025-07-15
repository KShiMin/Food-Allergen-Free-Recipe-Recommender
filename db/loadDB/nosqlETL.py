import re
import csv
import pandas as pd
from pathlib import Path
from fractions import Fraction
from datetime import datetime
from db.nosql.nosql import MongoCRUD


class ETL:
    
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    CSV_PATH = BASE_DIR.joinpath('data', 'recipes_final_v3.csv')
    
    def __init__(self, client):
        self.client = client
        self.recipe_df = pd.read_csv(self.CSV_PATH)
    
    def safe_value(self, val, fallback="", cast=str):
        if pd.isna(val):
            return fallback
        return cast(val)
    
    def parse_time_to_minutes(self, time_str):
        if pd.isna(time_str) or str(time_str).strip() == "":
            return 0
        
        text = str(time_str).lower()
        total_minutes = 0
        
        # Look for hours
        hours_match = re.search(r"(\d+)\s*hrs", text)
        if hours_match:
            total_minutes += int(hours_match.group(1)) * 60

        # Look for minutes
        mins_match = re.search(r"(\d+)\s*mins", text)
        if mins_match:
            total_minutes += int(mins_match.group(1))

        # If no match, try if it's just a number (e.g., "15")
        if total_minutes == 0:
            num_match = re.match(r"^\s*(\d+)\s*$", text)
            if num_match:
                total_minutes = int(num_match.group(1))

        return total_minutes     
       
    def parse_preparation_notes(self, notes_raw):
        if pd.isna(notes_raw):
            return ""
        
        notes = str(notes_raw).split("|")
        notes = [n.strip() for n in notes]
        if len(notes) > 1:
            return [{"before": notes[0], "after": notes[1]}]
        else:
            return [{"before": notes[0]}]
    
    def build_recipe_documents(self):
        recipes = {}
        for recipe_id, group in self.recipe_df.groupby("recipe_id"):
            recipe_doc = self.process_recipe_group(group)
            recipes[recipe_id] = recipe_doc
        return recipes
    
    def process_recipe_group(self, group):
        first_item = group.iloc[0]
        
        instructions = self.process_instructions(first_item.directions)
        ingredients = self.process_ingredients(group)
        
        recipe_doc = {
            "_id": int(first_item.recipe_id),
            "name": self.safe_value(first_item["recipe_name"]),
            "prep_time": self.parse_time_to_minutes(first_item["prep_time"]),
            "cook_time": self.parse_time_to_minutes(first_item["cook_time"]),
            "servings": self.safe_value(first_item["servings"], fallback=None, cast=int),
            "ingredients": ingredients,
            "instruction": instructions,
            "cusine_path": self.safe_value(first_item["cusine_path"]),
            "calories": self.safe_value(first_item['calories'], fallback=None, cast=int),
            "img_src": self.safe_value(first_item["img_src"]),
            "video_url": self.safe_value(first_item.get("youtube_url", None)),            
        }
        
        return recipe_doc
    
    
    def process_ingredients(self, group):
        
        ingredients = []
        for row in group.itertuples():
            # Quantity handling
            quantity_raw = row.quantity
            if pd.isna(quantity_raw) or str(quantity_raw).strip() == "":
                quantity_str = "0"
            else:
                fraction_obj = Fraction(float(quantity_raw)).limit_denominator(10)  # Limits fractions from being too big
                quantity_str = str(fraction_obj)

            preparation_notes = self.parse_preparation_notes(row.preparation_notes)

            ingredients.append({
                "ingredient_id": str(row.ingredient_id),
                "quantity": quantity_str,
                "units": self.safe_value(row.units),
                "preparation_notes": preparation_notes
            })
            
        return ingredients
    
    def process_instructions(self, directions_str):
        if pd.isna(directions_str):
            return []
        
        directions_split = str(directions_str).split("\n")
        instructions = [
            {"step_id": idx, "instructions": step}
            for idx, step in enumerate(directions_split, 1)
            if step.strip()
        ]
        
        return instructions
    
    def load_reviews(self):
        review_csv_path = self.BASE_DIR / "data" / "sample_reviews.csv"

        if not review_csv_path.exists():
            print("No sample_reviews.csv file found. Skipping review import.")
            return []

        reviews = []
        with open(review_csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                reviews.append({
                    "recipe_id": int(row["recipe_id"]),
                    "user_id": int(row["user_id"]),
                    "description": row["description"],
                    "rating": int(row["rating"]),
                    "imgs": row["imgs"].split(",") if row["imgs"] else [],
                    "videos": row["videos"].split(",") if row["videos"] else [],
                    "video_url": row["video_url"],
                    "created_at": datetime.fromisoformat(row["created_at"])
                })
        return reviews
    
    def run(self):
        recipes = self.build_recipe_documents()
        docs = list(recipes.values())
        
        if not docs:
            print("No recipes to insert.")
            return 
        
        try:
            result = self.client.insert("Recipes", docs, ordered=False)
            print(f"{len(result.inserted_ids)} recipes inserted successfully")
        except Exception as e:
            print(f"Error during bulk insert: {e}")
        
        # Reviews
        review_docs = self.load_reviews()
        if review_docs:
            try:
                result = self.client.insert("Reviews", review_docs, ordered=False)
                print(f"{len(result.inserted_ids)} reviews inserted successfully")
            except Exception as e:
                print(f"Error during review insert: {e}")

def main():
    mongo_client = MongoCRUD()
    etl = ETL(mongo_client)
    etl.run()

# Without uv run
if __name__ == '__main__':
    main()