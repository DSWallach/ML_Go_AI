print("Load up some dataset. skdata is convenient")
from skdata.mnist.view import OfficialVectorClassification
from tqdm import tqdm
import numpy as np
import array
import tensorflow as tf
import random

data = OfficialVectorClassification()

print("data ",data)
print("Training index?")
trIdx = data.sel_idxs[:]

# Must randomly shuffle the data or can't make use
# of tensorflow's great out of core shuffling ?

random.shuffle(trIdx)

writer = tf.python_io.TFRecordWriter("mnist.tfrecords")
print("Iterate over each example")
print("Wrap with tqdm for a progress bar")
all_labels = array.array("q", data.all_labels)
for example_idx in tqdm(trIdx):
    features = array.array("q", data.all_vectors[example_idx])
    label = all_labels[example_idx]

    # Construct example protobuf object 
    """ How the documentation says I should do it
        example = tf.parse_example(
        serialized = [
            features: { 
                feature { key: "label" value { int64_list { value: [label] } } }
                feature { key: "image" value { int64_list { value: features } } }
            }
        ])
    """
    """ How the tutorial says to do it """

    # construct the Example proto boject
    example = tf.train.Example(
        # Example contains a Features proto object
        features=tf.train.Features(
          # Features contains a map of string to Feature proto objects
          feature={
            # A Feature contains one of either a int64_list,
            # float_list, or bytes_list
            'label': tf.train.Feature(
                int64_list=tf.train.Int64List(value=[label])),
            'image': tf.train.Feature(
                int64_list=tf.train.Int64List(value=features)),
    }))
    """ Neither works """


    # Use the proto object to serialize the example to a string
    serialized = example.SerializeToString()
    # Write the serialized object to disk
    writer.write(serialized)