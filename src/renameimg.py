import os

input_dir = 'dataset1_robowflow'

for folder in os.listdir(input_dir):
  if folder == '.DS_Store':
     continue
  i = 1
  for file in os.listdir(os.path.join(input_dir, folder)):
      if file == '.DS_Store':
        continue
      path = os.path.join(input_dir, folder)
      img_path = os.path.join(path, file)
      new_name = folder + str(i) + '.jpg'
      new_path = os.path.join(path, new_name)
      img_new = os.rename(img_path, new_path)
      i += 1
      print(new_name)