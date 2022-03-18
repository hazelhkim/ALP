from transformers import *
import logging
import models
import numpy as np
import os
import tensorflow as tf

logger = logging.getLogger('ST')

def train_model(max_seq_length, X, y, X_val, y_val, X_test, y_test, X_unlabeled, Config=BertConfig, valid_split = -1):

        pt_teacher_checkpoint = 'bert-base-uncased'
        TFModel = "TFBertModel"
        sup_batch_size = 4
        unsup_batch_size = 32
        unsup_size = 4096 # number of pseudo-labeell data during self-training.
        sample_size = 16384  # number of unlabeled dat.
        sup_epochs = 70
        unsup_epochs = 25
        N_base = 10
        dense_dropout = 0.5
        attention_probs_dropout_prob = 0.3
        hidden_dropout_prob = 0.3

        labels = set(y)
        logger.info ("Class labels {}".format(labels))

        # Augment-and-Split method
        if valid_split > 0:
            train_size = int((1. - valid_split)*len(X["input_ids"]))
            X_train, y_train = {"input_ids": X["input_ids"][:train_size], "token_type_ids": X["token_type_ids"][:train_size], "attention_mask": X["attention_mask"][:train_size]}, y[:train_size]

            X_dev, y_dev = {"input_ids": X["input_ids"][train_size:], "token_type_ids": X["token_type_ids"][train_size:], "attention_mask": X["attention_mask"][train_size:]}, y[train_size:]
        # AugTrain-Train method
        else:
            X_train, y_train = X, y
            X_dev, y_dev = X_val, y_val

        strategy = tf.distribute.MirroredStrategy()
        gpus = strategy.num_replicas_in_sync
        logger.info('Number of devices: {}'.format(gpus))

        #Base model for the self-training.
        best_base_model = None
        best_validation_loss = np.inf
        for counter in range(N_base):
            with strategy.scope():
                model = models.construct_teacher(TFModel, Config, pt_teacher_checkpoint, max_seq_length, len(labels), dense_dropout=dense_dropout, attention_probs_dropout_prob=attention_probs_dropout_prob, hidden_dropout_prob=hidden_dropout_prob)
                model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08), loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=[tf.keras.metrics.SparseCategoricalAccuracy(name="acc")])
                if counter == 0:
                    logger.info(model.summary())

            model.fit(x=X_train, y=y_train, shuffle=True, epochs=sup_epochs, validation_data=(X_dev, y_dev), batch_size=sup_batch_size*gpus, callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_acc', patience=5, restore_best_weights=True)])

            val_loss = model.evaluate(X_dev, y_dev)
            logger.info ("Validation loss for run {} : {}".format(counter, val_loss))
            if val_loss[0] < best_validation_loss:
                best_base_model = model
                best_validation_loss = val_loss[0]

        model = best_base_model
        logger.info ("Best validation loss for base model {}: {}".format(best_validation_loss, model.evaluate(X_dev, y_dev)))

        best_val_acc = 0.
        best_test_acc = 0.
        max_test_acc = 0.

        for epoch in range(25):

            logger.info ("Starting loop {}".format(epoch))

            test_acc = model.evaluate(X_test, y_test, verbose=0)[-1]
            val_acc = model.evaluate(X_dev, y_dev, verbose=0)[-1]
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_test_acc = test_acc
            if test_acc > max_test_acc:
                max_test_acc = test_acc

            logger.info ("Test acc {}".format(test_acc))
            if sample_size < len(X_unlabeled["input_ids"]):
                indices = np.random.choice(len(X_unlabeled["input_ids"]), sample_size, replace=True)
                X_unlabeled_sample = {'input_ids': X_unlabeled["input_ids"][indices], 'token_type_ids': X_unlabeled["token_type_ids"][indices], 'attention_mask': X_unlabeled["attention_mask"][indices]}
            else:
                X_unlabeled_sample = X_unlabeled

            logger.info (X_unlabeled_sample["input_ids"][:5])

            y_pred = model.predict(X_unlabeled_sample, batch_size=256)
            y_pred = np.argmax(y_pred, axis=-1).flatten()
            if unsup_size < len(X_unlabeled_sample['input_ids']):
                indices = np.random.choice(len(X_unlabeled_sample['input_ids']), unsup_size, replace=False)
                X_batch, y_batch = {"input_ids": X_unlabeled_sample['input_ids'][indices], "token_type_ids": X_unlabeled_sample['token_type_ids'][indices], "attention_mask": X_unlabeled_sample['attention_mask'][indices]}, y_pred[indices]
            else:
                X_batch, y_batch = X_unlabeled_sample, y_pred

            X_conf = np.ones(len(X_batch['input_ids']))
            logger.info ("Weights ".format(X_conf[:10]))

            model.fit(x=X_batch, y=y_batch, shuffle=True, epochs=unsup_epochs, validation_data=(X_dev, y_dev), batch_size=unsup_batch_size*gpus, sample_weight=X_conf, callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_acc', patience=5, restore_best_weights=True)])

        logger.info ("Test accuracy on the best validation loss {}".format(best_test_acc))
        logger.info ("Best test accuracy {}".format(max_test_acc))
