


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
# from selenium.webdriver import PhantomJS
import numpy
from selenium.webdriver.firefox.options import Options
from PIL import Image
from io import BytesIO
import warnings
import json
import os

def warn(*args, **kwargs):
    pass

warnings.warn = warn
import cv2




def html_to_img(driver,html_content,outimgpath,id_count,max_height,max_width, id_same_cells):
    # opts = Options()
    # opts.set_headless()
    # assert opts.headless
    # #driver=PhantomJS()
    # driver = Firefox(options=opts)
    # driver.get("data:text/html;charset=utf-8," + html_content)
    html_file = os.getcwd() + "//" + html_content 
    driver.get('file:///'+html_file)

    #driver.execute_script("document.write('{}')".format(json.dumps(htmlcode)))
    # print(driver)
    window_size=driver.get_window_size()
    max_height,max_width=window_size['height'],window_size['width']
    element = WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, '1')))

    WebDriverWait(driver, 500).until(EC.visibility_of(element))

    png = driver.get_screenshot_as_png()

    im = Image.open(BytesIO(png))
    width,height=im.size
    bboxes=[]
    bboxes_cell = []
    open_cv_image = numpy.array(im) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    # for id in range(id_count):
    for list_id in id_same_cells:
        xmin_,ymin_,xtg_,ytg_,xmax_,ymax_ = 10000,10000,0,0,0,0
        for id in list_id:
            
            e = driver.find_element_by_id(str(id))
            txt=e.text.strip()
            lentext=len(txt)
            loc = e.location
            # print("loc", loc)
            size_ = e.size
            xmin = loc['x']
            ymin = loc['y']
            xmax = int(size_['width'] + xmin)
            ymax = int(size_['height'] + ymin)
            if xmin_> xmin:
                xmin_ = xmin
            if ymin_>ymin:
                ymin_ = ymin
            if xmax_< xmax:
                xmax_ = xmax
            if ymax_< ymax:
                ymax_ = ymax

        bboxes.append([lentext,txt,xmin_,ymin_,xmax_,ymax_])
        cv2.rectangle(open_cv_image,(xmin_,ymin_),(xmax_,ymax_),(0,0,255),2)

    rows = driver.find_elements_by_tag_name("tr")
    for row_index, row in enumerate(rows, start=1): 
        cells = row.find_elements_by_tag_name("td")
        for column_index, cell in enumerate(cells):
            loc = cell.location
            # print("loc",loc)
            size_ = cell.size
            xmin = loc['x']
            ymin = loc['y']
            xmax = int(size_['width'] + xmin)
            ymax = int(size_['height'] + ymin)
            # x_center, y_center, w, h = convert_topleftbottomright2yolo([xmin,ymin,xmax,ymax],max_width,max_height)
            bboxes_cell.append([xmin, ymin, xmax, ymax])
            # cv2.rectangle(open_cv_image,(xmin,ymin),(xmax,ymax),(0,0,255),2)

        cells = row.find_elements_by_tag_name("th")
        for column_index, cell in enumerate(cells):
            loc = cell.location
            # print("loc",loc)
            size_ = cell.size
            xmin = loc['x']
            ymin = loc['y']
            xmax = int(size_['width'] + xmin)
            ymax = int(size_['height'] + ymin)
            bboxes_cell.append([xmin, ymin, xmax, ymax])
            # x_center, y_center, w, h = convert_topleftbottomright2yolo([xmin,ymin,xmax,ymax],max_width,max_height)

            # cv2.rectangle(open_cv_image,(xmin,ymin),(xmax,ymax),(0,0,255),2)
    x_min, y_min, x_max, y_max = 10000,10000,0,0
    for coordinate in bboxes_cell:
        if x_min>coordinate[0]:
            x_min = coordinate[0]
        if y_min>coordinate[1]:
            y_min = coordinate[1]
        
        if x_max<coordinate[2]:
            x_max = coordinate[2]
        if y_max<coordinate[3]:
            y_max = coordinate[3]
    
    cv2.rectangle(open_cv_image,(x_min,y_min),(x_max,y_max),(0,0,255),2)
        
    # cv2.imwrite(outimgpath[:-4]+"box"+outimgpath[-4:], open_cv_image)
    im = im.crop((0,0, max_width, max_height))

    # im.save(outimgpath,dpi=(600,600))
    im.save(outimgpath)

    return im,bboxes, bboxes_cell

    # try:
    #     driver.get("data:text/html;charset=utf-8," + html_content)
    #     #driver.execute_script("document.write('{}')".format(json.dumps(htmlcode)))

    #     element = WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, '1')))

    #     WebDriverWait(driver, 500).until(EC.visibility_of(element))


    #     bboxes=[]
    #     for id in range(id_count):
    #         e = driver.find_element_by_id(str(id))
    #         txt=e.text.strip()
    #         lentext=len(txt)
    #         loc = e.location
    #         size_ = e.size
    #         xmin = loc['x']
    #         ymin = loc['y']
    #         xmax = int(size_['width'] + xmin)
    #         ymax = int(size_['height'] + ymin)
    #         bboxes.append([lentext,txt,xmin,ymin,xmax,ymax])
    #         # cv2.rectangle(im,(xmin,ymin),(xmax,ymax),(0,0,255),2)

    #     png = driver.get_screenshot_as_png()

    #     im = Image.open(BytesIO(png))
    #     width,height=im.size

    #     im = im.crop((0,0, max_width, max_height))

    #     im.save(outimgpath,dpi=(600,600))
    #     return im,bboxes

    # except:
    #     raise Exception()