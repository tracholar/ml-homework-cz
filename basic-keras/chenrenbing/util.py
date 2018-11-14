import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def load_data(path='mnist.npz'):
    """Loads the MNIST dataset.

    # Arguments
        path: path where to cache the dataset locally
            (relative to ~/.keras/datasets).

    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """

    f = np.load(path)
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']
    f.close()
    return (x_train, y_train), (x_test, y_test)

def change_shape(x):
    return np.reshape(x,(28,28))
def show_image(x,x_noisy,y):
    x=change_shape(x)
    x_noisy=change_shape(x_noisy)
    y=change_shape(y)
    imgs=np.concatenate([x,x_noisy,y],axis=0)
    imgs = (imgs * 255).astype(np.uint8)
    print(np.shape(imgs))
    plt.figure()
    plt.axis('off')
    plt.title('Original images: top rows, '
              'Corrupted Input: middle rows, '
              'Denoised Input:  third rows')
    plt.imshow(imgs, interpolation='none', cmap='gray')
    plt.show()
def add_noise(x):
    noise = np.random.normal(loc=0.5, scale=0.5, size=x.shape)
    x_noisy = x+ noise


    x_noisy = np.clip(x_noisy, 0., 1.)
    return x_noisy


def nn_input():
    (x_train,_),(x_test,_)=load_data()

    col,row=np.shape(x_train)[1:]
    x_train=np.reshape(x_train,(np.shape(x_train)[0],784))

    x_test=np.reshape(x_test,(np.shape(x_test)[0],784))
    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255
    x_train_noisy = add_noise(x_train)
    x_test_noisy = add_noise(x_test)
    return x_train,x_train_noisy,x_test,x_test_noisy
def cnn_input():

    (x_train, _), (x_test, _) = load_data(path='mnist.npz')

    image_size = x_train.shape[1]
    x_train = np.reshape(x_train, [-1, image_size, image_size, 1])
    x_test = np.reshape(x_test, [-1, image_size, image_size, 1])
    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255

    x_train_noisy = add_noise(x_train)

    x_test_noisy = add_noise(x_test)
    return x_train,x_train_noisy,x_test,x_test_noisy