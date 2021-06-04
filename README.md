# coco-to-pascal-voc
A script to convert coco-formatted annotations to pascal-voc annotations

This assumes that your coco bounding box annotations take the 
format of `xmin, ymin, xmax, ymax`, ie: 

`{'id': 1, 'image_id': 0, 'bbox': [xmin, ymin, xmax, ymax], 'area': 57546.363400432514, 'iscrowd': 0, 'category_id': 2, 'segmentation': []}`

# Usage:
Change the variables `COCO_DATA_IMAGES, COCO_DATA_ANNOTATIONS`, and `OUTPUT_ZIP_NAME` in `main.py` to suit your needs, then run `python main.py`. No special python packages are required.