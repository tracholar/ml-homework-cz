import tensorflow as tf

example = tf.train.Example()
fl = tf.train.FloatList()
fl.value.append(4.0)
print(dir(example.features.feature))
example.features.feature['test'] = fl
print(example)


