# coding:utf-8
import tensorflow as tf
from tqdm import tqdm

tensor = tf.data.Dataset.from_tensor_slices(list(range(100)))

for t in tensor.repeat(100).shuffle(100).padded_batch(7):
    print(t.numpy())

new_tensor = tensor.map(lambda x: x**2).filter(lambda x: x%2==0)
print(new_tensor.prefetch())


flowers = tf.keras.utils.get_file(
    'flower_photos',
    'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
    untar=True)

print(flowers)

example = tf.train.Example()
print(example.features.feature['test'])

