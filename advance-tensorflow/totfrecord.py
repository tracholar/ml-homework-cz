import tensorflow as tf
from tqdm import tqdm

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
                                    output_shapes=((None, ), ()))

def map_fn(x, y):
    idx = range(10)
    feature = {
        'idx' : tf.train.Feature(int64_list=tf.train.Int64List(value=idx)),
        'x' : tf.train.Feature(float_list=tf.train.FloatList(value=x)),
        'target' : tf.train.Feature(float_list=tf.train.FloatList(value=[y]))
    }

    features = tf.train.Features(feature=feature)
    return tf.train.Example(features=features).SerializeToString()

writer = tf.io.TFRecordWriter('./data/tfrecord.data')
for x, y in tqdm(read_data()):
    s = map_fn(x, y)
    writer.write(s)

def decode_fn(record_bytes):
    feature = {
        'idx' : tf.io.VarLenFeature(dtype=tf.int64),
        'x' : tf.io.VarLenFeature(dtype=tf.float32),
        'target' : tf.io.FixedLenFeature([], dtype=tf.float32),
    }
    example = tf.io.parse_single_example(record_bytes, feature)
    return example['idx'], example['x'], example['target']

ds = tf.data.TFRecordDataset('./data/tfrecord.data')
for example in ds.map(decode_fn).batch(32).take(2):
    print(example)