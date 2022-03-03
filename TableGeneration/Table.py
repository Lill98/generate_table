
import random
import numpy as np
from TableGeneration.Distribution import Distribution

class Table:
    def __init__(self,no_of_rows,no_of_cols,images_path,ocr_path,table_path):
        self.no_of_rows=no_of_rows
        self.no_of_cols=no_of_cols
        self.distribution=Distribution(images_path,ocr_path,table_path)
        self.all_words,self.all_numbers=self.distribution.get_distribution()
        self.words_distribution, self.numbers_distribution = len(self.all_words), len(self.all_numbers)
        self.html = """<html>"""
        self.id_count=0
        self.same_cols=[]
        self.same_rows=[]
        self.same_cells=[]
        self.header_span_indices=[]
        self.current_col=0
        self.table_type=1



    def create_style(self):
        self.html+="<head><style>"
        self.html+="html{width:1366px;height:768px;background-color: white;}table{"
        # self.html += """ border:1px dashed black; border-collapse: collapse;"""
        self.html += """border-collapse: collapse; border-color:#7F7E7E;border-style:solid;""" #border:1px solid black; 

        #random center align
        if(random.randint(0,1)==1):
            self.html+="text-align:center;"
            #  style="width:100%","height:100%"
        self.html+= "width:100%;height:80%"
        # self.html+="""}td,th{border: 0.2px dashed black;"""
        self.html+="""}td{border-style:solid;border-color:#7F7E7E;"""
        self.html+="""}th{border-style:solid; background-color:#918E8E;border-color:#7F7E7E;"""
#solid black border: 1px solid black;
        

        # if (random.randint(0, 1) == 1):  # border or non-border
        #     self.html += """ border:1px solid black; """
        # else:
        #     self.html+="""border-bottom:1px solid black;"""
        # self.html += """ border:1px dashed black; border-collapse: collapse;"""

        self.html+="}</style></head>"

    def create_html(self):
        self.create_style()
        self.create_table()
        same_row_matrix = self.get_same_matrix(self.same_rows)
        same_col_matrix = self.get_same_matrix(self.same_cols)
        same_cell_matrix = self.get_same_matrix(self.same_cells)
        # print("self.same_cells", self.same_cells)
        return same_row_matrix,same_col_matrix,same_cell_matrix,self.id_count,self.html, self.same_cells


    def create_table(self):

        self.html+="""<table background="/Users/lill98/Documents/EHR/data/generate_table/TIES_DataGeneration/background/bg1.jpeg">"""

        self.define_col()
        if (self.no_of_cols > 1):
            self.header_span_indices = self.get_header_col_span_indices()

        self.create_headers()
        self.create_rows()
        self.table_type=random.randint(1,5)


    def get_header_col_span_indices(self):
        x = random.randint(0, self.no_of_cols)
        l = []
        for e in range(x, self.no_of_cols-1, 2):
            l.append(x)
        return random.sample(l, random.randint(0, len(l)))

    def define_col(self):
        total=self.words_distribution+self.numbers_distribution
        prob_words=self.words_distribution/total
        prob_numbers=self.numbers_distribution/total
        self.col_types=random.choices([0,1], weights=[prob_words,prob_numbers],k=self.no_of_cols)
        for _ in range(self.no_of_cols): self.same_cols.append([])

    def get_rand_text(self,header):
        #header is a flag. If true, means it should be text, else conditioned upon the col_types
        text_len = random.randint(3, 4)
        if(header==True or self.col_types[self.current_col]==0):
            text_arr = random.sample(self.all_words, text_len)
        else:
            text_arr = random.sample(self.all_numbers, 1)
        final_text = ''
        for idx, t in enumerate(text_arr):
            if idx > 1: 
                final_text += '<span id=\"' + str(self.id_count) + '\">' + t + '<br>'+' </span>'
            else:
                final_text += '<span id=\"' + str(self.id_count) + '\">' + t + ' </span>'
            self.id_count += 1
        return final_text

    def append_same_cols_and_cells(self,start_col, end_col):
        try:
            temp = [i for i in range(start_col, end_col)]
            self.same_cols[self.current_col] += (temp)
            self.same_cells.append(temp)
        except:
            print('\nError at current_col:',self.current_col)
            print('\nLen of same_cols:',len(self.same_cols))

    def enlist_same_rows(self,start_row, end_row):
        self.same_rows.append([i for i in range(start_row, end_row)])


    def create_headers(self):
        if(random.randint(0,1)==1):
            self.html+="<tr background-color=#CDCCCC>"
        else:
            self.html += "<tr>"
        self.html+="<tr background-color=#CDCCCC>"

        start_row = self.id_count

        for c in range(self.no_of_cols):
            self.current_col = c
            # if this column is spanning 2 columns
            if (c in self.header_span_indices):
                start_col = self.id_count
                self.html += "<th colspan=2>" + str(self.get_rand_text(True)) + "</th>"
                end_col = self.id_count
                self.append_same_cols_and_cells(start_col, end_col)

                # same elements for the two spanned columns
                self.current_col += 1
                self.append_same_cols_and_cells(start_col, end_col)

            # if previous column had two column span
            elif (c - 1 in self.header_span_indices):
                continue

            else:
                start_col = self.id_count
                self.html += "<th rowspan=2>" + str(self.get_rand_text(True)) + "</th>"
                # html += "<th rowspan=1>"++"</th>"
                end_col = self.id_count
                self.append_same_cols_and_cells(start_col, end_col)

        end_row = self.id_count
        self.enlist_same_rows(start_row, end_row)
        self.html += '</tr>'

        self.html += "<tr>"
        start_row = self.id_count
        for c in range(self.no_of_cols):
            self.current_col = c
            if (c in self.header_span_indices or c - 1 in self.header_span_indices):
                start_col = self.id_count
                self.html += "<th>" + str(self.get_rand_text(True)) + "</th>"
                end_col = self.id_count
                self.append_same_cols_and_cells(start_col, end_col)
        end_row = self.id_count
        self.enlist_same_rows(start_row, end_row)
        self.html += '</tr>'

    def create_rows(self):
        for _ in range(self.no_of_rows):
            n_gaib = random.randint(0, self.no_of_cols // 2)
            gaib_indices = random.sample(range(self.no_of_cols), n_gaib)
            self.html += "<tr>"
            start_row = self.id_count
            for c in range(self.no_of_cols):
                self.current_col = c
                self.html += "<td>"
                if (c not in gaib_indices):
                    start_col = self.id_count
                    self.html += str(self.get_rand_text(False))
                    end_col = self.id_count
                    self.append_same_cols_and_cells(start_col, end_col)
                else:
                    self.html += ""
                self.html += "</td>"
            end_row = self.id_count
            self.enlist_same_rows(start_row, end_row)
            self.html += '</tr>'
        self.html += """</table></html>"""

    def get_same_matrix(self,same_data):
        same_matrix = np.zeros(shape=(self.id_count, self.id_count))
        for row in same_data:
            for element in row:
                same_matrix[element, np.array(row)] = 1
        return same_matrix
