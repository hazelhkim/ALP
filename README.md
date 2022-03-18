# ALP: Data Augmentation using Lexicalized PCFGs for Few-Shot Text Classification

This repository is for the paper: [**ALP**:_Data **A**ugmentation using **L**exicalized **P**CFGs for Few-Shot Text Classification, AAAI 2022_](https://arxiv.org/abs/2112.11916).

To run the ALP method with semi-supervised learning, run **run_alp_st.py**. It augments given data using ALP and trains a classic self-training classifier to test the classification performance. You can run **the aug_alp.py** to solely use the ALP method for different purposes than our baseline semi-supervised learning method, classic self-training.

In this paper, we introduce a data augmentation method (i.e. _**ALP**_) and a novel splitting scheme of training and validation sets (i.e. _**AugTrain-Train**_) to perform well in low-resource settings:



### Overview of ALP Method
<img width="850" alt="ALP" src="ALP.png">




### Overview of AugTrain-Train Method
<img width="600" alt="augTrain-TrainM" src="AugTrain-Train.png">
