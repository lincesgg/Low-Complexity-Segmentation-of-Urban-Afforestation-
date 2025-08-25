# Low Complexity Segmentation of Urban Afforestation
Data, Graphs and Codes For Evaluating Performance of Low Complexity Methods For Segmenting Urban Afforestation.

Data: `segmentationAnalysis/condoAnalysisData.py`

Data Processing Notebook: `segmentationAnalysis/analyze_segmentation_results.ipynb`

### Best normMCC results For Each Color Space
---
![Min-Max Thresholding](./extraAssets/Min_Max_K_Folds_Results.png)
![Mean-SD Thresholding](./segmentationAnalysis/analysisResults/MCC/Mean-SD/Mean-SD-Best_Results_From_Each_Color_Space.png)
![Kmeans + KNN](./segmentationAnalysis/analysisResults/MCC/K-Means+KNN/K-Means+KNN-Best_Results_From_Each_Color_Space.png)
![Slic Min-Max](./segmentationAnalysis/analysisResults/MCC/MinMax-Slic/MinMax-Slic-Best_Results_From_Each_Color_Space.png)


### Mean NormMCC For Each Method (Tecnique + Hyperparameters) Along All Color Spaces
---

|<img src="./segmentationAnalysis/analysisResults/MCC/Mean-SD/heatmaps/Mean-SD-Mean-Of-Color-Spaces-MCC-HPs_Heatmap.png" width="250"/>|<img src="./segmentationAnalysis/analysisResults/MCC/K-Means+KNN/heatmaps/K-Means+KNN-Mean-Of-Color-Spaces-MCC-HPs_Heatmap.png" width="250"/>|<img src="./segmentationAnalysis/analysisResults/MCC/MinMax-Slic/heatmaps/MinMax-Slic-Mean-Of-Color-Spaces-MCC-HPs_Heatmap.png" width="250"/> |
|:---------------:|:----------:|:------------:|
|Mean-SD Threshold|Kmeans + KNN|SLIC + Min-Max|

