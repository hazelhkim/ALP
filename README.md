# ALP: Data **A**ugmentation using **L**exicalized **P**CFGs for Few-Shot Text Classification

This repository is for the paper: _Data Augmentation using Lexicalized PCFGs for Few-Shot Text Classification, AAAI 2022_.

To run the ALP method with semi-supervised learning, run **run_alp_st.py**. It augments given data using ALP and trains a classic self-training classifier to test the classification performance. You can run **the aug_alp.py** to solely use the ALP method for different purposes than our baseline semi-supervised learning method, classic self-training.

In this paper, we introduced data augmentation method and splitting schemes of training and validation sets to perform well in low-resource settings:

- Overview of ALP Method
[ALP.pdf](https://github.com/hazelhkim/ALP/blob/main/ALP.pdf)
<img width="844" alt="Screen Shot 2019-09-23 at 6 31 44 PM" src="https://user-images.githubusercontent.com/46575719/65467824-78eb6500-de30-11e9-82e6-b036f85c31c8.png">


- Overview of AugTrain-Train Method
- [AugTrain-Train.pdf](https://github.com/hazelhkim/ALP/files/8303034/AugTrain-Train.pdf)
