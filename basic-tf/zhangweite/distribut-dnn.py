
## 本程序基于tensorflow官方例程，做了一定的修改与注释
## 运行方式见最下方

import argparse
import sys
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
FLAGS = None

def main(_):
	ps_hosts = FLAGS.ps_hosts.split(",")
	worker_hosts = FLAGS.worker_hosts.split(",")

	# Create a cluster from the parameter server and worker hosts.
	# 定义集群数量、ip以及名称。
	cluster = tf.train.ClusterSpec({"ps": ps_hosts, "worker": worker_hosts})

	# Create and start a server for the local task.
	server = tf.train.Server(cluster,
		job_name=FLAGS.job_name,
		task_index=FLAGS.task_index)

	# 如果当前为ps则进入等待状态，等待集群其余机器的请求。
	if FLAGS.job_name == "ps":
		server.join()
	elif FLAGS.job_name == "worker":

		# Assigns ops to the local worker by default.
		# 定义worker的模型
		with tf.device(tf.train.replica_device_setter(worker_device="/job:worker/task:%d" % FLAGS.task_index,cluster=cluster)):
			tf_x = tf.placeholder(tf.float32, [None, 784])
			tf_y = tf.placeholder(tf.float32, [None, 10])

			l1 = tf.layers.dense(inputs = tf_x, units = 512, activation = tf.nn.relu, name ='l1',
			kernel_initializer = tf.initializers.random_normal(mean=0, stddev=1))
			l2 = tf.layers.dense(inputs = l1, units = 256, activation = tf.nn.relu, name ='l2',
			kernel_initializer = tf.initializers.random_normal(mean=0, stddev=1))
			output = tf.layers.dense(l2, 10)

			loss = tf.losses.softmax_cross_entropy(onehot_labels=tf_y, logits=output) 

			global_step = tf.contrib.framework.get_or_create_global_step()

			train_op = tf.train.AdagradOptimizer(0.01).minimize(loss, global_step=global_step)

		# The StopAtStepHook handles stopping after running given steps.
		# hook相当于时刻监听程序中的状态，对应的作出反应
		# 这里指的是训练1000次后停止
		hooks=[tf.train.StopAtStepHook(last_step=1000)]

		# The MonitoredTrainingSession takes care of session initialization,
		# restoring from a checkpoint, saving to a checkpoint, and closing when done
		# or an error occurs.
		# 监控训练过程，包括执行初始化、模型恢复和模型训练。
		with tf.train.MonitoredTrainingSession(master=server.target,
			is_chief=(FLAGS.task_index == 0),
			checkpoint_dir="/tmp/train_logs",
			hooks=hooks) as mon_sess:
			while not mon_sess.should_stop():
			# Run a training step asynchronously.
			# See `tf.train.SyncReplicasOptimizer` for additional details on how to
			# perform *synchronous* training.
			# mon_sess.run handles AbortedError in case of preempted PS.
				xs, ys = mnist.train.next_batch(100)
				mon_sess.run(train_op, feed_dict = {tf_x: xs,tf_y: ys})

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.register("type", "bool", lambda v: v.lower() == "true")
	# Flags for defining the tf.train.ClusterSpec
	parser.add_argument(
		"--ps_hosts",
		type=str,
		default="172.18.246.128:2220",
		help="Comma-separated list of hostname:port pairs"
	)
	parser.add_argument(
		"--worker_hosts",
		type=str,
		default="172.18.246.128:2221,172.18.246.128:2222",
		help="Comma-separated list of hostname:port pairs"
	)
	parser.add_argument(
		"--job_name",
		type=str,
		default="",
		help="One of 'ps', 'worker'"
	)
	# Flags for defining the tf.train.Server
	parser.add_argument(
		"--task_index",
		type=int,
		default=0,
		help="Index of task within the job"
	)
	FLAGS, unparsed = parser.parse_known_args()
	tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)

	## 以上默认定义了1个ps和2个worker
	## 如果单机跑，ip字段需要修改成本地ip
	## 执行语句：
	## ps0: python distribute-dnn.py --job_name=ps --task_index=0
	## worker0: python distribute-dnn.py --job_name=worker --task_index=0
	## worker1: python distribute-dnn.py --job_name=worker --task_index=1






