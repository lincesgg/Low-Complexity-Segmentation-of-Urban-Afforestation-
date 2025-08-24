from typing import Sequence, Tuple
from analysisTypes import *
import pandas as pd
import copy

def returnBinaryClassificationEvaluationMetrics(typesDistribution: typesDistribution_t) -> classification_evaluation_metrics_t:
    # Compute Accuracy and Precision ---
    # Bool(0) == False, then If Denominator == 0, the metric result'll 0
    predictedPositives = (typesDistribution["TP"] + typesDistribution["FP"])
    positives = (typesDistribution["TP"] + typesDistribution["FN"])
    negatives = (typesDistribution["TN"] + typesDistribution["FP"])
    
    precision = predictedPositives and typesDistribution["TP"] / predictedPositives or 0
    recall = positives and typesDistribution["TP"] / positives or 0
    
    truePositiveRate = recall
    trueNegativeRate = negatives and typesDistribution["TN"] / negatives or 0
    falsePositiveRate = positives and typesDistribution["FP"] / negatives or 0
    falseNegativeRate = positives and typesDistribution["FN"] / positives or 0
    
    overselectionIndex = (falsePositiveRate - falseNegativeRate) / (falsePositiveRate + falseNegativeRate)
    
    accuracy = (typesDistribution["TP"] + typesDistribution["TN"]) / (typesDistribution["TOTAL_CLASSIFICATIONS"])
    balancedAccuracy = (truePositiveRate + trueNegativeRate) / 2.0
    jaccardIndex = typesDistribution["TP"] / (typesDistribution["TP"] + typesDistribution["FN"] + typesDistribution["FP"])
    
    F1Score = (2 * typesDistribution["TP"]) / (2 * typesDistribution["TP"] + typesDistribution["FP"] + typesDistribution["FN"])
        
    return {
        "precision":precision * 100,
        "recall": recall * 100,
        
        "truePositiveRate": truePositiveRate * 100,
        "trueNegativeRate": trueNegativeRate * 100,
        "falsePositiveRate": falsePositiveRate * 100,
        "falseNegativeRate": falseNegativeRate * 100,
        
        "accuracy": accuracy * 100,
        "balancedAccuracy": balancedAccuracy * 100,
        
        "jaccardIndex": jaccardIndex * 100, 
        "F1Score": F1Score * 100,
        
        "overselectionIndex": overselectionIndex * 100,
        
        "typesDistribution": typesDistribution
    }

def quantifyDsPropertiesMeanAndDs(ds, dict_insde_dict:bool=False):
    dataPointEx = ds[0]
    properties = [*dataPointEx.keys()]
    
    propsMean = {}
    df = pd.DataFrame(ds)
    
    for prop in properties:
        if type(dataPointEx[prop]) is dict:
            propsMean[f"mean_{prop}"] = quantifyDsPropertiesMeanAndDs(df[prop].to_list(), True)
        else:
            prop_ds_name = f"{prop}" if dict_insde_dict else f"mean_{prop}"
            propsMean[prop_ds_name] = df[prop].mean()
            
            propsMean[f"{prop}_ds"] = df[prop].to_list()
        
    return propsMean

def remove_bin_class_bias(idx_condo:Tuple[int, classification_evaluation_metrics_t]):
    """_summary_
    Remove Bias: Ignore Correct Classification of Pixels Masked Out Before Segmentation
    """

    (idx, classification_evaluation_metrics) = idx_condo
    classification_evaluation_metrics = copy.deepcopy(classification_evaluation_metrics)
    
    ignorated_area = {0: 923462, 1: 944231, 2: 906847, 3: 889228, 4: 926625, 5: 886228, 6: 887038, 7: 826730, 8: 763940, 9: 860469, 10: 1185532, 11: 1534077, 12: 1591156, 13: 1353776, }

    classification_evaluation_metrics['typesDistribution']["TN"] -= ignorated_area[idx]
    classification_evaluation_metrics['typesDistribution']["TOTAL_CLASSIFICATIONS"] -= ignorated_area[idx]
    
    new_bin_eval_metrics = returnBinaryClassificationEvaluationMetrics(classification_evaluation_metrics['typesDistribution'])
    new_bin_eval_metrics = {**classification_evaluation_metrics, **new_bin_eval_metrics}
    return new_bin_eval_metrics


def return_segmentation_classification_eval_metrics(condo_ds: condo_ds_t):
    condo_ds_df = pd.DataFrame(condo_ds)
    
    classification_results = condo_ds_df["classification_evaluation_metrics"].to_list()
    unbiased_classification_results = [*map(remove_bin_class_bias, enumerate(classification_results))]

    return quantifyDsPropertiesMeanAndDs(unbiased_classification_results)


