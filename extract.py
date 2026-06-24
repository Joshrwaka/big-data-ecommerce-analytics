import json

with open('../dataset_generator.py', 'r') as f:
    nb = json.load(f)

code = ''
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        code += ''.join(cell['source']) + '\n\n'

with open('dataset_generator_clean.py', 'w') as f:
    f.write(code)

print('Done!')