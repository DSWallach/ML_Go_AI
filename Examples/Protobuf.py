print("Load up some dataset. skdata is convenient")
from skdata.mnist.view import OfficialVectorClassification
from tqdm import tqdm
import numpy as np
import tensorflow as tf

print("data")
data = OfficialVectorClassification()
print("Training index?")
trIdx = data.sel_idxs[:]

# Must randomly shuffle the data or can't make use
# of tensorflow's great out of core shuffling ?

np.random.shuffle(trIdx)

writer = tf.python_io.TFRecordWriter("mnist.tfrecords")
print("Iterate over each example")
print("Wrap with tqdm for a progress bar")
for example_idx in tqdm(trIdx):
    features = data.all_vectors[example_idx].astype("int")
    label = int(data.all_labels[example_idx])

    # Construct example protobuf object 
    example = tf.train.Example(
        # Example contains a Features proto object
        features = tf.train.Features(
            # Features contains a map of string to Feature proto objects
                # A Feature contains one of either a int64_list,
                # float_list, or bytes_list
            feature={
                'label': tf.train.Feature(
                    int64_list = tf.train.Int64List(value = [label])),
                'image': tf.train.Feature(
                    int64_list = tf.train.Int64List(value = features)),
            }
        )
    )
    # Use the proto object to serialize the example to a string
    serialized = example.SerializeToString()
    # Write the serialized object to disk
    writer.write(serialized)