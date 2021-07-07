import os
import shutil
import json
import glob
import re
import cv2
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import xml.etree.ElementTree as ET

from templates import xml_template, object_template

# Edit these
COCO_DATA_IMAGES = "./coco/images"
COCO_DATA_ANNOTATIONS = "./coco/annotations/2classes_test.json"
OUTPUT_ZIP_NAME = "sample_voc_output"

def prepare_output_dirs():

    for folder in ["JPEGImages", "Annotations"]:
        path = os.path.join("output", OUTPUT_ZIP_NAME, folder)
        if os.path.exists(path):
            shutil.rmtree(path)

        os.makedirs(path)


def resize_images_and_adjust_bounding_boxes(images_dir,
                                            annotations_dir,
                                            imsize=(608, 608)):

    imwidth = imsize[0]
    imheight = imsize[1]

    imsize_as_dict = {"height": imheight, "width": imwidth}

    for f in os.listdir(annotations_dir):
        print(f)
        image_fpath_matches = glob.glob(os.path.join(images_dir,os.path.splitext(f)[0] + ".*"))
        assert len(image_fpath_matches) == 1  # This should never throw, if it does then we need to patch

        image_fpath = image_fpath_matches[0]
        annotation_fpath = os.path.join(annotations_dir, f)

        image = cv2.imread(image_fpath)
        og_imshape = image.shape[:2]

        tree = ET.parse(os.path.join(annotations_dir, f))

        tree.find("size/width").text = str(imwidth)
        tree.find("size/height").text = str(imheight)

        objects = tree.findall("object")
        objects_and_bbs = {}
        bboxes = []
        for obj_num, obj in enumerate(objects):
            bbs = obj.find("bndbox")
            xmin = float(bbs[0].text)
            ymin = float(bbs[1].text)
            xmax = float(bbs[2].text)
            ymax = float(bbs[3].text)
            objects_and_bbs[obj_num] = obj
            bboxes.append(
                BoundingBox(x1=xmin, y1=ymin, x2=xmax, y2=ymax, label=obj_num))

        bbs_for_augment = BoundingBoxesOnImage(bboxes, og_imshape)
        seq = iaa.Resize(size=imsize_as_dict)
        image_resized, bbs_augmented = seq(image=image,
                                           bounding_boxes=bbs_for_augment)

        for bb_aug in bbs_augmented:
            overwrite_object = objects_and_bbs[bb_aug.label]

            overwrite_object.find("bndbox/xmin").text = str(bb_aug.x1)
            overwrite_object.find("bndbox/ymin").text = str(bb_aug.y1)
            overwrite_object.find("bndbox/xmax").text = str(bb_aug.x2)
            overwrite_object.find("bndbox/ymax").text = str(bb_aug.y2)

        tree.write(annotation_fpath)
        cv2.imwrite(image_fpath, image_resized)


def create_pascal_voc_package(data):
    image_data = data["images"]
    category_data = data["categories"]
    annotation_data = data["annotations"]

    labelmap = {c["id"]: c["name"] for c in category_data}
    imagemap = {d["id"]: {"fname": d["file_name"], "w": d["width"], "h": d["height"]} \
        for d in image_data}

    for i, (image_id, image_data) in enumerate(imagemap.items()):
        object_str = ""
        delete_indices = []

        for j, k in enumerate(annotation_data):
            if k["image_id"] == image_id:
                one_image_anno = annotation_data[j]
                delete_indices.append(j)

                x_min = one_image_anno["bbox"][0]
                y_min = one_image_anno["bbox"][1]
                width = one_image_anno["bbox"][2]
                height = one_image_anno["bbox"][3]

                if labelmap[one_image_anno["category_id"]] != "person":
                    break

                object_str += object_template.format(
                    labelmap[one_image_anno["category_id"]],
                    x_min,
                    y_min,
                    x_min + width,
                    y_min + height
                )

        # Modify the image fname to replace excess "." with -
        split_path = os.path.splitext(image_data["fname"])
        target_basename = split_path[0]
        target_basename = re.sub('[^0-9a-zA-Z]+', '_', target_basename)
        og_image_extension = split_path[-1]
        out_image = target_basename + og_image_extension
        out_anno = target_basename + ".xml"

        xml_annotation = xml_template.format(out_image, image_data["w"], image_data["h"], object_str)

        # Refines the list after extracting relevant annotations
        annotation_data = [a for i, a in enumerate(annotation_data) if i not in delete_indices]

        image = os.path.join(COCO_DATA_IMAGES, image_data["fname"])
        if not os.path.exists(image):
            print("No image for the particular annotation")
            continue

        with open(os.path.join("output", OUTPUT_ZIP_NAME, "Annotations", out_anno), "w+") as f:
            f.write(xml_annotation)

        print(f"Successfully converted {os.path.basename(image)}")
        shutil.copy(image, os.path.join("output", OUTPUT_ZIP_NAME, "JPEGImages", out_image))


if __name__ == "__main__":

    prepare_output_dirs()

    with open(COCO_DATA_ANNOTATIONS) as f:
        data = json.load(f)

    create_pascal_voc_package(data)
    resize_images_and_adjust_bounding_boxes(images_dir=f"./output/{OUTPUT_ZIP_NAME}/JPEGImages",
                                            annotations_dir=f"./output/{OUTPUT_ZIP_NAME}/Annotations")
    # shutil.make_archive(OUTPUT_ZIP_NAME, "zip", os.path.join("output", OUTPUT_ZIP_NAME))




