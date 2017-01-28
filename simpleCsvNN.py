import tensorflow as tf
from tqdm import tqdm
import random

name_list = list()
print("Populating name_list")
for i in tqdm(range(25000)):
    name_list.append("/home/david/Documents/gameFiles/CSV-19x19/data"+str(i)+".csv")


filename_queue = tf.train.string_input_producer(name_list, shuffle=True)

reader = tf.TextLineReader()
key, value = reader.read(filename_queue)

# Default values, in case of empty columns. Also specifies the type of the
# decoded result.

print("Initialize columns")
columns = [[0] for x in tqdm(range(723))]
#print(columns)
print("Initialize Features")
feat = [0 for x in tqdm(range(361))]
#print(features)
columns = tf.decode_csv(value, record_defaults=columns)
#print(columns)
print("Populating solutions")
solutions = [columns[x] for x in tqdm(range(362, 723))]
#print(solutions)

features = tf.pack(feat)

with tf.Session() as sess:
  # Start populating the filename queue.
  coord = tf.train.Coordinator()
  threads = tf.train.start_queue_runners(coord=coord)

  print("Training")
  for i in range(25000):
    # Retrieve a single instance:
    example, label = sess.run([features, solutions])

  coord.request_stop()
  coord.join(threads)