# coding:utf-8
# TF 2.0
import tensorflow as tf
from tqdm import tqdm
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train/255.0, x_test/255.0

print(x_train.shape)
x_train = x_train[..., tf.newaxis].astype('float32')
x_test = x_test[..., tf.newaxis].astype('float32')
print(x_train.shape)


train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(1000).batch(32)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(32, 3, activation='relu')
        self.flatten = Flatten()
        self.d1 = Dense(128, activation='relu')
        self.d2 = Dense(10)

    def call(self, x):
        x = self.conv1(x)
        x = self.flatten(x)
        x = self.d1(x)
        x = self.d2(x)
        return x

model = MyModel()

loss_func = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer = tf.keras.optimizers.Adam()

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_acc = tf.keras.metrics.SparseCategoricalAccuracy(name='train_acc')


test_loss = tf.keras.metrics.Mean(name='test_loss')
test_acc = tf.keras.metrics.SparseCategoricalAccuracy(name='test_acc')

@tf.function
def train_step(images, labels):
    with tf.GradientTape() as trap:
        pred = model(images, training=True)
        loss = loss_func(labels, pred)

    gradients = trap.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_acc(labels, pred)

@tf.function
def test_step(images, labels):
    # training=False is only needed if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    predictions = model(images, training=False)
    t_loss = loss_func(labels, predictions)

    test_loss(t_loss)
    test_acc(labels, predictions)

EPOCH = 5
for epoch in range(EPOCH):
    # reset metrics each iter
    train_loss.reset_states()
    train_acc.reset_states()
    test_loss.reset_states()
    test_acc.reset_states()

    for images, labels in tqdm(train_ds):
        train_step(images, labels)

    for images, labels in tqdm(test_ds):
        test_step(images, labels)

    print(f'Epoch: {epoch + 1}, Loss: {train_loss.result():.4f},',
          f'ACC:  {train_acc.result():.2f}, Test Loss: {test_loss.result():.4f},',
          f'Test ACC: {test_acc.result():.2f}'
          )


model.save('model/mnist_cnn_py')