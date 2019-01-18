# import tensorflow as tf
# import numpy as np
# import matplotlib as plt
import requests
from bs4 import BeautifulSoup
import os

# m1 = tf.constant([[3, 3]])
# m2 = tf.constant([[2], [3]])
# product = tf.matmul(m1,m2)
# print(product)
# with tf.Session() as sess:
#     result = sess.run(product)
#     print(result)

# x = tf.Variable([1, 2])
# a = tf.constant([3, 3])
# sub = tf.subtract(x, a)
# add = tf.add(x, sub)
# init = tf.global_variables_initializer()
# with tf.Session() as sess:
#     sess.run(init)
#     print(sess.run(sub))
#     print(sess.run(add))

# state = tf.Variable(0, name='counter')
# new_value = tf.add(state, 1)
# # 赋值
# update = tf.assign(state, new_value)
# init = tf.global_variables_initializer()
# with tf.Session() as sess:
#     sess.run(init)
#     print(sess.run(state))
#     for i in range(5):
#         sess.run(update)
#         print(sess.run(state))

# input1 = tf.constant(3.0)
# input2 = tf.constant(2.0)
# input3 = tf.constant(5.0)
#
# add = tf.add(input2, input3)
# mul = tf.multiply(input1, add)
#
# with tf.Session() as sess:
#     result = sess.run([mul, add])
#     print(result)


# input1 = tf.placeholder(tf.float32)
# input2 = tf.placeholder(tf.float32)
# output = tf.multiply(input1, input2)
# with tf.Session() as sess:
#     print(sess.run(output, feed_dict={input1: [7, ], input2: [2, ]}))

# x_data = np.linspace(-0.5, 0.5, 200)[:, np.newaxis]
# noise = np.random.normal(0, 0.02, x_data.shape)
# y_data = np.square(x_data) + noise
#
# x = tf.placeholder(tf.float32, [None, 1])
# y = tf.placeholder(tf.float32, [None, 1])
#
# Weights_Li = tf.Variable(np.random.normal([1, 10]))
# biases_Li = tf.Variable(tf.zeros[1, 10])
# Wx_plus_b_Li = tf.matmul(x,Weights_Li + biases_Li)