# coco-to-pascal-voc
A script to convert coco-formatted annotations to pascal-voc annotations

This assumes that your coco bounding box annotations take the 
format of `xmin, ymin, xmax, ymax`, ie: 

`{'id': 1, 'image_id': 0, 'bbox': [xmin, ymin, xmax, ymax], 'area': 57546.363400432514, 'iscrowd': 0, 'category_id': 2, 'segmentation': []}`
