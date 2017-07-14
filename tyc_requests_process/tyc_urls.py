# -*- coding:utf-8 -*-
#17975家公司
import pymysql
from urllib import quote
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def put_db(name,number,url):
	name = str(name)
	number = str(number)
	url = str(url)
	try:
		conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='test', port=3306, charset='utf8')
		cur1 = conn.cursor()
		sql = "INSERT INTO tyc_sid_urls (name,number,url)VALUES(%s,%s,%s)"
		cur1.execute(sql,(name,number,url))
		conn.commit()
		print name + '的id是' + number
	except Exception as e:
		print(u"导入异常%s"%e)
	finally:
		cur1.close()
		conn.close()

def get_url(company):
	url = r'http://www.tianyancha.com/v2/search/%s.json?'
	a = quote(company)
	url1 = url %a
	try:
		try:
			proxy = {'http':'http://117.143.109.173:80'}
			response = requests.get(url1,proxies=proxy)
		except:
			print(u'代理异常')
		else:
			id = ((json.loads(response.text)["data"])[0])["id"]
			id = str(id)
			c_url = 'http://www.tianyancha.com/company/'+id
			put_db(company, id, c_url)
	except:
		comp = str(company)
		print(u'%s不存在' %comp)
	else:
		print(u'获取成功')


def get_db():
	try:
		conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='tyc', port=3306, charset='utf8')
		cur = conn.cursor()
		sql = "SELECT name FROM tyc_no_company"
		cur.execute(sql)
		conn.commit()
		companys = cur.fetchall()
		print len(companys)
	except Exception as e:
		print(u"导出异常%s"%e)
	finally:
		cur.close()
		conn.close()
		for company in companys:
			company = str(company[0].encode('utf-8').strip())
			get_url(company)


if __name__=='__main__':
    get_db()
