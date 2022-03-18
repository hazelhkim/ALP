# ALP: Data Augmentation using Lexicalized PCFGs for Few-Shot Text Classification

This repository is for the paper: [**ALP**:_Data **A**ugmentation using **L**exicalized **P**CFGs for Few-Shot Text Classification, AAAI 2022_](https://arxiv.org/abs/2112.11916).

To execute the ALP method with semi-supervised learning, run the **run_alp_st.py** script. It augments given data using ALP and trains a classic self-training classifier to test the classification performance. You can modify the **aug_alp.py** script to solely use the ALP method for different purposes than our few-shot text classification task.

In this paper, we introduce a data augmentation method (_i.e. **ALP**_) and a splitting scheme of training and validation sets (_i.e. **AugTrain-Train**_) to perform well in low-resource settings:



### Overview of ALP Method
<img width="850" alt="ALP" src="ALP.png">




### Overview of AugTrain-Train Method
<img width="600" alt="augTrain-TrainM" src="AugTrain-Train.png">
