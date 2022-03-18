"""Manipulated the function for uncertainty-aware self-training for few-shot learning by Subho Mukherjee (submukhe@microsoft.com)"""
from collections import defaultdict
from aug_alp import *
import csv
import logging
import numpy as np
import six
import tensorflow as tf


logger = logging.getLogger('ST')

def convert_to_unicode(text):
  """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
  if six.PY3:
    if isinstance(text, str):
      return text
    elif isinstance(text, bytes):
      return text.decode("utf-8", "ignore")
    else:
      raise ValueError("Unsupported string type: %s" % (type(text)))
  elif six.PY2:
    if isinstance(text, str):
      return text.decode("utf-8", "ignore")
    elif isinstance(text, unicode):
      return text
    else:
      raise ValueError("Unsupported string type: %s" % (type(text)))
  else:
    raise ValueError("Not running on Python2 or Python 3?")

def generate_train_val_sequence_data(MAX_SEQUENCE_LENGTH, input_file, sup_labels, tokenizer, n_aug, seed, unlabeled=False):
    
    X1 = []
    X_origin = []
    X2 = []
    y = []

    label_count = defaultdict(int)
    with tf.io.gfile.GFile(input_file, "r") as f:
      reader = csv.reader(f, delimiter="\t", quotechar=None)
      for line in reader:
        if len(line) == 0:
          continue
        X_origin.append(line[0])
        #X1.append(convert_to_unicode(line[0]))
        if not unlabeled:
            label = int(convert_to_unicode(line[-1]))
            y.append(label)
            label_count[label] += 1
        else:
            y.append(-1)
    X_origin = np.array(X_origin)
    y = np.array(y)
    labels = set(y)
    if 0 not in labels:
      y -= 1
    labels = set(y)
    X_train_, y_train, X_val_, y_val = [], [], [], []
    for i in labels:
      indx = np.where(y==i)[0]
      random.Random(seed).shuffle(indx)
      train_indx = indx[:sup_labels]
      val_indx = indx[sup_labels+1: 2*sup_labels+1]
        
      X_train_.extend(X_origin[train_indx])
      X_val_.extend(X_origin[val_indx])
      y_train.extend(y[train_indx])
      y_val.extend(y[val_indx])
      total_augmented_data = aug_alp(X_origin[train_indx], n_aug, MAX_SEQUENCE_LENGTH)
      print('total_augmented_data: {}'.format(len(total_augmented_data)) )
      text = []
      label = []
      for data in total_augmented_data:
          text.append(data)
          label.append(int(i))
      X_train_.extend(text)
      y_train.extend(label)
      with open('train_origin_{}.txt'.format(i), 'w') as f:
            f.write('\n'.join(X_origin[train_indx]))
      with open('total_augmented_{}.txt'.format(i), 'w') as f:
          f.write('\n'.join(total_augmented_data))

    X_train__ = []
    X_val__ = []
    for i in range(len(X_train_)):
        X_train__.append(convert_to_unicode(X_train_[i]))
    
    for i in range(len(X_val_)):
        X_val__.append(convert_to_unicode(X_val_[i])) 
        
    X_train =  tokenizer(X_train__, padding=True, truncation=True, max_length = MAX_SEQUENCE_LENGTH)
    X_val =  tokenizer(X_val__, padding=True, truncation=True, max_length = MAX_SEQUENCE_LENGTH)

    for key in label_count.keys():
        logger.info ("Count of instances with label {} is {}".format(key, label_count[key]))

    if "token_type_ids" not in X_train:
        token_type_ids_train = np.zeros((len(X_train["input_ids"]), MAX_SEQUENCE_LENGTH))
        token_type_ids_val = np.zeros((len(X_val["input_ids"]), MAX_SEQUENCE_LENGTH))
        
    else:
        token_type_ids_train = np.array(X_train["token_type_ids"])
        token_type_ids_val = np.array(X_val["token_type_ids"])
    print('#'*10)
    print('x_train:')
    print(x_train_)
    print('x_val:')
    print(x_val_)
    print("Count of instances with train data is {}".format(len(X_train_)))
    print("Count of instances with valid data is {}".format(len(X_val_)))
 
    return {"input_ids": np.array(X_train["input_ids"]), "token_type_ids": token_type_ids_train, "attention_mask": np.array(X_train["attention_mask"])}, np.array(y_train), {"input_ids": np.array(X_val["input_ids"]), "token_type_ids": token_type_ids_val, "attention_mask": np.array(X_val["attention_mask"])}, np.array(y_val), 

def generate_sequence_data(MAX_SEQUENCE_LENGTH, input_file, tokenizer, unlabeled=False):
    
    X1 = []
    X2 = []
    y = []

    label_count = defaultdict(int)
    with tf.io.gfile.GFile(input_file, "r") as f:
      reader = csv.reader(f, delimiter="\t", quotechar=None)
      for line in reader:
        if len(line) == 0:
          continue
        X1.append(convert_to_unicode(line[0]))
        if not unlabeled:
            label = int(convert_to_unicode(line[-1]))
            y.append(label)
            label_count[label] += 1
        else:
            y.append(-1)
    
    X =  tokenizer(X1, padding=True, truncation=True, max_length = MAX_SEQUENCE_LENGTH)

    for key in label_count.keys():
        logger.info ("Count of instances with label {} is {}".format(key, label_count[key]))

    if "token_type_ids" not in X:
        token_type_ids = np.zeros((len(X["input_ids"]), MAX_SEQUENCE_LENGTH))
    else:
        token_type_ids = np.array(X["token_type_ids"])

    return {"input_ids": np.array(X["input_ids"]), "token_type_ids": token_type_ids, "attention_mask": np.array(X["attention_mask"])}, np.array(y)

