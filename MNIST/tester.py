from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf


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

# Lightweight class that stores the training, validation, and testing sets
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# Interactive Session for interleving operations which build a computation
# graph with those that run the graph.
sess = tf.InteractiveSession()

# Create nodes for the input images and target output classes

# 2D tensor of floating point numbers
# 784 is the dimensionality of a single 28 x 28 pixel image
# Input layer
x = tf.placeholder(tf.float32, shape=[None, 784])

# Output layer
y_ = tf.placeholder(tf.float32, shape=[None, 10])

# Model parameters
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))


# Convolve x_image with the weight tensor, add bias
# apply the ReLU function and max pool.
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
x_image = tf.reshape(x, [-1,28,28,1])

# Reduces image size to 14x14
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)


# Second Convolutional Layer
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

# reduce to 7x7
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


# Add a fully connected layer
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1) 


# Apply dropout to reduce overfitting
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# Readout layer
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

# Initialize Variables
#sess.run(tf.global_variables_initializer())
#sess.run(tf.initialize_all_variables())

# Implement regression
#y = tf.matmul(x, W) + b

# Loss function
#cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))

                         
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())
for i in range(200000):
    batch = mnist.train.next_batch(50)
    if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accuracy %g"%(i, train_accuracy))
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
\
print("test accuracy %g"%accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

# Training
#train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# Run the training
#for i in range(1000):
#    batch = mnist.train.next_batch(100)
#    train_step.run(feed_dict={x: batch[0], y_:batch[1]})

# Check the model
#correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_,1))

# Accuracy
#accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#print(accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

