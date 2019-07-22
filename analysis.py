# coding=utf-8
"""
　　__title__ = ''
　　__file__ = ''
　　__author__ = 'tianmuchunxiao'
　　__mtime__ = '2019/7/16'
"""

import get_data
import pandas as pd
import tensorflow.compat.v1 as tf
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from numpy.random import RandomState

ssq_df = pd.read_csv('F:/Caipaio_Data/ssq.csv', encoding='gbk')

columns = ['期号', '红1', '红2', '红3', '红4', '红5', '红6', '蓝球', '快乐星期天', '奖池资金（元）', '一等奖注数', '一等奖资金（元）', '二等奖注数',
	           '二等奖资金（元）', '总投注额(元)', '开奖日期']
imput_title = ['红1', '红2', '红3', '红4', '红5', '红6', '蓝球', '奖池资金（元）', '一等奖注数', '一等奖资金（元）', '二等奖注数',
	           '二等奖资金（元）', '总投注额(元)']
ssq_df['蓝球'] = ssq_df['蓝球'] + 33
data_df = ssq_df[['红1', '红2', '红3', '红4', '红5', '红6', '蓝球']]
one_hot_columns = list(range(1, 50))
data_list = []
for row in data_df.values:
	data = np.zeros([49], dtype=np.float32)
	for i in range(len(row)):
		data[row[i] - 1] = 1
	data_list.append(data)
data_df = pd.DataFrame(data_list, columns=one_hot_columns)


batch_size = 50

x = tf.placeholder(tf.float32, shape=(None, 49))
y_ = tf.placeholder(tf.float32, shape=(None, 49))

Weigth_1 = tf.Variable(tf.random_normal([49, 49], stddev=1, seed=1))
biase_1 = tf.Variable(tf.zeros(49))
layer_1 = tf.sigmoid(tf.matmul(x, Weigth_1) + biase_1)

Weigth_2 = tf.Variable(tf.random.normal([49, 49], stddev=1, seed=1))
biase_2 = tf.Variable(tf.zeros(49))
layer_2 = tf.sigmoid(tf.matmul(x, Weigth_1) + biase_1)

loss = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(layer_2, 1e-10, 1.0)) + (1-layer_2)*tf.log(tf.clip_by_value(1-layer_2, 1e-10, 1.0)))
train_step = tf.train.AdadeltaOptimizer(0.001).minimize(loss)

init_op = tf.global_variables_initializer()

with tf.Session() as sess:
	sess.run(init_op)
	
	for i in range(len(data_df) - 101):
		start = i
		end = i + 100
		X = np.array(data_df[start:end])
		print(X)
		Y = np.array(data_df.loc[i + 100]).reshape(1,49)
		
		sess.run(train_step,
		         feed_dict={x: X, y_: Y})
		
		if i %200==0:
			print(sess.run(loss, feed_dict={x:X,y_:Y}))
	
	prediction = sess.run(layer_2, feed_dict={x:data_df[-101:-1]})
	
	pred = list(prediction[-1])
	num_list = []
	for i in range(10):
		index = pred.index(max(pred))
		pred[index] = 0
		num = index + 1
		print(num)
		num_list.append(num)
	num_list.sort()
	print(num_list)
		
		
		
