import os 
import shutil 
import json 
import glob 

from templates import xml_template, object_template

# Edit these
COCO_DATA_IMAGES = "./coco/<image-folder>"
COCO_DATA_ANNOTATIONS = "./coco/<annotations-json>.json"
OUTPUT_ZIP_NAME = "sample_voc_output"

def prepare_output_dirs():

    for folder in ["JPEGImages", "Annotations"]:
        path = os.path.join("output", OUTPUT_ZIP_NAME, folder)
        if os.path.exists(path):
            shutil.rmtree(path)
        
        os.makedirs(path)


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

                object_str += object_template.format(
                    labelmap[one_image_anno["category_id"]],
                    x_min,
                    y_min, 
                    x_min + width, 
                    y_min + height
                )


        xml_annotation = xml_template.format(
            image_data["fname"], image_data["w"], image_data["h"], object_str)

        # Refines the list after extracting relevant annotations
        annotation_data = [a for i, a in enumerate(annotation_data) if i not in delete_indices]

        image = os.path.join(COCO_DATA_IMAGES, image_data["fname"])
        if not os.path.exists(image):
            print("No image for the particular annotation")
            continue 

        with open(os.path.join(
            "output", OUTPUT_ZIP_NAME, "Annotations", os.path.splitext(image_data["fname"])[0] + ".xml"), "w+") \
                as f:
            f.write(xml_annotation)
        
        print(f"Successfully converted {os.path.basename(image)}")
        shutil.copy(image, os.path.join("output", OUTPUT_ZIP_NAME, "JPEGImages", image_data["fname"]))


if __name__ == "__main__":

    prepare_output_dirs()

    with open(COCO_DATA_ANNOTATIONS) as f:
        data = json.load(f)
        
    create_pascal_voc_package(data)
    shutil.make_archive(OUTPUT_ZIP_NAME, "zip", os.path.join("output", OUTPUT_ZIP_NAME))




