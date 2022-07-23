# coding:utf-8
# play music
from IPython.display import Audio

import numpy as np
framerate = 44100
t = np.linspace(0,5,framerate*15)
data = np.sin(2*np.pi*220*t) + np.sin(2*np.pi*224*t)
audio = Audio(data,rate=framerate,autoplay=True)

