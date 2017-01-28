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

sess = tf.Session()

# Initialize Variables
init = tf.global_variables_initializer()
sess.run(init)
tf.train.start_queue_runners(sess=sess)

# Grab examples 
# First example from file
label_val_1, image_val_1 = sess.run([label, image])
print(label_val_1, image_val_1)
print()
# Second example from file
label_val_2, image_val_2 = sess.run([label, image])
print(label_val_2, image_val_2)
print()