# coding=utf-8
"""
　　__title__ = ''
　　__file__ = ''
　　__author__ = 'tianmuchunxiao'
　　__mtime__ = '2019/7/16'
"""

import requests
import pandas as pd
from lxml import etree
from multiprocessing import Pool

def get_ssq():
	PARAMS = {
		'start': '03001',
		'end': '99081'
		}
	
	URL = 'https://datachart.500.com/ssq/history/newinc/history.php'
	
	HEADERS = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
		'Connection': 'keep-alive',
		'Host': 'datachart.500.com',
		'Referer': 'https://datachart.500.com/ssq/history/history.shtml',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		              'Chrome/75.0.3770.142 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest'
		}
	columns = ['期号', '红1', '红2', '红3', '红4', '红5', '红6', '蓝球', '快乐星期天', '奖池资金（元）', '一等奖注数', '一等奖资金（元）', '二等奖注数',
	           '二等奖资金（元）', '总投注额(元)', '开奖日期']
	print('正在获取双色球数据...')
	response = requests.get(url=URL, params=PARAMS, headers=HEADERS)
	print('正在处理双色球数据...')
	html = etree.HTML(response.text)
	tr_tags = html.xpath('//*[@id="tdata"]/tr')
	data_df = pd.DataFrame(columns=columns)
	for tr in tr_tags:
		text_list = list(tr.xpath('./td/text()'))
		data = {}
		for i in range(len(columns)):
			data[columns[i]] = text_list[i]
		data['奖池资金（元）'] = int(data['奖池资金（元）'].replace(',', ''))
		data['一等奖资金（元）'] = int(data['一等奖资金（元）'].replace(',', ''))
		data['二等奖资金（元）'] = int(data['二等奖资金（元）'].replace(',', ''))
		data['总投注额(元)'] = int(data['总投注额(元)'].replace(',', ''))
		data['快乐星期天'] = data['快乐星期天'].replace('\xa0', '')
		data_df = data_df.append(data,
		                         ignore_index=True)
	data_df.sort_values(by='开奖日期',
	                    ascending=True,
	                    inplace=True)
	print('正在保存双色球数据...')
	data_df.to_csv('F:/Caipaio_Data/ssq.csv', encoding='gbk', index=False)
	print('双色球数据保存完成！')
	
def get_caojidaletou():
	PARAMS = {
		'start': '07001',
		'end': '99999'
		}
	
	URL = 'http://datachart.500.com/dlt/history/newinc/history.php'
	
	HEADERS = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
		'Connection': 'keep-alive',
		'Host': 'datachart.500.com',
		'Referer': 'https://datachart.500.com/dlt/history/history.shtml',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		              'Chrome/75.0.3770.142 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest'
		}
	columns = ['期号', '前1', '前2', '前3', '前4', '前5', '后1', '后2', '奖池资金（元）', '一等奖注数', '一等奖资金（元）', '二等奖注数',
	           '二等奖资金（元）', '总投注额(元)', '开奖日期']
	print('正在获取大乐透数据...')
	response = requests.get(url=URL, params=PARAMS, headers=HEADERS)
	print('正在处理大乐透数据...')
	html = etree.HTML(response.text)
	tr_tags = html.xpath('//*[@id="tdata"]/tr')
	data_df = pd.DataFrame(columns=columns)
	for tr in tr_tags:
		text_list = list(tr.xpath('./td/text()'))
		data = {}
		for i in range(len(columns)):
			data[columns[i]] = text_list[i]
		data['奖池资金（元）'] = int(data['奖池资金（元）'].replace(',', ''))
		data['一等奖资金（元）'] = int(data['一等奖资金（元）'].replace(',', ''))
		data['二等奖资金（元）'] = int(data['二等奖资金（元）'].replace(',', ''))
		data['总投注额(元)'] = int(data['总投注额(元)'].replace(',', ''))
		data_df = data_df.append(data,
		                         ignore_index=True)
	data_df.sort_values(by='开奖日期',
	                    ascending=True,
	                    inplace=True)
	print('正在保存大乐透数据...')
	data_df.to_csv('F:/Caipaio_Data/cjdlt.csv', encoding='gbk', index=False)
	print('大乐透数据保存完成！')
	

def main():
	pool = Pool(2)
	pool.apply_async(func=get_ssq)
	pool.apply_async(func=get_caojidaletou)
	pool.close()
	pool.join()
	print('全部彩票数据保存完成！')

if __name__ == '__main__':
    main()
