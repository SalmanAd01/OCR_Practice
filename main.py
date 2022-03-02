import easyocr
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import xlwt
import re

class OCR:
    result_dict = dict()
    def __init__(self,img_path):
        self.IMG_PATH = img_path
    def show(self):
        img = cv.imread(self.IMG_PATH)
        cv.imshow('img',img)
        cv.waitKey(0)
    def read_text(self):
        reader = easyocr.Reader(['en'],gpu=False)
        result = reader.readtext(self.IMG_PATH)
        print(result)
    def make_dict(self):
        reader = easyocr.Reader(['en'],gpu=False)
        result = reader.readtext(self.IMG_PATH)
        dict = {}
        index = 0
        while index < len(result):
            pattern = re.compile(r'[0-9]+')
            if pattern.match(result[index][1]):
                dict[result[index+1][1]] = result[index][1]
                index += 2
            else:
                dict[result[index][1]] = result[index+1][1]
                index += 2
        self.result_dict = dict
        print(dict)
    def get_dict(self):
        return self.result_dict
    def make_csv(self):
        dict = self.get_dict()
        with open('result.csv','w') as f:
            for key,value in dict.items():
                f.write(key+' '*10+value+'\n')
    def make_excel(self):
        dict = self.get_dict()
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet1')
        ws.write(0,0,"Subject")
        ws.write(0,1,"Marks")
        row = 1
        for key,value in dict.items():
            ws.write(row,0,key)
            ws.write(row,1,value)
            row += 1
        wb.save('result.xls')
    def highlight_text(self):
        reader = easyocr.Reader(['en'],gpu=False)
        result = reader.readtext(self.IMG_PATH)
        img = cv.imread(self.IMG_PATH)
        font = cv.FONT_HERSHEY_SIMPLEX
        for i in range(len(result)):
            try:
                cv.rectangle(img, tuple(result[i][0][0]), tuple(result[i][0][2]), (0,255,0), 2)
                cv.putText(img, result[i][1], tuple(result[i][0][0]), font, 1, (0,0,255), 2)
                print(result[i][0][0])
            except:
                print(result[i][0][2])
                numbers = [ int(x) for x in result[i][0][0] ]
                numbers2 = [ int(x) for x in result[i][0][2] ]
                cv.rectangle(img, numbers, numbers2, (0,255,0), 2)
                cv.putText(img, result[i][1], numbers, font, 1, (0,0,255), 2)
                print(numbers)
        plt.imshow(img)
        plt.show()


IMG_PATH = 'img/test.jpeg'
# img = OCR(IMG_PATH)
# # img.show()
# # img.read_text()
# # img.make_dict()
# # print(img.get_dict())
# # img.make_csv()
# # img.make_excel()
# img.highlight_text()