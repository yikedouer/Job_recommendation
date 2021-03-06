#!usr/bin/env python
# -*- coding:utf-8 -*-
#主函数
from __future__ import division
from getData import getTrainData
from itemCF_IUF import itemCF_IUF_finallyRecommend
from userCF_IIF import userCF_IIF_finallyRecommend
from user_cold_start import *
from show import formatToHtml
import math
import operator
import time

def outToFile(fileName,recommend):
	path='result/'
	outFile=open(path+fileName,'w')
	outFile.write('Jw_SN,Job_SN...\n')
	for u,u_recommend in recommend.items():
		if u_recommend!={}:
			outFile.write(str(u))
			for i,p in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True):
				outFile.write(','+str(i))
			outFile.write("\n")

if __name__ == '__main__':

	start = time.clock()
	nowtime,lastmonth=getTimes()
	nowtime='2016-7-28'
	lastmonth='2016-6-1'
	R_Num=8 #推荐职位数

	#获取数据
	Job_SN=getAllJob_SN(nowtime,lastmonth)#时间段内所有职位
	Jw_SN=getAllJw_SN()#获得所有求职者
	JWINFO,JOB_OFFER=getJWJOBINFO(nowtime,lastmonth)#获得求职者信息及职位信息
	trainData=getTrainData(nowtime,lastmonth)

	getData_time=time.clock()
	print u"getData耗时: %f s" % (getData_time - start)

	#userCF_IIF推荐
	finallyRecommend=userCF_IIF_finallyRecommend(trainData,JWINFO,JOB_OFFER,R_Num)
	userCF_IIF_time=time.clock()
	print u"userCF_IIF耗时: %f s" % (userCF_IIF_time - getData_time)

	#itemCF_IUF推荐
	finallyRecommend=itemCF_IUF_finallyRecommend(trainData,JWINFO,JOB_OFFER,R_Num,finallyRecommend)
	itemCF_IUF_time=time.clock()
	print u"itemCF_IUF耗时: %f s" % (itemCF_IUF_time - userCF_IIF_time)

	del trainData#训练数据销毁

	#most_popular推荐
	finallyRecommend=most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth,JWINFO,JOB_OFFER,R_Num,finallyRecommend)
	most_popular_time=time.clock()
	print u"most_popular耗时: %f s" % (most_popular_time - itemCF_IUF_time)

	#CB_fill推荐
	finallyRecommend=CB_fill_finallyRecommend(Jw_SN,Job_SN,nowtime,lastmonth,JWINFO,JOB_OFFER,R_Num,finallyRecommend)
	CB_fill_time=time.clock()
	print u"CB_fill耗时: %f s" % (CB_fill_time - most_popular_time)

	# for u,u_recommend in finallyRecommend.items():
	# 	print u,sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)

	#结果输出到文件
	outToFile('finallyRecommend.csv',finallyRecommend)

	end = time.clock()
	print u"耗时: %f s" % (end - start)

	#html显示结果
	formatToHtml('finallyRecommend.csv')
