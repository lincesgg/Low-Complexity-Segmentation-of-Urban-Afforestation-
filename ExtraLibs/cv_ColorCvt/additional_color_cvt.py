import cv2 as cv
import numpy as np
import colour

def cube_root(x):
    if x < 0:
        x = abs(x)
        cube_root = x**(1/3)*(-1)
    else:
        cube_root = x**(1/3)
    return cube_root

# --------
# Conversion Functions

def BGR_2_SHSV(_pixel):
        pixel = [int(_pixel[0]), int(_pixel[1]), int(_pixel[2])]
        b, g, r = pixel

        _max = max(b, g, r)
        _min = min(b, g, r)

        _max_channel = ["b", "g", "r"][pixel.index(_max)]

        # Defining HUE (H)
        if _max == _min:
            pixel[0] = 0
            
        else:
            match(_max_channel):

                case "r":
                    pixel[0] = (60 * ((g-b)/(_max-_min))) + 60
                        
                case "g":
                    pixel[0] = (60 * ((b-r)/(_max-_min))) + 180

                case "b":
                    pixel[0] = (60 * ((r-g)/(_max-_min))) + 300

        pixel[0] /= 2

        # Defining SATURATION (S)
        pixel[1] = 0 if _max == 0 else 1 - (_min/_max)
        pixel[1] *= 255

        # Defining VALUE (V)
        pixel[2] = _max
        
        # truncking
        pixel[0] = int( round(pixel[0], 0) )
        pixel[1] = int( round(pixel[1], 0) )
        
        return pixel


def HSX_2_SHSX(_img):
    img = _img.copy()
    
    img = img + [30, 0, 0]
    img[:, :, 0] = np.fmod(img[:, :, 0], 181)
    
    return img

def SHSX_2_HSX(_img):
    img = _img.copy()
    
    img = img + [150, 0, 0]
    img[:, :, 0] = np.fmod(img[:, :, 0], 181)
    return img
    
    
    pixel[0] -= 30
    if pixel[0] < 0: 
        pixel[0] += 180
    return pixel

def BGR_2_SHSX(pixel, HSX_color_system=cv.COLOR_BGR2HSV):
    HSX = cv.cvtColor(np.array([[pixel]], dtype='uint8'), HSX_color_system)
    HSX = list(HSX[0][0])

    return HSX_2_SHSX(pixel)



def BGR_2_OKLAB(pixel):
    XYZ = cv.cvtColor(np.array([[pixel]], dtype='uint8'), cv.COLOR_BGR2XYZ)[0][0]
    X, Y, Z = XYZ

    X = X/255
    Y = Y/255
    Z = Z/255
    
    return list(colour.XYZ_to_Oklab([X, Y, Z]))

def OKLAB_2_BGR(pixel):
    L, a, b = pixel

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_ * l_ * l_
    m = m_ * m_ * m_
    s = s_ * s_ * s_

    pixel[0] = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    pixel[1] = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    pixel[2] = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    return pixel



# --------
# Lib Functions

def map_rows(map_func):
    def _map_rows(row):
        row = list( map(map_func, row) )
        return row
    return _map_rows

def convert_img_to(img, map_func):
    return np.array( list( map(map_rows(map_func), img) ) )


def _convert_img_to(img, map_func):
    return map_func(img)    

# ---------------------------
# Listing Color Conversions
# ---------------------------
additional_color_cvt = {
    "BGR_2_SHSV":BGR_2_SHSV,
    "HSX_2_SHSX":HSX_2_SHSX,
    "SHSX_2_HSX":SHSX_2_HSX
}
