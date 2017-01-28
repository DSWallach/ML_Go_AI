import tensorflow as tf

def read_and_decode_single_example(filename):
    # Construct a queue containing a list of filenames
    # Allows user to split the data up into multiple files
    filename_queue = tf.train.string_input_producer([filename],
                                                    num_epochs=None)
    # Unlike TFRecordWriter, the TFRecordReader is symbolic
    reader = tf.TFRecordReader()

    # One can read a single serialized example from a filename
    # serialized_example is a Tensor of type string. 
    _, serialized_example = reader.read(filename_queue)

    # The serialized example is converted back to actual values
    # One needs to describe the format of the objects to be returned
    features = tf.parse_single_example(
        serialized_example,
        features = {
            'label': tf.FixedLenFeature([], tf.int64),
            'image': tf.FixedLenFeature([784], tf.int64)
    })
    # Now return the converted data
    label = features['label']
    image = features['image']

    return label, image

# Returns the symbolic label and image
label, image = read_and_decode_single_example("mnist.tfrecords")

image = tf.cast(image, tf.float32) / 255.

# Group examples into batches randomly
images_batch, labels_batch = tf.train.shuffle_batch(
    [image, label], batch_size = 128,
    capacity = 2000,
    min_after_dequeue = 1000
)

# Simple model
w = tf.get_variable("w1", [28*28, 10])
y_pred = tf.matmul(images_batch, w)
loss = tf.nn.sparse_softmax_cross_entropy_with_logits(y_pred, labels_batch)

# For monitoring
loss_mean = tf.reduce_mean(loss)

train_op = tf.train.AdamOptimizer().minimize(loss)

sess = tf.Session()

# Initialize Variables
init = tf.global_variables_initializer()
sess.run(init)
tf.train.start_queue_runners(sess=sess)
count = 0
while True:
    # Pass it through feed_dict
    _, loss_val = sess.run([train_op, loss_mean])
    if count%100 == 0 and loss_val < 0.1:
        break
    count += 1
print("Finished with loss_val = "+str(loss_val))