# coding:utf-8
import os.path
import tensorflow as tf

from tensorflow.python.keras.protobuf import saved_metadata_pb2
from tensorflow.core.protobuf import graph_debug_info_pb2
from tensorflow.core.protobuf import meta_graph_pb2
from tensorflow.core.protobuf import saved_model_pb2
from google.protobuf import message
from google.protobuf import text_format, json_format

print(os.path.abspath('.'))

with open('model/mnist_cnn_py/keras_metadata.pb', 'rb') as f:
    data = f.read()
    saved_metadata = saved_metadata_pb2.SavedMetadata()
    saved_metadata.ParseFromString(data)
    print(saved_metadata)


with open('model/mnist_cnn_py/saved_model.pb', 'rb') as f:
    data = f.read()
    saved_model = saved_model_pb2.SavedModel()
    saved_model.ParseFromString(data)

    with open('tfjs/saved_model.json', 'w') as g:
        print(json_format.MessageToJson(saved_model, indent=4), file=g)

from tensorflow.python.training import py_checkpoint_reader
from tensorflow.python.training.tracking import base
from tensorflow.core.protobuf import trackable_object_graph_pb2
ckpt_reader = py_checkpoint_reader.NewCheckpointReader('model/mnist_cnn_py/variables/variables')
print(ckpt_reader)
tensor_string = ckpt_reader.get_tensor(base.OBJECT_GRAPH_PROTO_KEY)
tog = trackable_object_graph_pb2.TrackableObjectGraph()
tog.ParseFromString(tensor_string)
ckpt_key_to_fullname = {}
for node in tog.nodes:
    for att in node.attributes:
        ckpt_key_to_fullname[att.checkpoint_key] = att.full_name

with open('tfjs/trackable_object_graph.json', 'w') as g:
    print(json_format.MessageToJson(tog, indent=4), file=g)
print(len(tog.nodes))

var_to_shape_map = ckpt_reader.get_variable_to_shape_map()
var_to_dtype_map = ckpt_reader.get_variable_to_dtype_map()
var_to_shape_dtype_map = dict()
for name in var_to_shape_map:
    if name == base.OBJECT_GRAPH_PROTO_KEY:
        continue
    print(ckpt_key_to_fullname[name], var_to_shape_map[name], var_to_dtype_map[name])
    print(ckpt_reader.get_tensor(name))

from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file

print('>>>>>> model tensors: >>>>>>')
# print_tensors_in_checkpoint_file('model/mnist_cnn_py/variables/variables', tensor_name='', all_tensors=True)
print('>>>>>> end >>>>>>')



import tensorflow as tf
load = tf.saved_model.load('model/mnist_cnn_py')
new_model = tf.keras.models.load_model('model/mnist_cnn_py')
print(new_model.summary())


