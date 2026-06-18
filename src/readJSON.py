import json

with open('v1coco-segmentation/test/snake_coco_test.json', 'r') as file:
  data = json.load(file)

def print_filename(d):
  for img in data['images'][:10]:
    print(img['file_name'])

def print_structure(d, indent=0):
  if isinstance(d, dict):
    for key, value in d.items():
      print(' ' * indent + str(key))
      print_structure(value, indent+1)
  elif isinstance(d, list):
    print(' ' * indent + '[list of length {} containing:]'.format(len(d)))
    if d:
      print_structure(d[0], indent+1)
    
print_structure(data)