# coco-to-pascal-voc
A script to convert coco-formatted annotations to pascal-voc annotations

This assumes that your coco bounding box annotations take the 
format of `xmin, ymin, width, height`, per coco standard.

The output xml bbox coordinates are in the format `xmin ymin xmax ymax`

# Usage:
Change the variables `COCO_DATA_IMAGES, COCO_DATA_ANNOTATIONS`, and `OUTPUT_ZIP_NAME` in `main.py` to suit your needs, then run `python main.py`. No special python packages are required.

To check the results, run `sanity_check.py` which will populate the folder `output/sanity_check` with 
images overlaid with the translated bounding boxes found in the xmls. This provide a method 
of visual inspection to ensure that results are as expected.