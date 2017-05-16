import sqlite3
import json

class RecipeSlurper:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()


    def insert(self, target):
        self.data = json.load(open(target))

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

    def execute(self, sql):
        cursor = self.cursor
        cursor.execute(sql)
        return cursor.fetchall()

    def commit(self):
        connection = self.connection
        connection.commit()

    def close(self):
        connection = self.connection
        connection.close()


if __name__ == '__main__':
    recipe = RecipeSlurper('cookbook.db')
    recipe.insert('./recipes/tamariavocadotoast.json')
    print recipe.execute('select * from recipes;')[0]
    recipe.close()