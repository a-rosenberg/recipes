import sqlite3
import json
import os

class RecipeSlurper:
    """Sluper to get serialized JSON recipe files into database"""
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()


    def insert(self, target):
        self.data = json.load(open(target))

        author_firstname = self.data.get('author_firstname').lower()
        author_lastname = self.data.get('author_lastname').lower()
        name = self.data.get('name')
        subtitle = self.data.get('subtitle')
        cook_time = self.data.get('cook_time')
        instructions = self.data.get('instructions').replace('"', '\"')
        notes = self.data.get('notes')

        # author table
        self.cursor.execute("select author_id from authors "
                            "where author_firstname = '{}' "
                            "AND author_lastname = '{}';".format(author_firstname, author_lastname))
        author_test = self.cursor.fetchone()
        if author_test:
            author_id = author_test[0]
        else:
            self.cursor.execute("INSERT INTO authors "
                                "(author_firstname, author_lastname) "
                                "VALUES "
                                "('{}', '{}');".format(author_firstname, author_lastname))
            self.cursor.execute("SELECT last_insert_rowid() ")
            author_id = self.cursor.fetchone()[0]

        # recipe table
        self.cursor.execute("INSERT INTO recipes "
                            "(name, subtitle, notes, cook_time, author_id) "
                            "VALUES "
                            "(?, ?, ?, ?, ?);",
                            (name, subtitle, notes, cook_time, author_id))


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

            # recipe/ingredient junction table
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
    slurper = RecipeSlurper('cookbook.db')

    folder = 'recipes'
    for recipe in [os.path.join(folder, x) for x in os.listdir(folder) if x.endswith('.json')]:
        slurper.insert(recipe)

    # for i in recipe.execute("select r.name, i.ingredient "
    #                         "from recipes as r "
    #                         "natural join recipes_ingredients "
    #                         "natural join ingredients as i "
    #                         "where r.name = 'turkey bacon scramble';"): print i
    # for i in slurper.execute("select r.name from recipes as r "
    #                         "natural join recipes_ingredients "
    #                         "natural join ingredients as i "
    #                         "where i.ingredient = 'egg';"): print i
    for i in slurper.execute('select a.author_firstname, a.author_lastname, r.name from recipes as r'
                             ' natural join authors as a;'): print i

    # sluper.commit()
    slurper.close()