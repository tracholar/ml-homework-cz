import tensorflow as tf
import numpy as np

def read_data():
    with open('data/data.csv') as fp:
        for line in fp:
            xarr = line.strip().split(',')
            if len(xarr) != 11:
                continue
            y = float(xarr[-1])
            x = [float(i) for i in xarr[:-1]]
            yield x,y

ds = tf.data.Dataset.from_generator(read_data,
                                    output_types=(tf.float32, tf.float32),
                                    output_shapes=((None, ), ()))\
    .prefetch(100) \
    .batch(32)


print(ds)

for x, y in ds.take(1):
    print(x, y)