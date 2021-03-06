#!/usr/bin/python
#coding=utf-8
import urllib2
import MySQLdb
from StringIO import StringIO
import gzip
import json

class FlowCrawler(object):
	def __init__(self, keyword="docker",dbtype="mysql",dbname="crawler"):
		self.dbconnect = DBhelper(dbtype,dbname)
		self.keyword=keyword
		self.baseUrl="http://api.stackexchange.com/2.2/"
	def startCrawler(self, pagesize=50,order="desc",sort="votes"):
		flag=True
		page=1
		while flag:
			flag=self.crawlQuestions(page,pagesize,order,sort)
			page=page+1

	def crawlQuestions(self, page,pagesize,order="desc",sort="votes"):
		url=self.baseUrl+"search?page="+str(page)+"&pagesize="+str(pagesize)+"&order="+order+"&sort="+sort+"&tagged="+self.keyword+"&site=stackoverflow&filter=!6RfQ8AInh-Rr7"
		result=self.getContent(url)
		qList=result["items"]
		for q in qList:
			self.crawlQuestion(q["question_id"])
		return strResult["has_more"]
		
	def crawlQuestion(self,question_id):
		url=self.baseUrl+"questions/"+str(question_id)+"?site=stackoverflow&filter=!mSHi707_rs"
		result=self.getContent(url)
		q=result["items"][0]
		user_id=q["owner"]["user_id"]
		#save question to database
		self.dbconnect.saveQuestion(q)
		#crawl related user
		self.crawlUser(user_id)
		#crawl related comments
		flag=True
		page=1
		while flag:
			flag=self.crawlComments(True,question_id,page)
			page=page+1
			pass
		#crawl related answers
		if q["is_answered"]:
			flag=True
			page=1
			while flag:
				flag=self.crawlAnswers(question_id,page)
				page=page+1
		pass

	def crawlAnswers(self,question_id,page=1,pagesize=50,order="desc",sort="votes"):
		url=self.baseUrl+"questions/"+str(question_id)+"/answers?page="+str(page)+"&pagesize="+str(pagesize)+"&order="+order+"&sort="+sort+"&site=stackoverflow&filter=!6JEiSzNSf8Sdk"
		result=self.getContent(url)
		aList=result["items"]
		for a in aList:
			self.crawlAnswer(a["answer_id"])
		return result["has_more"]

	def crawlAnswer(self,answer_id):
		url=self.baseUrl+'answers/'+str(answer_id)+'?site=stackoverflow&filter=!*Jxe6D(*XyI0WSOD'
		result=self.getContent(url)
		a=result["items"][0]
		user_id=a["owner"]["user_id"]
		#save answer to database
		self.dbconnect.saveAnswer(a)
		#crawl related user
		self.crawlUser(user_id)
		#crawl related comments
		flag=True
		page=1
		while flag:
			flag=self.crawlComments(False,answer_id,page)
			page=page+1
		
		pass

	def crawlUser(self,user_id):
		url=self.baseUrl+"users/"+str(user_id)+"?site=stackoverflow&filter=!40dOQeE6To4*rN*m("
		result=self.getContent(url)
		user=result["items"][0]
		self.dbconnect.saveUser(user)
		pass

	def crawlComments(self,of_question,id,page=1,pagesize=50,order="desc",sort="votes"):
		url=''
		if of_question:
			url=self.baseUrl+"questions/"+str(id)+"/comments?page="+str(page)+"&pagesize="+str(pagesize)+"&order="+order+"&sort="+sort+"&site=stackoverflow&filter=!6JEiSzOmGKjT("
		else:
			url=self.baseUrl+"answers/"+str(id)+"/comments?page="+str(page)+"&pagesize="+str(pagesize)+"&order="+order+"&sort="+sort+"&site=stackoverflow&filter=!9jPV9tT2s";
		result=self.getContent(url)
		cList=result["items"]
		for c in cList:
			self.crawlComment(of_question,c["comment_id"],id)
		return result["has_more"]

	def crawlComment(self,of_question,comment_id,id):
		url=self.baseUrl+"comments/"+str(comment_id)+"?site=stackoverflow&filter=!6JEiSzLdab3D3"
		result=self.getContent(url)
		c=result["items"][0]
		user_id=c["owner"]["user_id"]
		#save comment to database
		self.dbconnect.saveComment(c)
		#crawl related user
		self.crawlUser(user_id)
		

	def getContent(self,url):
		print url
		response=urllib2.urlopen(url)
		buf=StringIO(response.read())
		f=gzip.GzipFile(fileobj=buf)
		data=f.read()
		result=json.loads(data)
		response.close()
		return result

		


class DBhelper(object):
	def __init__(self,dbtype="mysql",dbname="crawler"):
		self.db=MySQLdb.connect("localhost","hello","test1234",dbname)
		pass
	def saveQuestion(self,question):
		pass
	def saveAnswer(self,answer):
		pass
	def saveComment(self,comment):
		print comment
		pass
	def saveUser(self,user):
		print user
	def hasQustion(self,question_id):
		return False
	def hasAnswer(self,answer_id):
		return False
	def hasUser(self,user_id):
		return False
	def hasComment(self,comment_id):
		return False

