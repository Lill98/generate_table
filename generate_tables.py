from TableGeneration.Distribution import Distribution
from TableGeneration.Table import Table
from multiprocessing import Process
import time
import random
import argparse
from TableGeneration.tools import *
import os
import pickle
import numpy as np
from tqdm import tqdm
from selenium.webdriver import Firefox, Chrome
import shutil
import tqdm as tqdm 

parser=argparse.ArgumentParser()

parser.add_argument('--imagespath',default='/Users/tuananh/Downloads/TIES_DataGeneration/UNLV_dataset/unlv_images')
parser.add_argument('--ocrpath',default='/Users/tuananh/Downloads/TIES_DataGeneration/UNLV_dataset/unlv_xml_ocr')
parser.add_argument('--tablepath',default='/Users/tuananh/Downloads/TIES_DataGeneration/UNLV_dataset/unlv_xml_gt')
parser.add_argument('--cols',default=0)
parser.add_argument('--rows',default=0)
parser.add_argument('--N',default=20,type=int,help='Number of images to generate')
parser.add_argument('--outpath',help='main output directory to store output images',default='gentables/')
parser.add_argument('--distributionpath',default='distribution_pickle')
parser.add_argument('--threads',type=int,default=1)
args=parser.parse_args()

#random.seed(a=None,version=2)
import time


def create_dir(path):
    if (not os.path.exists(path)):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)

    

def generate(outpath):

    arr=np.random.randint(1,10,(args.N,2))

    opts = Options()

    opts.set_headless()
    assert opts.headless

    driver = Firefox(options=opts)
    for i,subarr in tqdm.tqdm(enumerate(arr)):
        rows=subarr[0]
        cols=subarr[1]

        table=Table(rows,cols,args.imagespath,args.ocrpath,args.tablepath)
        same_row_matrix,same_col_matrix,same_cell_matrix,id_count,html_content, id_same_cells=table.create_html()
        # pickle.dump([same_row_matrix,same_col_matrix,same_cell_matrix,bboxes],"infofile.pkl")
        # print("same_cell_matrix", same_cell_matrix)
        path_image= os.path.join(outpath,"border_dash_line_table_"+str(i)+'.png')
        path_txt = path_image.replace("png","txt").replace("images","txt")
        path_html = path_image.replace("png","html").replace("images","html")
        try:
            image,bboxes=html_to_img(driver,html_content,path_image,id_count,768,1366, id_same_cells)
            with open(path_html,"w") as f:
                f.write(html_content)
            with open(path_txt,"w") as f_:
                for box in bboxes:
                    # print("box",box)
                    f_.write(str(",".join([str(i) for i in box[2:]]))+"\n")
        except:
            print('\nException')
            pass

        # try:
        #     table=Table(rows,cols,args.imagespath,args.ocrpath,args.tablepath)
        #     same_row_matrix,same_col_matrix,same_cell_matrix,id_count,html_content, id_same_cells=table.create_html()
        #     # pickle.dump([same_row_matrix,same_col_matrix,same_cell_matrix,bboxes],"infofile.pkl")
        #     print("same_cell_matrix", same_cell_matrix)
        #     path_image= os.path.join(outpath,"dashed_table_"+str(i)+'.png')
        #     path_txt = path_image.replace("png","txt").replace("images","txt")
        #     path_html = path_image.replace("png","html").replace("images","html")

        #     image,bboxes=html_to_img(driver,html_content,path_image,id_count,768,1366, id_same_cells)
        #     with open(path_html,"w") as f:
        #         f.write(html_content)
        #     with open(path_txt,"w") as f_:
        #         for box in bboxes:
        #             # print("box",box)
        #             f_.write(str(",".join([str(i) for i in box[2:]]))+"\n")
        # except:
        #     print('\nException')
        #     pass
    driver.stop_client()
    driver.quit()

create_dir(args.outpath)

startime=time.time()
procs=[]

outpath_root_image=os.path.join(args.outpath+'images')
outpath_root_txt=os.path.join(args.outpath+'txt')
outpath_root_html=os.path.join(args.outpath+'html')

for path in [outpath_root_image,outpath_root_txt,outpath_root_html]:
    create_dir(path)

generate(outpath_root_image)




