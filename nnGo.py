from SGFSerializer import SGFSerializer
import sgf
import numpy as np
from tqdm import tqdm
import random

sgfs = SGFSerializer(19)
sgfs.convertFiles(100000)
print('done')