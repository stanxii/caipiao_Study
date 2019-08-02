# coding=utf-8
"""
　　__title__ = ''
　　__file__ = ''
　　__author__ = 'tianmuchunxiao'
　　__mtime__ = '2019/7/16'
"""

import get_data
import pandas as pd
import tensorflow as tf
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

print(tf.__version__)

