# coding:utf-8
import tensorflow as tf
from tqdm import tqdm

tensor = tf.data.Dataset.from_tensor_slices(list(range(100)))
print(tensor)
print(tensor._graph)


dataset = tf.data.Dataset.list_files('./*.py')
for x in tqdm(dataset):
    print(x.numpy())