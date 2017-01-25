import tensorflow as tf
import array
import numpy as np
from tqdm import tqdm

def some_decoder(record_string):
    """ Reads in a .sgf file and converts it into a TrainingGame object """
    return 

def some_processing(example):
    """ Takes a TrainingGame object and processes it into training examples """
    print("Stuff")
    return example

def read_my_file_format(filename_queue):
    """ Reads in all the files in the queue and converts them to a training binary """
    reader = tf.WholeFileReader("SGF-Reader")
    key, record_string = reader.read(filename_queue)
    print(key, record_string)
    example, label = tf.string_split(record_string, ';')
    print(example, label)
    #processed_example = some_processing(example)
    #return processed_example, label

def input_pipeline(filenames, batch_size, read_threads, num_epochs=None):
    """ Training Pipline for files """
    filename_queue = tf.train.string_input_producer(
        filenames, num_epochs=num_epochs, shuffle=True)
    example_list = [read_my_file_format(filename_queue)
                    for _ in range(read_threads)]
    min_after_dequeue = 10000
    capacity = min_after_dequeue + 3 * batch_size
    example_batch, label_batch = tf.train.shuffle_batch_join(
        example_list, batch_size=batch_size, capacity=capacity,
        min_after_dequeue=min_after_dequeue)
    return example_batch, label_batch

def make_filename_queue(num_names):
    """ Create a list of filenames """
    files = list()
    for i in tqdm(range(num_names)):
        files.append(str(i)+"game.sgf")
    return tf.train.string_input_producer(files, num_epochs=1)

filenames = make_filename_queue(10) #110599
read_my_file_format(filenames)