from pycocotools.coco import COCO
import shutil
import os
import random
from PIL import Image

# Paths to COCO annotations and images
annotation_file = 'D:/Main project/project/FramePainter/annotations/instances_train2017.json'
image_dir = 'D:/Main project/project/FramePainter/train2017'
output_dir = 'path/to/reduced_coco/'

# Create output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load COCO annotations
coco = COCO(annotation_file)
categories = coco.getCatIds()
selected_images = set()

# Calculate images per category
images_per_category = 1000 // len(categories)

# Collect unique image IDs from all categories
for cat_id in categories:
    img_ids = coco.getImgIds(catIds=[cat_id])
    random.shuffle(img_ids)
    selected_images.update(img_ids[:images_per_category])

# Copy and resize selected images to output directory
for img_id in selected_images:
    img_info = coco.loadImgs(img_id)[0]
    img_path = os.path.join(image_dir, img_info['file_name'])
    output_path = os.path.join(output_dir, img_info['file_name'])

    try:
        with Image.open(img_path) as img:
            resized_img = img.resize((1024, 576))
            resized_img.save(output_path)
        print(f"Processed and saved: {output_path}")
    except Exception as e:
        print(f"Error processing {img_path}: {e}")

print(f"Reduced dataset saved to {output_dir} with {len(selected_images)} images.")
