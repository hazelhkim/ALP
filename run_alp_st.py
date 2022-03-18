from huggingface_utils import MODELS
from preprocessing import generate_sequence_data, generate_train_val_sequence_data
from sklearn.utils import shuffle
from transformers import *
from st import train_model

import argparse
import logging
import numpy as np
import os

# logging
logger = logging.getLogger('ST')
logging.basicConfig(level = logging.INFO)

GLOBAL_SEED = int(os.getenv("PYTHONHASHSEED"))
logger.info ("Global seed {}".format(GLOBAL_SEED))

if __name__ == '__main__':

	# construct the argument parse and parse the arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--n_aug", required=True, type=int)  
	parser.add_argument("--task", required=True, help="data path")
	parser.add_argument("--sup_labels", nargs="?", type=int, default=60, help="total number of labeled samples per class for both training and validation")
	parser.add_argument("--seq_len", default=128, type=int, help="sequence length")
	parser.add_argument("--valid_split", nargs="?", type=float, default=-1, help="percentage of splitting training and validation sets; augTrain-Train method, otherwise")

	args = vars(parser.parse_args())
	logger.info(args)
	task_name = args["task"]
	sup_labels = args["sup_labels"]
	n_aug = args["n_aug"]
	max_seq_length = args["seq_len"]
	valid_split = args["valid_split"]

	for indx, model in enumerate(MODELS):
		if model[0].__name__ == pt_teacher:
			TFModel, Tokenizer, Config = MODELS[indx]

	tokenizer = Tokenizer.from_pretrained(pt_teacher_checkpoint)
	seed = GLOBAL_SEED
	X_train_all, y_train_all, X_val_all, y_val_all = generate_train_val_sequence_data(max_seq_length, task_name +"/real_train.tsv", sup_labels, tokenizer, n_aug, seed)

	X_test, y_test = generate_sequence_data(max_seq_length, task_name + "/real_test.tsv", tokenizer)

	X_unlabeled, _ = generate_sequence_data(max_seq_length, task_name + "/real_transfer.txt", tokenizer, unlabeled=True)

	labels = set(y_train_all)
	for i in labels:
		X_input_ids = X_train_all["input_ids"]
		X_token_type_ids = X_train_all["token_type_ids"]
		X_attention_mask = X_train_all["attention_mask"]
		y_train = np.array(y_train_all)
		X_val_input_ids = X_val_all["input_ids"]
		X_val_token_type_ids = X_val_all["token_type_ids"]
		X_val_attention_mask = X_val_all["attention_mask"]
		y_val = np.array(y_val_all)

        
		X_input_ids, X_token_type_ids, X_attention_mask, y_train = shuffle(X_input_ids, X_token_type_ids, X_attention_mask, y_train, random_state=GLOBAL_SEED)
		X_val_input_ids, X_val_token_type_ids, X_val_attention_mask, y_val = shuffle(X_val_input_ids, X_val_token_type_ids, X_val_attention_mask, y_val, random_state=GLOBAL_SEED)

		X_train = {"input_ids": np.array(X_input_ids), "token_type_ids": np.array(X_token_type_ids), "attention_mask": np.array(X_attention_mask)}
		y_train = np.array(y_train)

		X_val = {"input_ids": np.array(X_val_input_ids), "token_type_ids": np.array(X_val_token_type_ids), "attention_mask": np.array(X_val_attention_mask)}
		y_val = np.array(y_val)

	train_model(max_seq_length, X_train, y_train, X_val, y_val, X_test, y_test, X_unlabeled, Config=Config, valid_split=valid_split)

