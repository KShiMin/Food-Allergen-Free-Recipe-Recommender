-- enable enforcement of foreign key constraints in SQLite
PRAGMA foreign_keys = ON;   

CREATE TABLE IF NOT EXISTS user_profile (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    user_password TEXT NOT NULL,
    height REAL,
    weight REAL,
    gender TEXT CHECK (gender IN ('male', 'female', 'prefer_not_to_say')),
    age INTEGER,
    caloric_budget INTEGER,
    dietary_preferences TEXT,
    activity_level TEXT CHECK (activity_level IN ('sedentary', 'light', 'moderate', 'active', 'very_active'))
);

CREATE TABLE IF NOT EXISTS allergen (
    allergen_id INTEGER PRIMARY KEY,
    allergen_name TEXT NOT NULL,
    allergen_description TEXT
);

CREATE TABLE IF NOT EXISTS user_allergen (
    user_id INTEGER NOT NULL,
    allergen_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, allergen_id),
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergen(allergen_id)
);

CREATE TABLE IF NOT EXISTS ingredient (
    ingredient_id TEXT PRIMARY KEY,
    ingredient_name TEXT NOT NULL,
    nutritional_info REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredient_allergen (
    allergen_id INTEGER NOT NULL,
    ingredient_id TEXT NOT NULL,
    PRIMARY KEY (allergen_id, ingredient_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);

CREATE TABLE IF NOT EXISTS ingredient_substitution (
    original_ingredient_id TEXT NOT NULL,
    substitute_ingredient_id TEXT NOT NULL,
    PRIMARY KEY (original_ingredient_id, substitute_ingredient_id),
    FOREIGN KEY (original_ingredient_id) REFERENCES ingredient(ingredient_id),
    FOREIGN KEY (substitute_ingredient_id) REFERENCES ingredient(ingredient_id)
);


INSERT INTO user_profile (user_name, user_password) VALUES ("Natalie", "password1");
INSERT INTO user_profile (user_name, user_password) VALUES ("Shi Min", "password2");

INSERT INTO allergen (allergen_id, allergen_name) VALUES (1, "Milk");
INSERT INTO allergen (allergen_id, allergen_name) VALUES (2, "Eggs");
INSERT INTO allergen (allergen_id, allergen_name) VALUES (3, "Fish");
INSERT INTO allergen (allergen_id, allergen_name) VALUES (4, "Crustacean Shellfish");
INSERT INTO allergen (allergen_id, allergen_name) VALUES (5, "Tree Nuts");
INSERT INTO allergen (allergen_id, allergen_name) VALUES (6, "Peanuts");
INSERT INTO allergen (allergen_id, allergen_name) VALUES (7, "Wheat");
INSERT INTO allergen (allergen_id, allergen_name) VALUES (8, "Soybean");
INSERT INTO allergen (allergen_id, allergen_name) VALUES (9, "Mustard");
INSERT INTO allergen (allergen_id, allergen_name) VALUES (10, "Celery");

INSERT INTO user_allergen (user_id, allergen_id) VALUES (1, 1);
INSERT INTO user_allergen (user_id, allergen_id) VALUES (1, 3);
INSERT INTO user_allergen (user_id, allergen_id) VALUES (2, 8);

INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("1145", "Butter", 717);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("9004", "Apple", 48);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("11282", "Onion", 40);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("O049", "Pork Chop", 178.772);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("2047", "Salt", 0);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("2023", "Black Pepper", 271);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("9020", "Apple Sauce", 42);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("19334", "Brown Sugar", 380);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("2046", "Mustard", 60);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("2010", "Cinnamon", 247);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("6700", "Vegetable Broth", 5);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("4053", "Olive Oil", 884);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("11291", "Green Onion", 32);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("20044", "Arborio Rice", 365);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("43154", "White Wine", 50);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("9089", "Figs", 74);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("P", "Prosciutto", 55);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("PRC", "Pecorino-Romano Cheese", 110);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("RO", "Red Onion", 40);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("9160", "Lime Juice", 25);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("9326", "Watermelon", 30);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("D044", "Baby Cucumbers", 17.447);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("1019", "Feta Cheese", 264);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("G016", "Mint Leaves", 37.045);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("15270", "Bay Shrimp", 85);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("9152", "Lemon Juice", 22);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("GS", "Garlic Salt", 1.2);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("PP", "Penne Pasta", 196);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("1032", "Parmesan Cheese", 420);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("1004", "Gorgonzola Cheese", 353);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("1053", "Whipping Cream", 340);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("E051", "Pear", 37.523);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("H021", "Walnuts", 671.351);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("E009", "Bananas", 110.657);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("19335", "White Sugar", 387);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("M001", "Egg", 134.796);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("20481", "All-Purpose Flour", 364);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("18372", "Baking Soda", 0);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("5061", "Chicken Breast", 184);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("9070", "Cherries", 63);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("11143", "Celery", 16);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("12142", "Pecans", 691);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("4018", "Mayonnaise", 250);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("1088", "Buttermilk", 40);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("1077", "Milk", 61);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("9156", "Lemon Zest", 47);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("LP", "Lemon Pepper", 1);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("19296", "Honey", 304);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("SXW", "Shaoxing Cooking Wine", 18);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("6175", "Hoisin Sauce", 220);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("9148", "Kiwi", 61);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("CDS", "Chinese Dark Soy Sauce", 8.5);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("6633", "Thai Chile Sauce", 79);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("G012", "Garlic", 122.846);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("6176", "Oyster Sauce", 51);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("C5P", "Chinese Five-spice Powder", 6.5);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("10860", "Pork Belly", 548);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("2075", "Taco Seasoning Mix", 322);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("4669", "Vegetable Oil", 884);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("G025", "Cumin", 304.486);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("6183", "Chicken Broth", 15);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("14555", "Water", 0);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("11527", "Tomatoes", 18);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("11165", "Cilantro", 23);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("CO", "Coconut Oil", 121);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("27034", "Mushroom Sauce", 53);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("MB", "Mushroom Broth", 13);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("16357", "Chickpea", 164);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("KOM", "King Oyster Mushroom", 40);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("QP", "Quinoa Pasta", 226);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("CC", "Coconut Cream", 68);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("15108", "Pumpkin Seeds", 89);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("A", "Aquafaba", 43);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("AF", "Almond Flour", 648);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("11205", "Cucumber", 15);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("12061", "Almonds", 579);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("1256", "Greek Yogurt", 59);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("1180", "Vegan Sour Cream", 74);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("12176", "Coconut Milk", 202);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("14106", "White Wine", 82);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("SS", "Soy Sauce", 8.5);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("CA", "Coconut Aminos", 6);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("6631", "Sriracha Sauce", 93);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("D077", "Zucchini noodles", 20.076);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("CF", "Coconut Flour", 28);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("12036", "Sunflower Seeds", 584);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("16161", "Silken Tofu (blended)", 55);
INSERT INTO ingredient (ingredient_id, ingredient_name, nutritional_info) VALUES ("FS", "Fish Sauce", 6.3);

INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (1, "1145");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (9, "2046");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (8, "6700");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (1, "PRC");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (1, "1019");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (4, "15270");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (2, "PP");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (7, "PP");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (1, "1032");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (1, "1004");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (1, "1053");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (5, "H021");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (2, "M001");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (7, "20481");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (10, "11143");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (5, "12142");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (2, "4018");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (1, "1088");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (1, "1077");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (7, "SXW");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (7, "6175");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (8, "6175");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (7, "CDS");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (8, "CDS");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (7, "6633");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (8, "6633");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (4, "6176");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (8, "16357");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (5, "16357");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (5, "A");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (5, "AF");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (5, "12061");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (1, "1256");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (8, "SS");
INSERT INTO ingredient_allergen (allergen_id, ingredient_id) VALUES (8, "16161");

INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("1145", "CO");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("2046", "27034");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("6700", "MB");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("6700", "6183");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("PRC", "16357");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("1019", "16357");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("15270", "KOM");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("PP", "QP");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("PP", "D077");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("1032", "16357");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("1004", "16357");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("1053", "CC");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("H021", "15108");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("M001", "A");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("M001", "9020");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("20481", "AF");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("20481", "CF");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("11143", "11205");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("12142", "12061");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("12142", "12036");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("4018", "1256");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("4018", "16161");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("1088", "1180");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("1077", "12176");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("SXW", "14106");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("6175", "SS");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("6175", "FS");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("CDS", "CA");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("6633", "6631");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("6176", "SS");
INSERT INTO ingredient_substitution (original_ingredient_id, substitute_ingredient_id) VALUES ("6176", "27034");
