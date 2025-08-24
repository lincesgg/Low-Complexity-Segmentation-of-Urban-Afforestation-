import cv2 as cv
import numpy as np

from math import ceil

def centroid_position(img): 
    white_pixels_pos = np.argwhere(img == 255)
    pixel_amount_of_analyzed_shape = white_pixels_pos.shape[0]
    sum_of_x_coordinates = white_pixels_pos[:, 1].sum()
    sum_of_y_coordinates = white_pixels_pos[:, 0].sum()

    centroid_y = round(sum_of_y_coordinates / pixel_amount_of_analyzed_shape)
    centroid_x = round(sum_of_x_coordinates / pixel_amount_of_analyzed_shape)

    centroid_position = (centroid_y, centroid_x)
    return centroid_position, pixel_amount_of_analyzed_shape

def apply_mask(img, mask):
    return cv.bitwise_and(img, img, mask=mask) 

def overlay_img_with_darkned_background(img, background, alpha=.1, beta=0):
    darkened_bottom_img = cv.convertScaleAbs(background, alpha=alpha, beta=beta)

    # cv.imshow('Baseeeeee', darkened_bottom_img)

    result_over_base_img = cv.addWeighted(darkened_bottom_img, 1.0, img, 1.0, 0)
    #cv.bitwise_or(darkened_bottom_img, img)

    return result_over_base_img

def contour_img_with_mask_contours(img, mask, alpha=.2, beta=0, mask_contour_diffusion=7):
        img = img.copy()
        mask = mask.copy()

        # Top Image
        top_img = apply_mask(img, mask)

        # Creating Diffused Mask
        if mask_contour_diffusion != 0:
            blurred_thresh = cv.blur(mask, (mask_contour_diffusion, mask_contour_diffusion))
            ret, mask = cv.threshold(blurred_thresh, 20, 255, cv.THRESH_BINARY)

        # Countour Drawer
        edges = cv.Canny(cv.bitwise_not(mask), 120, 140)
        contours, hierarch = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        img_with_contours = cv.drawContours(top_img, contours, -1, (255, 0, 0), 2)

        # Gerador de Imagem Final
        result_over_base_img = overlay_img_with_darkned_background(img_with_contours, img, alpha=alpha, beta=beta)

        return result_over_base_img

def create_mask_based_on_other_weigtened_masks(masks_and_weights=[[[], 1.0]], threshold_relative_to_best_method=False, threshold=0.95, max_value=255):
    """
    Receives a list of (mask, weight) \n
    Creates a new mask based on a weightened mean of the mask \n
    The Pixels On The Final Mask with (%) value < threshold will be removed from mask
    """

    weighted_mask = masks_and_weights[0][0].astype('float64') * masks_and_weights[0][1]
    weights_sum = masks_and_weights[0][1]

    for mask, weight in masks_and_weights[1:]:
        weighted_mask += mask.astype('float64') * weight
        weights_sum += weight

    mean_weighted_mask = weighted_mask / weights_sum
    mean_weighted_mask = mean_weighted_mask.astype('uint8')

    if threshold_relative_to_best_method:
        weights = [weight for mask, weight in masks_and_weights]
        max_weight = np.array(weights).max()
        max_value_for_most_weigthned_mask_at_full_value_and_other_at_0 = max_value * max_weight / weights_sum

        threshold = ceil(threshold * max_value_for_most_weigthned_mask_at_full_value_and_other_at_0) - 1
    
    else:
        threshold = ceil(threshold * max_value) - 1


    _, final_mask = cv.threshold(mean_weighted_mask, threshold, max_value, cv.THRESH_BINARY)
    

    # cv.imshow("Weightned --", cv.applyColorMap(mean_weighted_mask, cv.COLORMAP_VIRIDIS))
    # cv.imwrite("GRAY_mean_weighted_mask.png", mean_weighted_mask)
    # cv.waitKey(1)

    return {
        "heat_map": cv.applyColorMap(mean_weighted_mask, cv.COLORMAP_VIRIDIS),
        "GRAY_mean_weighted_mask": mean_weighted_mask,
        "final_mask": final_mask.astype('uint8')
    }

def extract_analysis_result_values(base_img, vegetation_in_area_to_analyze_mask, should_crop_region_of_interest, initial_interest_region_size, squared_pixel_to_squared_meter):
    # Calculating Centroid Position
    _centroid_position, vegetation_area_size = centroid_position(vegetation_in_area_to_analyze_mask)

    # Calculating Interest Region Size
    img_height, img_width, _ = base_img.shape

    interest_region_size = img_height * img_width if not should_crop_region_of_interest else initial_interest_region_size
    percentual_vegetation_area = round((vegetation_area_size / (interest_region_size)) * 100, 3)

    print(squared_pixel_to_squared_meter)
    real_total_area = round(interest_region_size * squared_pixel_to_squared_meter, 2)
    real_vegetation_area = round(vegetation_area_size * squared_pixel_to_squared_meter, 2)

    return {
        "data":{
            "vegetation_percentage_calculated":percentual_vegetation_area,
            "vegetation_area_calculated":real_vegetation_area,
            "interest_region_size": interest_region_size,
            "total_area_calculated":real_total_area
        }
    }

def remove_outliers_from_sample(sample_img, safe_zone_coefficient=1.7):
    sample_img = sample_img.astype('float64')
    c_stds = sample_img.reshape(-1, 3).std(axis=0) * safe_zone_coefficient
    c_means = sample_img.reshape(-1, 3).mean(axis=0)
    sample_img = np.where(abs(c_means-sample_img) < c_stds, sample_img, c_means)
    return sample_img.astype('uint8')

def inverse_if_greater_than_1(x):
    return x if x < 1 else x**-1

def return_mask_size(mask):
    _, thresh = cv.threshold(mask, 0, 255, cv.THRESH_BINARY)
    _, counts = np.unique(thresh, return_counts=True)
    mask_size = counts[-1]

    return mask_size