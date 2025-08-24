import cv2 as cv
import numpy as np
from additional_color_cvt import additional_color_cvt

# ----------------
# Implementation
# ----------------

# '143 amount' extracted from documentation (https://docs.opencv.org/3.4/d8/d01/group__imgproc__color__conversions.html)
cv2_total_amount_color_cvt = 143
last_color_cvt_index = cv2_total_amount_color_cvt

# For Mapping Name To Index
additional_color_cvt = {}
# For Mapping Index to Func
additional_color_cvt_funcs = {}

def add_new_color_conversions(color_conversion_dict):
    for cvt_name in color_conversion_dict.keys():
        last_color_cvt_index += 1
        additional_color_cvt[cvt_name] = last_color_cvt_index
        additional_color_cvt_funcs = color_conversion_dict[cvt_name]

def map_rows(map_func):
    def _map_rows(row):
        row = list( map(map_func, row) )
        return row
    return _map_rows

def cvt_img(img, cvt_func_index):
    if cvt_func_index <= 143:
        return cv.cvtColor(img, cvt_func_index)
    else:
        cvt_func = additional_color_cvt_funcs[additional_color_cvt_funcs]
        return np.array( list( map(map_rows(cvt_func), img) ) )

# ----------------------------------------
# Importing Additional Color Conversions
# ----------------------------------------

add_new_color_conversions(additional_color_cvt)