import sqlite3
import json

class RecipeSlurper:
    def __init__(self, target, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.data = json.load(open(target))

    def insert(self):
        name = self.data.get('name')
        subtitle = self.data.get('subtitle')
        cook_time = self.data.get('cook_time')
        instructions = self.data.get('instructions').replace('"', '\"')
        notes = self.data.get('notes')

        # recipe table
        self.cursor.execute("INSERT INTO recipes "
                            "(name, subtitle, notes, cook_time) "
                            "VALUES "
                            "(?, ?, ?, ?);",
                            (name, subtitle, notes, cook_time))


        self.cursor.execute("SELECT last_insert_rowid() ")
        recipe_id = self.cursor.fetchone()[0]

        self.cursor.execute("INSERT INTO "
                            "instructions "
                            "(recipe_id, instructions) "
                            "VALUES "
                            "(?, ?);",
                            (recipe_id, instructions))

        # ingredient table
        for item in self.data.get('ingredients'):
            ingredient = item.get('ingredient')
            quantity = item.get('quantity')
            unit = item.get('unit')
            preparation = item.get('preparation')

            self.cursor.execute("select ingredient_id from ingredients where ingredient = '{}';".format(ingredient))
            ingredient_test = self.cursor.fetchone()
            if ingredient_test:
                ingredient_id = ingredient_test[0]
            else:
                self.cursor.execute(
                    "INSERT INTO ingredients "
                    "(ingredient) "
                    "VALUES "
                    "('{}');"
                    .format(ingredient))
                self.cursor.execute("SELECT last_insert_rowid() ")
                ingredient_id = self.cursor.fetchone()[0]

            self.cursor.execute(
                "INSERT INTO recipes_ingredients "
                "(recipe_id, ingredient_id, quantity, unit, preparation) "
                "VALUES "
                "(?, ?, ?, ?, ?);",
                (recipe_id, ingredient_id, quantity, unit, preparation))




if __name__ == '__main__':
    # recipe = RecipeSlurper('./recipes/misobowl.json', database='cookbook.db')
    # recipe.insert()
    # recipe.connection.commit()

    # recipe = RecipeSlurper('./recipes/shakshuka.json', database='cookbook.db')
    # recipe.insert()
    # recipe.connection.commit()

    recipe = RecipeSlurper('./recipes/tamariavocadotoast.json', database='cookbook.db')
    # recipe.insert()
    # recipe.connection.commit()

    # recipe.cursor.execute("select r.name, i.ingredient, ri.quantity, ri.unit, ri.preparation "
    #                          "from recipes as r "
    #                          "natural join ingredients as i "
    #                          "natural join recipes_ingredients as ri;")
    # recipe.cursor.execute("select r.recipe_id, r.name, ri.quantity, ri.unit from recipes as r "
    #                       "natural join ingredients as i "
    #                       "natural join recipes_ingredients as ri "
    #                       "where i.ingredient = 'garlic';")
    # recipe.cursor.execute('SELECT name, cook_time FROM recipes WHERE cook_time < 60')
    recipe.cursor.execute("select ingredient_id, count(ingredient_id) "
                          "from recipes_ingredients "
                          "group by ingredient_id "
                          "having count(ingredient_id) > 1")
    for i in recipe.cursor.fetchall(): print i

    recipe.connection.close()