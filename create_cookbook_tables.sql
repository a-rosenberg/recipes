-- First drop tables (remove if from new)
DROP TABLE recipes;

DROP TABLE recipes_ingredients;

DROP TABLE ingredients;

DROP TABLE instructions;
--

CREATE TABLE recipes (
    recipe_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subtitle TEXT NOT NULL,
    date_added TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    cook_time INTEGER NOT NULL
);

CREATE TABLE recipes_ingredients (
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    unit TEXT,
    preparation TEXT,
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
    FOREIGN KEY (ingredient_id) REFERENCES recipes(ingredient_id)
);

CREATE TABLE ingredients (
    ingredient_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ingredient TEXT NOT NULL,
    category TEXT
);

CREATE TABLE instructions (
    recipe_id INTEGER NOT NULL PRIMARY KEY,
    instructions BLOB NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);