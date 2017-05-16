import json

recipe = {
    'author_firstname': 'firstname',
    'author_lastname': 'lastname',
    'name': 'name',
    'cook_time': 'cook_time',
    'subtitle': 'subtitle',
    'instructions': 'instructions',
    'notes': 'notes',
    'ingredients': [
        {
            'ingredient': 'ingredient',
            'quantity': 'quantity',
            'unit': 'unit',
            'preparation': 'preparation'
        }
    ]
}

with open('templates/template.json', 'w') as template:
    template.write(json.dumps(recipe, indent=2))