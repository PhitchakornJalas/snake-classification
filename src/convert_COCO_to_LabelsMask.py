import json
import numpy as np
import skimage
import tifffile
import os
import shutil
from pycocotools import mask as maskUtils

def create_mask(image_info, annotations, output_folder):
  # Create an empty mask as a numpy array
  mask_np = np.zeros((image_info['height'], image_info['width']), dtype=np.uint16)

  # Counter for the object number
  object_number = 1

  for ann in annotations:
    if ann['image_id'] == image_info['id']:
      rle = ann['segmentation']
      binary_mask = maskUtils.decode(rle)
      mask_np[binary_mask == 1] = object_number
      object_number += 1

      # Extract segmentation polygon
      # for seg in ann['segmentation']:
        # Convert polygons to a binary mask and add it to the main mask
        # rr, cc = skimage.draw.polygon(seg[1::2], seg[0::2], mask_np.shape)
        # mask_np[rr, cc] = object_number
        # object_number += 1 #We are assigning each object a unique integer value (labeled mask)

  # Save the numpy array as a TIFF using tifffile library
  # mask_path = os.path.join(output_folder, image_info['file_name'].replace('.tif', '_mask.tif'))
  mask_path = os.path.join(output_folder, image_info['file_name'].replace('.jpg', '.jpg'))
  tifffile.imsave(mask_path, mask_np)

  print(f"Saved mask for {image_info['file_name']} to {mask_path}")


def main(json_file, mask_output_folder, image_output_folder, original_image_dir):
  # Load COCO JSON annotations
  with open(json_file, 'r') as f:
    data = json.load(f)

  images = data['images']
  annotations = data['annotations']

  # Ensure the output directories exist
  if not os.path.exists(mask_output_folder):
    os.makedirs(mask_output_folder)
  if not os.path.exists(image_output_folder):
    os.makedirs(image_output_folder)

  for img in images:
    # Create the masks
    create_mask(img, annotations, mask_output_folder)
    
    # Copy original images to the specified folder
    original_image_path = os.path.join(original_image_dir, img['file_name'])

    new_image_path = os.path.join(image_output_folder, os.path.basename(original_image_path))
    shutil.copy2(original_image_path, new_image_path)
    print(f"Copied original image to {new_image_path}")


if __name__ == '__main__':
  # Train
  original_image_dir = 'v1coco-segmentation/train' 
  json_file = 'v1coco-segmentation/train/snake_coco_train.json'
  mask_output_folder = 'v1coco-segmentation-maskLebels/train/masks'
  image_output_folder = 'v1coco-segmentation-maskLebels/train/images' 

  # Valid
  # original_image_dir = 'v1coco-segmentation/valid'
  # json_file = 'v1coco-segmentation/valid/snake_coco_val.json'
  # mask_output_folder = 'v1coco-segmentation-maskLebels/val/masks' 
  # image_output_folder = 'v1coco-segmentation-maskLebels/val/images'

  # Test
  # original_image_dir = 'v1coco-segmentation/test'
  # json_file = 'v1coco-segmentation/test/snake_coco_test.json'
  # mask_output_folder = 'v1coco-segmentation-maskLebels/test/masks'
  # image_output_folder = 'v1coco-segmentation-maskLebels/test/images'

  main(json_file, mask_output_folder, image_output_folder, original_image_dir)