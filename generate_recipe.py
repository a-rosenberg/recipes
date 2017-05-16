import os
import json

recipe = {
    'name': 'name',
    'cook_time': 'cook_time',
    'subtitle': 'subtitle',
    'instructions': 'instructions',
    'notes': 'notes',
    'author_firstname': 'author_firstname',
    'author_lastname': 'author_lastname',
    'ingredients': []
}

recipe['author_firstname'] = raw_input('author first name?: ').lower()
recipe['author_lastname'] = raw_input('author last name?: ').lower()
recipe['name'] = raw_input('recipe name?: ')
recipe['subtitle'] = raw_input('subtitle?: ')
recipe['cook_time'] = raw_input('cook time? (min): ')

while True:
    entry = {
        'ingredient': 'ingredient',
        'quantity': 'quantity',
        'unit': 'unit',
        'preparation': 'preparation'
    }
    entry['ingredient'] = raw_input('ingredient name?: ').lower()
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
save = raw_input("save to '{save_path}'? (y/n): ".format(save_path=save_path))

if save.strip().lower() == 'y':
    with open(save_path, 'w') as fid:
        fid.write(json.dumps(recipe, indent=2))