import pandas as pd
import spacy
import re

nlp = spacy.load("en_core_web_sm")

pd.set_option('display.max_colwidth', None)

recipes = pd.read_csv("recipes.csv")

recipes_wanted = ["Joy's Easy Banana Bread", "Pan-Fried Shrimp", "Refreshing Cucumber Watermelon Salad", 
                  "Applesauce Pork Chops", "Risotto with Fresh Figs and Prosciutto", "Gorgonzola Pear Pasta",
                 "Char Siu (Chinese Barbeque Pork)", "Cherry Chicken Salad", "Mexican Chicken Soup", 
                  "Fresh Fig and Prosciutto Pasta Sauce"]

def rmStopwords(text):
    doc = nlp(text)
    filtered_words = [ token.text for token in doc if (
        not token.is_stop and not token.is_punct and not token.like_num
    )]
    filtered_quantity = [token.text for token in doc if token.like_num]
    return ('|'.join(filtered_words), '|'.join(filtered_quantity))


recipes_filtered = recipes[recipes["recipe_name"].isin(recipes_wanted)]

recipes_filtered[["cleaned_ingredients", "quantity"]] = recipes_filtered["ingredients"].apply(rmStopwords).apply(pd.Series)

recipes_filtered.to_csv("filtered_recipes2.csv", index=False)
print("Filtered Recipes exported")