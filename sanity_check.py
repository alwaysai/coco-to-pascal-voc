import os 
import random 
import glob 
import time
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

from main import OUTPUT_ZIP_NAME 

ROOT_DIR = os.path.join("output", OUTPUT_ZIP_NAME)

ann_dir = os.path.join(ROOT_DIR, "Annotations")
im_dir = os.path.join(ROOT_DIR, "JPEGImages")

annotations = sorted(os.listdir(ann_dir))
images = sorted(os.listdir(im_dir))

assert len(annotations) == len(images)
num_samples = len(annotations)

if __name__ == "__main__":
    for i in range(num_samples):

        image_fname = images[i]
        assert os.path.splitext(image_fname)[0] == \
            os.path.splitext(annotations[i])[0]


        with Image.open(os.path.join(im_dir, images[i])) as im:
            draw = ImageDraw.Draw(im)

            tree = ET.parse(os.path.join(ann_dir, annotations[i]))
            objects = tree.findall("object")
            
            for obj in objects:

                bbox = obj.find('bndbox')
                xmin = int(float(bbox.find('xmin').text))
                ymin = int(float(bbox.find('ymin').text))
                xmax = int(float(bbox.find('xmax').text))
                ymax = int(float(bbox.find('ymax').text))

                draw.rectangle((xmin, ymin, xmax, ymax), 
                    fill=None, outline=(0, 255, 0), width=3)

            im.save(f"output/sanity_check/{image_fname}")

