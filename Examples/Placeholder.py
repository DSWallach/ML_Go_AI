# Feed dict
# Copy the data necessary for each batch through placeholders.abs
# TensorFlow does the work of training the model

import tensorflow as tf

print("Create the batches")
images_batch = tf.placeholder(dtype=tf.float32, shape=[None, 28*28])
labels_batch = tf.placeholder(dtype=tf.int32, shape=[None, ])

# Simple model
print("Create the simple model")
w = tf.get_variable("w1", [28*28, 10])
y_pred = tf.matmul(images_batch, w)
loss = tf.nn.sparse_softmax_cross_entropy_with_logits(y_pred, labels_batch)
loss_mean = tf.reduce_mean(loss)
train_op = tf.train.AdamOptimizer().minimize(loss)

print("Start the session")
sess = tf.Session()
print("Initialize variables")
init = tf.global_variables_initializer()
print("Run the session")
sess.run(init)

print("Load mnist, import numpy")
from skdata.mnist.view import OfficialVectorClassification
import numpy as np

print("Load data entirely into memory")
data = OfficialVectorClassification()
trIdx = data.sel_idxs[:]
features = data.all_vectors[trIdx]
labels = data.all_labels[trIdx]

print("Def data iterator()")
def data_iterator():
    """ A simple data iterator """
    batch_idx = 0
    while True:
        print("Shuffle labels and features")
        idxs = np.arange(0, len(features))
        np.random.shuffle(idxs)
        shuf_features = features[idxs]
        shuf_labels = labels[idxs]
        batch_size = 128
        for batch_idx in range(0, len(features), batch_size):
            images_batch = shuf_features[batch_idx:batch_idx+batch_size] / 255.
            images_batch = images_batch.astype("float32")
            labels_batch = shuf_labels[batch_idx:batch_idx+batch_size]
            yield images_batch, labels_batch

print("Initialize iter_")
iter_ = data_iterator()

while True:
    print("Get a batch of data")
    images_batch_val, labels_batch_val = next(iter_)
    print("Pass it in as through feed_dict")
    _, loss_val = sess.run([train_op, loss_mean], feed_dict={
        images_batch:images_batch_val,
        labels_batch:labels_batch_val
    })
    print(loss_val)