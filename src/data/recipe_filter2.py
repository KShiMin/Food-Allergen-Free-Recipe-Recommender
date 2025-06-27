import re
import pandas as pd
import spacy
from fractions import Fraction
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "recipes.csv")
export_path_raw = os.path.join(BASE_DIR, "filtered_recipe_raw.csv")
export_path = os.path.join(BASE_DIR, "filtered_recipe_ai.csv")

nlp = spacy.load("en_core_web_sm")

pd.set_option('display.max_colwidth', None)

recipes = pd.read_csv(csv_path)

recipes_wanted = ["Joy's Easy Banana Bread", "Pan-Fried Shrimp", "Refreshing Cucumber Watermelon Salad", 
                  "Applesauce Pork Chops", "Risotto with Fresh Figs and Prosciutto", "Gorgonzola Pear Pasta",
                 "Char Siu (Chinese Barbeque Pork)", "Cherry Chicken Salad", "Mexican Chicken Soup", 
                  "Fresh Fig and Prosciutto Pasta Sauce"]

PREP_KEYWORDS = {
    "chopped", "minced", "diced", "melted", "mashed", "sliced", "peeled",
    "grated", "halved", "softened", "crushed", "ground", "beaten",
    "roasted", "toasted", "boiled", "fried", "ripe", "unsalted",
    "salted", "fresh", "cold", "warm", "drained", "thinly", "thickly",
    "seedless", "divided", "extra-virgin", "cored"
}

UNITS = [
    "cup", "cups", "tablespoon", "tablespoons", "teaspoon", "teaspoons",
    "tbsp", "tsp", "pound", "pounds", "oz", "ounce", "ounces",
    "pinch", "clove", "cloves", "slice", "slices", "gram", "grams",
    "package", "inch"
]

FRACTION_MAP = {
    "¼": "1/4",
    "½": "1/2",
    "¾": "3/4",
    "⅐": "1/7",
    "⅑": "1/9",
    "⅒": "1/10",
    "⅓": "1/3",
    "⅔": "2/3",
    "⅕": "1/5",
    "⅖": "2/5",
    "⅗": "3/5",
    "⅘": "4/5",
    "⅙": "1/6",
    "⅚": "5/6",
    "⅛": "1/8",
    "⅜": "3/8",
    "⅝": "5/8",
    "⅞": "7/8"
}

def parse_fraction(text):
    text = text.strip()
    # Replace unicode fractions with ascii equivalents
    for uni, ascii_frac in FRACTION_MAP.items():
        text = text.replace(uni, ascii_frac)
    try:
        # Handle mixed numbers like '1 1/2'
        parts = text.split()
        if len(parts) == 2:
            return str(float(int(parts[0]) + Fraction(parts[1])))
        else:
            return str(float(Fraction(text)))
    except Exception:
        return text  # fallback if parsing fails


def parse_ingredient(item):
    original = item.strip().lower()

    # Split by hyphen if preparation is after the name
    parts = original.split(" - ")
    main_part = parts[0].strip()
    extra_prep = parts[1].strip() if len(parts) > 1 else ""

    # Regex to find quantity (supporting fractions)
    qty_match = re.match(r"(\d+/\d+|\d+\s\d+/\d+|\d+|\d+\.\d+|¼|½|¾|⅛|⅜|⅝|⅞|⅓|⅔|⅕|⅖|⅗|⅘)", main_part)
    quantity = parse_fraction(qty_match.group(1)) if qty_match else None

    # Remove quantity
    if quantity:
        main_part = main_part.replace(qty_match.group(1), "").strip()

    # Find unit
    unit = None
    for u in UNITS:
        if main_part.startswith(u):
            unit = u
            main_part = main_part[len(u):].strip()
            break

    # Tokenize for ingredient and preparation terms
    doc = nlp(main_part)

    ingredient_terms = []
    prep_terms = []

    for token in doc:
        if token.text in PREP_KEYWORDS:
            prep_terms.append(token.text)
        elif token.pos_ in {"NOUN", "PROPN", "ADJ"} and token.text not in PREP_KEYWORDS:
            ingredient_terms.append(token.text)

    # Combine preparation from hyphen part if present
    if extra_prep:
        prep_terms.append(extra_prep)

    ingredient = " ".join(ingredient_terms).strip()
    preparation = " | ".join(prep_terms) if prep_terms else None

    return pd.Series([ingredient, unit, quantity, preparation])

recipes_filtered = recipes[recipes["recipe_name"].isin(recipes_wanted)].copy()
recipes_filtered = recipes_filtered.assign(ingredient_list=recipes_filtered["ingredients"].str.split(","))
recipes_filtered = recipes_filtered.explode("ingredient_list")
recipes_filtered["ingredient_list"] = recipes_filtered["ingredient_list"].str.strip()

recipes_filtered[["cleaned_ingredients", "units", "quantity", "preparation_notes"]] = (
    recipes_filtered["ingredient_list"].apply(parse_ingredient)
)

final_df = recipes_filtered[["Unnamed: 0", "recipe_name", "prep_time", "cook_time",	"total_time", "servings", 
                             "yield", "cleaned_ingredients", "units", "quantity", "preparation_notes", "directions", 
                             "rating", "url", "cuisine_path", "nutrition", "timing", "img_src"]]

recipes_filtered.to_csv(export_path_raw, index=False)
final_df.to_csv(export_path, index=False)
print("Filtered Recipes exported")
