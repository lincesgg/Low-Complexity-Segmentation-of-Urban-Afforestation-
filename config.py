import cv2 as cv
import ExtraLibs.cv_ColorCvt.additional_color_cvt as additional_color_cvt

import segmentationUtils as utils

# APIs
# mapsAPI_KEY = "..."

# Paths
paths = {
	"debug_condos_dir": "C:/Users/lince/Documents/Projects/Analista_De_Aborizacao/Cpp_Analista_Arborizacao/Condominios_Usados",
	"bin_classification_ground_truth_dir": "C:/Users/lince/Documents/Projects/Analista_De_Aborizacao/Analista V.6/Condominios_Usados/ground_truth_bin_classification"
}

debug_condo_base_path = "C:/Users/lince/Documents/Projects/Analista_De_Aborizacao/Analista V.6/Condominios_Usados_newFormat"
debug_condo_imgs_name_prefix = "condo"
debug_imgs_condos_paths = {
	"src_imgs": f"{debug_condo_base_path}",
	"samples": f"{debug_condo_base_path}/sample",
	"scales": f"{debug_condo_base_path}/scale_images",
	"delimitation_masks": f"{debug_condo_base_path}/delimitation_masks",
	"delimitation_paths": f"{debug_condo_base_path}/delimitado_1px",
	"bin_classification_ground_truth": f"{debug_condo_base_path}/truth_references"
}

# Real Valid Data ---
# Trees Terrains
real_delimitation_areas = [11619.71, 4938.85, 6983.48, 930.67, 6639.72, 10673.67, 21207.25, 7249.32, 9198.49, 12340.8, 11375.05, 9757.2, 8036.28, 6255.92]
real_ROI_areas = [2421, 307.89, 1087.73, 452.85, 599.44, 690.03, 11167.5, 922.28, 758.56, 802.53, 1655.1, 2574.44, 1506.02, 2317.27]
real_scales = [20, 20, 20, 5, 20, 20, 20, 20, 20, 20, 10, 20, 20, 10]
tree_ignorated_areas = {0: 923462, 1: 944231, 2: 906847, 3: 889228, 4: 926625, 5: 886228, 6: 887038, 7: 826730, 8: 763940, 9: 860469, 10: 1185532, 11: 1534077, 12: 1591156, 13: 1353776, }

# DB Used
debug_imgs_path_used = debug_imgs_condos_paths
debug_imgs_prefix = debug_condo_imgs_name_prefix


# Color CVT
SHLS_f = lambda img: additional_color_cvt._convert_img_to(cv.cvtColor(img, cv.COLOR_BGR2HLS), additional_color_cvt.HSX_2_SHSX)
SHSV_f = lambda img: additional_color_cvt._convert_img_to(cv.cvtColor(img, cv.COLOR_BGR2HSV), additional_color_cvt.HSX_2_SHSX)
LAB_f = lambda img: cv.cvtColor(img, cv.COLOR_BGR2LAB)
LUV_f = lambda img: cv.cvtColor(img, cv.COLOR_BGR2LUV)
OKLAB_f = lambda img: additional_color_cvt.convert_img_to(img, additional_color_cvt.BGR_2_OKLAB)

