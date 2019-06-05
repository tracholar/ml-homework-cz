#coding:utf-8

import tensorflow as tf
import numpy as np
import gym



# input state
obs_placeholder = tf.placeholder(dtype=tf.float32, shape=(None, 4))
obs_new_placeholder = tf.placeholder(dtype=tf.float32, shape=(None, 4))


with tf.variable_scope('dqn'):
    h1 = tf.layers.dense(obs_placeholder, 16, activation=tf.nn.relu, kernel_initializer=tf.truncated_normal_initializer(stddev=0.7), name='hidden1')
    q = tf.layers.dense(h1, 2, name='q')

## set target net trainable to False
with tf.variable_scope('dqn_target'):
    h2 = tf.layers.dense(obs_new_placeholder, 16, activation=tf.nn.relu, kernel_initializer=tf.truncated_normal_initializer(stddev=0.7), trainable=False, name='hidden1')
    q_target = tf.layers.dense(h2, 2, trainable=False, name='q')

vars1 = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='dqn')
vars2 = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='dqn_target')
vars1 = sorted(vars1, key=lambda x: x.name)
vars2 = sorted(vars2, key=lambda x: x.name)

update_list = []
for v1, v_target in zip(vars1, vars2):
    update_list.append(v_target.assign(v1))
update_target_op = tf.group(*update_list)

var_w = tf.reduce_mean([tf.reduce_mean(v*v) for v in vars1])


act_placeholder = tf.placeholder(dtype=tf.int64, shape=(None, ))
rew_placeholder = tf.placeholder(dtype=tf.float32, shape=(None, ))
done_placeholder = tf.placeholder(dtype=tf.bool, shape=(None, ))

act_onehot = tf.one_hot(act_placeholder, 2)
pred_q = tf.reduce_sum(q * act_onehot, axis=1)
target_q = rew_placeholder + tf.cast(done_placeholder, dtype=tf.float32) * tf.reduce_max(q_target, axis=1)  # gamma = 1

print pred_q.shape, target_q.shape
loss = tf.reduce_sum((pred_q - target_q)**2) + 1e-2*var_w

adam = tf.train.AdamOptimizer(1e-3)
step = tf.Variable(0, trainable=False)
train_op = adam.minimize(loss, var_list=vars1, global_step=step)

tf.GraphKeys
class ExpBuffer():
    def __init__(self, max_size=10240):
        self.buff = []
        self.max_size = max_size

    def reset(self):
        self.buff = []

    @property
    def size(self):
        return len(self.buff)
    def append(self, data):
        """
        :param data: (s, a, r, s', done)
        :return:
        """
        assert len(data) == 5
        if self.size >= self.max_size:
            self.buff.pop(0)
        self.buff.append(data)

    def sample(self, batch_size = 32):
        idx = np.random.randint(0, self.size, size=(batch_size))
        obs = []
        act = []
        rew = []
        obs_new = []
        done = []

        for i in idx:
            x = self.buff[i]
            obs.append(x[0])
            act.append(x[1])
            rew.append(x[2])
            obs_new.append(x[3])
            done.append(x[4])

        return obs, act, rew, obs_new, done


exp_buffer = ExpBuffer()
epsilon = 1

import gym
env = gym.make('CartPole-v1')


observation = env.reset()

init_op = tf.global_variables_initializer()
avg_reward = 0
max_reward = 0
cum_reward = 0
alpha = 0.95
with tf.Session() as sess:
    sess.run([init_op])

    for i in range(1024000):
        if np.random.rand() < epsilon: ## epsilon greedy
            action = env.action_space.sample()
        else:
            qv, = sess.run([q], feed_dict={obs_placeholder: np.array(observation).reshape((1, 4))})
            action = np.argmax(qv.squeeze())

        obs_new, reward, done, info = env.step(action)
        cum_reward += reward
        exp_buffer.append((observation, action, reward, obs_new, done))
        observation = obs_new

        if done:
            observation = env.reset()
            avg_reward = avg_reward * alpha + cum_reward * (1 - alpha)
            max_reward = max(max_reward, cum_reward)
            cum_reward = 0

        if i < 128:
            continue

        obs, act, rew, obsn, doneb  = exp_buffer.sample(32)

        _, l, istep = sess.run([train_op, loss, step], feed_dict={
            obs_placeholder: obs,
            act_placeholder: act,
            rew_placeholder: rew,
            obs_new_placeholder: obsn,
            done_placeholder: doneb
        })

        if (i+1) % 1024 == 0:
            print istep, 'update target, loss =', l, 'epsilon=', epsilon,\
                'avg_reward=', avg_reward,\
                'max_reward=',max_reward,\
                'var_weight=', sess.run(var_w)
            sess.run([update_target_op])

            epsilon *= 0.99
            #epsilon = max(epsilon, 0.1)





