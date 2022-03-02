# get a list of all the files to 
import os
import glob
from PIL import Image
from selenium import webdriver 
from PIL import Image
from io import BytesIO
import numpy

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
from TableGeneration.tools import *

import shutil


glob_folder = os.path.join("/Users/tuananh/Downloads/TIES_DataGeneration/gentables/html/", '*.html')

html_file_list = glob.glob(glob_folder)
opts = Options()

opts.set_headless()
assert opts.headless

driver = Firefox(options=opts)

from tqdm import tqdm

for html_file in tqdm(html_file_list):
    text_file = html_file.replace("html", "txt")
    file_name = html_file.split("/")[-1].replace(".html", ".png")
    shutil.copy(text_file, "/Users/tuananh/Downloads/TIES_DataGeneration/private_test/txt/")
    shutil.copy(html_file, "/Users/tuananh/Downloads/TIES_DataGeneration/private_test/html/")
    # get the name into the right format
    temp_name = "file://" + html_file
    # The above line could be substituted for these 3 lines, 
    # which would prevent the webpage from opening first
    ###########
    driver.get(temp_name)
    
    window_size=driver.get_window_size()
    max_height,max_width=window_size['height'],window_size['width']
    max_height = 615
    element = WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, '1')))

    WebDriverWait(driver, 500).until(EC.visibility_of(element))

    png = driver.get_screenshot_as_png()

    im = Image.open(BytesIO(png))
    width,height=im.size
    bboxes=[]
    open_cv_image = numpy.array(im) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    im = im.crop((0,0, max_width, max_height))

    # im.save(outimgpath,dpi=(600,600))
    im.save(f"/Users/tuananh/Downloads/TIES_DataGeneration/private_test/images/{file_name}")


# import cv2

# path_image = "/Users/tuananh/Downloads/TIES_DataGeneration/test_image/images/dashed_table_4.png"
# path_txt = "/Users/tuananh/Downloads/TIES_DataGeneration/test_image/txt/dashed_table_4.txt"

# data = open(path_txt, "r").read().split("\n")
# image = cv2.imread(path_image)
# for box in data:
#     box = box.split(",")
#     if box[0] == "":
#         continue
#     box = list(map(int, box))
#     cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), thickness=2, color=(0, 255, 0))
# cv2.imshow("image", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()