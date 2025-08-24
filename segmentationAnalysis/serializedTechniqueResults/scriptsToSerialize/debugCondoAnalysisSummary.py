from results import *

import cv2 as cv
from imgAnalyzer import imgAnalyzer

from imgAnalyzerPresets import *
from segmentation.Clusterization import *
from segmentation.segmenters import *

from config import *

class _debugCondoAnalysisSummary():
    @staticmethod
    def validate_analysis_results(should_bin_classificate, grayscale_ground_truth, segmentation_imgs, results, ROI_real_value, delimitation_real_value):
        results_validation: segmentationResultsValidated = segmentationResultsValidated(results, ROI_real_value, delimitation_real_value)
        
        # Bin Classification Eval ---
        if should_bin_classificate:
            # ground_truth = cv.imread(f"{paths["bin_classification_ground_truth_dir"]}/condominio_{condo_i}.png", cv.IMREAD_GRAYSCALE)
            ground_truth = grayscale_ground_truth
            _, ground_truth = cv.threshold(ground_truth, 0, 255, cv.THRESH_BINARY)
            
            actual_classification = segmentation_imgs["bin_ROI"]
            results_validation.evaluate_binary_classification(ground_truth, actual_classification)
        
        results_validation_serializable = results_validation.__dict__
        return results_validation_serializable
    
    @staticmethod
    def return_all_validated_results(segmenter, segmentation_config, analysis_color_space, condos_range:int, scales_real_values:int, ROI_real_values:int,
                                     delimitation_real_values:int, should_bin_classificate:bool=False):
        
        all_results = []

        for condo_i in range(*condos_range):
            # Importing Imgs
            src = cv.imread(f"{debug_imgs_path_used['src_imgs']}/{debug_imgs_prefix}_{condo_i}.png")
            sample = cv.imread(f"{debug_imgs_path_used['samples']}/{debug_imgs_prefix}_{condo_i}.png")
            scale_img = cv.imread(f"{debug_imgs_path_used['scales']}/{debug_imgs_prefix}_{condo_i}.png")
            delimitated_img = cv.imread(f"{debug_imgs_path_used['delimitation_paths']}/{debug_imgs_prefix}_{condo_i}.png")

            # Img Analysis
            analysis_data = imgAnalyzer.return_analysis_data(src, delimitated_img, sample, segmenter, segmentation_config, analysis_color_space, scale_img,
                                                             scales_real_values[condo_i] )
            results:segmentationResults = analysis_data["results"]
            segmentation_imgs:segmentationResults = analysis_data["sub_products"]["imgs"]
            
            # Results Validation
            # results_validation: segmentationResultsValidated = segmentationResultsValidated(results, ROI_real_values[condo_i], delimitation_real_values[condo_i])
            
            # Bin Classification Eval ---
            # if should_bin_classificate:
            #     # ground_truth = cv.imread(f"{paths["bin_classification_ground_truth_dir"]}/condominio_{condo_i}.png", cv.IMREAD_GRAYSCALE)
            #     ground_truth = cv.imread(f"{debug_imgs_path_used["bin_classification_ground_truth"]}/{debug_imgs_prefix}_{condo_i}.png", cv.IMREAD_GRAYSCALE)
            #     _, ground_truth = cv.threshold(ground_truth, 0, 255, cv.THRESH_BINARY)
                
            #     actual_classification = segmentation_imgs["bin_ROI"]
                # results_validation.evaluate_binary_classification(ground_truth, actual_classification)
            
            # results_validation_serializable = results_validation.__dict__
            
            ground_truth = None
            if should_bin_classificate:
                ground_truth = cv.imread(f"{debug_imgs_path_used["bin_classification_ground_truth"]}/{debug_imgs_prefix}_{condo_i}.png", cv.IMREAD_GRAYSCALE)
                _, ground_truth = cv.threshold(ground_truth, 0, 255, cv.THRESH_BINARY)
                
            results_validated = _debugCondoAnalysisSummary.validate_analysis_results(should_bin_classificate, ground_truth, segmentation_imgs, results, ROI_real_values[condo_i], delimitation_real_values[condo_i])
            
            # Gambiarra Para Obter Informações do Kmeans ---
            # results_validated["kmeans_davies_boudin"] = analysis_data["sub_products"]["kmeans_davies_boudin"]
            results_validated["time_to_analyze"] = analysis_data["sub_products"]["time_to_analyze"]
            all_results.append(results_validated)
            
        return all_results
            
        
            
            