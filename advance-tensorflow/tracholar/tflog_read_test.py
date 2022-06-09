# coding:utf-8
# 读取tflog数据
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator, event_file_loader
from tensorboard.compat.proto.event_pb2 import Event
from google.protobuf.json_format import MessageToJson

evt = EventAccumulator('./log/train/')
evt.Reload()
print(evt.Tags())
print(evt.Tensors('loss'))
print(evt.Tensors('acc'))

loss = evt.Tensors('loss')[0]

print(float(loss.tensor_proto.tensor_content))
print(MessageToJson(loss.tensor_proto, indent=4))

