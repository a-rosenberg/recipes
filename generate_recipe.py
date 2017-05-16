import os
import json
from load_recipe import RecipeSlurper

recipe = {
    'name': 'name',
    'cook_time': 'cook_time',
    'subtitle': 'subtitle',
    'instructions': 'instructions',
    'notes': 'notes',
    'ingredients': []
}

recipe['name'] = raw_input('recipe name?: ')
recipe['cook_time'] = raw_input('cook time? (min): ')

while True:
    entry = {
        'ingredient': 'ingredient',
        'quantity': 'quantity',
        'unit': 'unit',
        'preparation': 'preparation'
    }
    entry['ingredient'] = raw_input('ingredient name?: ')
    entry['quantity'] = float(raw_input('quantity?: '))
    entry['unit'] = raw_input('unit?: ')
    entry['prep'] = raw_input('preparation?: ')
    recipe['ingredients'].append(entry)
    more = raw_input('more ingredients? (y/n):')
    if more.strip().lower() == 'n':
        break

recipe['instructions'] = raw_input('instructions?: ')
recipe['notes'] = raw_input('notes?: ')


save_name = ''.join([x.lower() for x in recipe.get('name').strip().split()])
save_path = os.path.join('recipes', save_name + '.json')
with open(save_path, 'w') as fid:
    fid.write(json.dumps(recipe, indent=2))

# rload = RecipeSlurper(save_path, database='cookbook.db')
# rload.insert()
# rload.cursor.execute('select * from recipes;')
# for i in rload.cursor.fetchall(): print i
