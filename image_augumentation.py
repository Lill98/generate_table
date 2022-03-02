from cgitb import text
import os
import glob
import albumentations as A
import cv2
from tqdm import tqdm
import shutil
import random

# Declare an augmentation pipeline
dictionary_pixel_base = {
    "Blur": A.Blur(blur_limit=7, always_apply=True, p=1),
    "CLAHE": A.CLAHE(always_apply=True, p=1),
    # "ChannelDropout": A.ChannelDropout(always_apply=True, p=1),
    "Emboss": A.Emboss(always_apply=True, p=1),
    "GaussNoise": A.GaussNoise(always_apply=True, p=1, var_limit=500),
    "GaussianBlur": A.GaussianBlur(always_apply=True, p=1),
    # "HueSaturationValue": A.HueSaturationValue(always_apply=True, p=1),
    "MotionBlur": A.MotionBlur(always_apply=True, p=1, blur_limit=15),
    "RGBShift": A.RGBShift(always_apply=True, p=1),
    "RandomBrightnessContrast": A.RandomBrightnessContrast(always_apply=True, p=1, brightness_limit=0.1),
    "RandomSnow": A.RandomSnow(always_apply=True, p=1),
    "Sharpen": A.Sharpen(always_apply=True, p=1),
}

# Declare an augmentation pipeline
dictionary_pixel_tranform = {
    # "Affine": A.Affine(always_apply=True, p=1, fit_output=True),
    "Perspective": A.Perspective(always_apply=True, p=1, fit_output=True),
    # "PiecewiseAffine": A.PiecewiseAffine(always_apply=True, p=1, nb_cols=1, nb_rows=1),
}

def augumentation_without_bounding_box(image_paths, folder_save_parent):

    seed = [i for i in range(1, len(dictionary_pixel_base) + 1)]

    for index, augumentation_type in enumerate(dictionary_pixel_base):
        folder_save = folder_save_parent + augumentation_type
        if not os.path.isdir(folder_save):
            os.makedirs(folder_save)
        if not os.path.isdir(folder_save + "/html/"):
            os.makedirs(folder_save + "/html/")
        if not os.path.isdir(folder_save + "/images/"):
            os.makedirs(folder_save + "/images/")
        if not os.path.isdir(folder_save + "/txt/"):
            os.makedirs(folder_save + "/txt/")
        
        random.seed(seed[index])
        image_paths_ = random.sample(image_paths, 300)

        for image_path in tqdm(image_paths_):
            image = cv2.imread(image_path)

            name = image_path.split("/")[-1].split(".")[0].replace("dashed_table", f"dashed_table_{augumentation_type}")
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            transform = A.Compose([
                dictionary_pixel_base[augumentation_type]
            ])
            transformed = transform(image=image)
            transformed_image = transformed["image"]
            html_path = image_path.replace("images", "html").replace(".png", ".html")
            text_path = image_path.replace("images", "txt").replace(".png", ".txt")

            shutil.copy(html_path, folder_save + "/html/" + name + ".html")
            shutil.copy(text_path, folder_save + "/txt/" + name + ".txt")
            cv2.imwrite(folder_save + "/images/" + name + ".png", transformed_image)
    
    return None


def augumentation_with_bounding_box(image_paths, folder_save_parent):
    seed = [i for i in range(1, len(dictionary_pixel_tranform) + 1)]
    for index, augumentation_type in enumerate(dictionary_pixel_tranform):
        
        folder_save = folder_save_parent + augumentation_type
        if not os.path.isdir(folder_save):
            os.makedirs(folder_save)
        if not os.path.isdir(folder_save + "/html/"):
            os.makedirs(folder_save + "/html/")
        if not os.path.isdir(folder_save + "/images/"):
            os.makedirs(folder_save + "/images/")
        if not os.path.isdir(folder_save + "/txt/"):
            os.makedirs(folder_save + "/txt/")
        
        random.seed(seed[index])
        image_paths_ = random.sample(image_paths, 300)
        
        for image_path in tqdm(image_paths_):
            html_path = image_path.replace("images", "html").replace(".png", ".html")
            text_path = image_path.replace("images", "txt").replace(".png", ".txt")
            name = image_path.split("/")[-1].split(".")[0].replace("dashed_table", f"dashed_table_{augumentation_type}")

            image = cv2.imread(image_path)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            data = open(text_path, "r").read().split("\n")[:-1]
            bboxes = []
            class_labels = []
            for box in data:
                box = list(map(int, box.split(",")))
                x_min = box[0]
                y_min = box[1]
                w = box[2] - box[0]
                h = box[3] - box[1]
                bboxes.append([x_min, y_min, w, h])
                class_labels.append("cell")

            transform = A.Compose([
                dictionary_pixel_tranform[augumentation_type]
            ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

            transformed = transform(image=image, bboxes=bboxes, class_labels=class_labels)
            transformed_image = transformed["image"]
            transformed_bboxes = transformed['bboxes']
            boxes_str = ""
            for box in transformed_bboxes:
                box = list(map(int, box))
                # cv2.rectangle(transformed_image, (box[0], box[1]), (box[2]+box[0], box[3]+box[1]), thickness=2, color=(0, 255, 0))
                box = [box[0], box[1], box[2]+box[0], box[3]+box[1]]
                boxes_str += ",".join(list(map(str, box))) + "\n"
            
            boxes_str = boxes_str[:-1]

            file_txt_write = open(folder_save + "/txt/" + name + ".txt", "w")
            file_txt_write.write(boxes_str)
            file_txt_write.close()

            shutil.copy(html_path, folder_save + "/html/" + name + ".html")
            cv2.imwrite(folder_save + "/images/" + name + ".png", transformed_image)
    
    return None


if __name__ == "__main__":
    numbers = ["1", "2", "3", "4", "5"]
    
    for number in numbers:
        type_folder = f"test_image_bg_{number}"

        path_folder = f"/Users/tuananh/Downloads/TIES_DataGeneration/data_synthesize/dash-line-table/{type_folder}/images/*.png"
        path_folder_save = f"/Users/tuananh/Downloads/TIES_DataGeneration/data_synthesize/augumentation_dash_line_table/{type_folder}/"
        if not os.path.isdir(path_folder_save):
            os.makedirs(path_folder_save)

        image_paths = glob.glob(path_folder)

        augumentation_without_bounding_box(image_paths, path_folder_save)
        augumentation_with_bounding_box(image_paths, path_folder_save)
