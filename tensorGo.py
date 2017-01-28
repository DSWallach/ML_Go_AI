from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import argparse
import os.path
import sys
import time
import GoGame as gg
import IllegalMove as im
import numpy as np
import random

print("Populating name_list")
for i in tqdm(range(25000)):
    name_list.append("/home/david/Documents/gameFiles/CSV-19x19/data"+str(i)+".csv")


filename_queue = tf.train.string_input_producer(name_list)

reader = tf.TextLineReader()
key, value = reader.read(filename_queue)

# Default values, in case of empty columns. Also specifies the type of the
# decoded result.

print("Initialize columns")
columns = [[0] for x in tqdm(range(723))]
#print(columns)
print("Initialize Features")
features = [0 for x in tqdm(range(361))]
#print(features)
columns = tf.decode_csv(value, record_defaults=columns)
#print(columns)
print("Populating solutions")
solutions = [columns[x] for x in tqdm(range(362, 723))]
#print(solutions)

BOARD_LENGTH = 19
BOARD_SIZE = BOARD_LENGTH * BOARD_LENGTH

# FUNCTIONS
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def run_training():

    # Lightweight class that stores the training, validation, and testing sets
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

    # Interactive Session for interleving operations which build a computation
    # graph with those that run the graph.
    sess = tf.InteractiveSession()

    # Get the time at the start of the session.
    t0 = time.clock()

    if FLAGS.load_graph:
        # Saver for saving a loaded graph
        saver = tf.train.import_meta_graph(FLAGS.graph_name+'.meta')

        # Load the saved graph
        saver.restore(sess, tf.train.latest_checkpoint('./'))

        # Load the saved vars
        all_vars = tf.get_collection(FLAGS.graph_name+'-vars')

        # Load vars into variable names
        W = all_vars[0]
        b = all_vars[1]

    else:
        # Model parameters
        W = tf.Variable(tf.zeros([BOARD_LENGTH * BOARD_LENGTH, 0]))
        b = tf.Variable(tf.zeros([BOARD_LENGTH * BOARD_LENGTH, 0]))
        #W = tf.Variable(tf.zeros([784, 10]))
        #b = tf.Variable(tf.zeros([10]))

        # Add Variables to the collection for saving
        tf.add_to_collection(FLAGS.graph_name+'-vars', W)
        tf.add_to_collection(FLAGS.graph_name+'-vars', b)

        # Saver for saving a new graph
        saver = tf.train.Saver()

    # Create nodes for the input images and target output classes    
    # 2D tensor of floating point numbers
    # Input layer
    x = tf.placeholder(tf.float32, shape=[BOARD_LENGTH, BOARD_LENGTH])
    #x = tf.placeholder(tf.float32, shape=[None, 784])

    # Output layer
    y_ = tf.placeholder(tf.float32, shape=[BOARD_LENGTH, BOARD_LENGTH])
    #y_ = tf.placeholder(tf.float32, shape=[None, 10])

    # Initialize Variables
    sess.run(tf.global_variables_initializer())

    # Implement regression
    y = tf.matmul(x, W) + b

    # Loss function
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))

    # Training
    train_step = tf.train.GradientDescentOptimizer(FLAGS.learning_rate).minimize(cross_entropy)

    gg.play_go(BOARD_LENGTH)
    # Run the training
    for i in range(FLAGS.max_steps):
        batch = mnist.train.next_batch(100)
        train_step.run(feed_dict={x: batch[0], y_:batch[1]})

    # Check the model
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

    # Accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Get the time at the end
    t1 = time.clock()

    # Get the elapsed time
    tFinal = t1 - t0

    # Print the elapsed time 
    print("Elapsed time = "+ str(tFinal)+ " seconds")
    # Print the accuracy of the classifier
    print("Accuracy = "+
          str(accuracy.eval(feed_dict={
            x: mnist.test.images,
            y_: mnist.test.labels}))+" / 1")

    # Save the trained model
    saver.save(sess, 'Tensor-Go')

    # For curiousness
    print(x)
    print(y_)

# Convolve x_image with the weight tensor, add bias
# apply the ReLU function and max pool.
def main(_):
  if tf.gfile.Exists(FLAGS.log_dir):
    tf.gfile.DeleteRecursively(FLAGS.log_dir)
  tf.gfile.MakeDirs(FLAGS.log_dir)
  run_training()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--learning_rate',
      type=float,
      default=0.01,
      help='Initial learning rate.'
  )
  parser.add_argument(
      '--max_steps',
      type=int,
      default=2000,
      help='Number of steps to run trainer.'
  )
  parser.add_argument(
      '--hidden1',
      type=int,
      default=128,
      help='Number of units in hidden layer 1.'
  )
  parser.add_argument(
      '--hidden2',
      type=int,
      default=32,
      help='Number of units in hidden layer 2.'
  )
  parser.add_argument(
      '--batch_size',
      type=int,
      default=100,
      help='Batch size.  Must divide evenly into the dataset sizes.'
  )
  parser.add_argument(
      '--input_data_dir',
      type=str,
      default='/tmp/tensorGo/input_data',
      help='Directory to put the input data.'
  )
  parser.add_argument(
      '--log_dir',
      type=str,
      default='/tmp/tensorGo/logs/fully_connected_feed',
      help='Directory to put the log data.'
  )
  parser.add_argument(
      '--fake_data',
      default=False,
      help='If true, uses fake data for unit testing.',
      action='store_true'
  )
  parser.add_argument(
      '--load_graph',
      default=False,
      help='If true, loads the prvious model named $FLAGS.model_name',
  )
  parser.add_argument(
      '--graph_name',
      default='Tensor-Go',
      help='The name of the graph to be loaded'
  )

  FLAGS, unparsed = parser.parse_known_args()
tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
