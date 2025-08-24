from .debugCondoAnalysisSummary import _debugCondoAnalysisSummary
# import imgAnalyzerPresets as presets

import numpy as np
import os
from config import *
import copy
import timeit


### Utils
def appendToFile(filePath, text):
    file = open(filePath, "a")
    file.write(text)
    file.close()


### ----

file_prefix = "all_trees"

dir_path = "C:\\Users\\lince\\Documents\\Projects\\Analista_De_Aborizacao\\Analista V.6\\News\\program\\segmentationAnalysis\\serializedResults\\"
file_prefix = dir_path + file_prefix

should_evaluate_binary_classifcation = True
# color_spaces = ["SHLS", "SHSV", "LAB", "LUV", "OKLAB", "RGB"]
color_spaces = ["SHLS", "SHSV", "LAB", "LUV", "RGB"]

# color_spaces = ["RGB"]
# color_spaces = ["SHLS"]

# all_presets = [presets.min_max_threshold, presets.mean_sd_threshold, presets.kmeans_knn, presets.SLIC_superpixel_minMax]
all_presets = [presets.min_max_threshold]
# all_presets = [presets.mean_sd_threshold]
# all_presets = [presets.SLIC_superpixel_minMax, presets.SNIC_superpixel_minMax]

def return_all_color_spaces_results(color_spaces:list[str], segmenter, segmenter_config, should_bin_classificate, file_name):

    for color_space in color_spaces:
        color_space_conversion_f = eval(f"{color_space+'_f'}") if color_space != "RGB" else None
        results = _debugCondoAnalysisSummary.return_all_validated_results(segmenter, segmenter_config, color_space_conversion_f, [0, 14],
                                                                            real_scales, real_ROI_areas, real_delimitation_areas, should_bin_classificate)
        print(f"\t'{color_space}_results':  {results},\n")
        appendToFile(file_name, f"\t'{color_space}_results':  {results},\n")
        ### appendToFile(file_name, f"\t'{color_space}_davies_boudin':  {results},\n")
        print("--")
        

for preset in all_presets:
    print("=========================")
    print(f"{preset["name"]}")
    print("=========================")
    
    file_path = f"{file_prefix}_{preset["name"]}_pos_correction.txt"
    file = open(file_path, "w")
    file.write("")
    file.close()

    # print(f"'{preset["name"]}': {{")
    # appendToFile(file_path, f"'{preset["name"]}': {{")
    
    results = return_all_color_spaces_results(color_spaces, preset["segmenter"], preset["segmentation_config"], should_evaluate_binary_classifcation, file_path)
    
    # print(f"}}\n")
    # appendToFile(file_path, f"}},\n")




# [K-Means: K] Optimal K
# file_path = f"./{file_prefix}_Optimal_Kmeans_K_search_n_init_3_pos_truth_correction_Non_Repeated_Data_(((3 over 8)_clusters_amount_as_Centroids_at_KNN.txt"

# if not os.path.exists(file_path):
#     file = open(file_path, "w")
#     file.write("")
#     file.close()
    
# for k in range(20, 320, 20):
#     kmeans_config = copy.copy(presets.kmeans_knn["segmentation_config"])
#     kmeans_config["K"] = k
    
#     print(f"'Kmeans_k_{k}': {{\n")
#     appendToFile(file_path, f"'Kmeans_k_{k}': {{\n")
    
#     return_all_color_spaces_results(color_spaces, presets.kmeans_knn["segmenter"], kmeans_config, should_evaluate_binary_classifcation, file_path)    
    
#     print(f"}},\n")
#     appendToFile(file_path, f"}},\n")


    
# [SLIC MinMax] Optimal K and m
# file_path = f"./{file_prefix}_Optimal_SLIC_search_pos_truth_correction.txt"
# # file_path = f"./{file_prefix}_Optimal_SNIC_search_pos_truth_correction.txt"
# crr_preset = presets.SLIC_superpixel_minMax

# if not os.path.exists(file_path):
#     file = open(file_path, "w")
#     file.write("")
#     file.close()
    
# for superpixel_area in [20**2, 15**2, 10**2, 5**2]:
#     for m in [10, 20, 30, 50, 75, 100, 200]:
#         SLIC_config = copy.copy(crr_preset["segmentation_config"])
#         # SLIC_config = copy.copy(presets.SLIC_superpixel_minMax["segmentation_config"])
#         SLIC_config["superpixel_config"]["superpixels_amount"] = 1 / superpixel_area
#         SLIC_config["superpixel_config"]["compactness"] = m
        
#         print(f"'SLIC_minmax_spxArea_{superpixel_area}_m_{m}': {{\n")
#         appendToFile(file_path, f"'SLIC_minmax_spxArea_{superpixel_area}_m_{m}': {{\n")
        
#         return_all_color_spaces_results(color_spaces, crr_preset["segmenter"], SLIC_config, should_evaluate_binary_classifcation, file_path)    
#         # return_all_color_spaces_results(color_spaces, presets.SLIC_superpixel_minMax["segmenter"], SLIC_config, should_evaluate_binary_classifcation, file_path)    
        
#         print(f"}},\n")
#         appendToFile(file_path, f"}},\n")



# # [Mean-SD Thresholding] Analysis With Each Coeff Of Interest ---
# file_path = f"./{file_prefix}_Optimal_Mean_SD_Thresh_pos_truth_correction.txt"

# if not os.path.exists(file_path):
#     file = open(file_path, "w")
#     file.write("")
#     file.close()

# for preset in [presets.mean_sd_threshold]:
#     for coeff in np.arange(0, 6.05, 0.05, dtype=float):
#         coeff = round(coeff, 2)
#         preset["segmentation_config"]["coeff"] = coeff

#         print("=========================")
#         print(f"{preset["name"]}_{coeff}")
#         print("=========================")

#         print(f"'{preset["name"]}_{coeff}': {{")
#         appendToFile(file_path, f"'{preset["name"]}_{coeff}': {{\n")

#         results = return_all_color_spaces_results(color_spaces, preset["segmenter"], preset["segmentation_config"], should_evaluate_binary_classifcation, file_path)

#         print(f"}}\n")
#         appendToFile(file_path, f"}},\n")



# for coeff in np.arange(0, 11, 0.05, dtype=float):
#     print(f"'{coeff:.2f}': {{")
#     results = return_all_color_spaces_results(color_spaces, preset["segmenter"], {"coeff":coeff})
#     print(f"}}\n")

