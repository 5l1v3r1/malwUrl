import requests
import json
import sqlite3
import socket

DATABASE = 'malwUrl.db'

class Item:
	def __init__(self,ip):
		self.ip = ip
		self.score = int(1)

class ItemList:
	def __init__(self):
		self.hosts = []

	def search(self,item):
		for i in range(len(self.hosts)):
			if self.hosts[i].ip == item.ip:
				return i
		return -1
			

	def addHost(self,item):
		index = self.search(item)
		if index != -1:
			self.hosts[index].score+=1
		else:
			self.hosts.append(item)

	def printList(self):
		for i in self.hosts:
			print i.ip,str(i.score)

ips = ItemList()

def getData(url):
	response = requests.get(url)
	return response.content

def cleanZeros(ip):
	octets = ip.split(".")
	try:
		newIp =  str(int(octets[0])) + "." + str(int(octets[1])) + "." + str(int(octets[2])) + "." +str(int(octets[3]))
		return newIp
	except Exception as e:
		return False
	
def getHostName(url):
	try:
		name = url.split("//")[1].split("/")[0]
		return socket.gethostbyname(name)
	except Exception as e:
		return False

def isIp(str):
	if str.__contains__("/"):
		return False
	else:
		return True

def getDshield():
	url = "https://isc.sans.edu/api/sources/attacks/10000?json"
	data = json.loads(getData(url))
	for i in data:
		temp_ip = cleanZeros(i['ip'])
		if temp_ip != False:
			ip = Item(temp_ip)
			ips.addHost(ip)
	print "Dshield OK"

def writeList(ips):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	cnt = 0
	for i in ips.hosts:
		cnt += 1
		c.execute("insert into url(id,ip,score) values (?,?,?)",[cnt,str(i.ip),i.score])
		conn.commit()
	conn.close()

def getOpenPhish():
	url = "https://openphish.com/feed.txt"
	data = getData(url)
	urls = data.split("\n")
	for i in urls:
		temp_ip = getHostName(i)
		if temp_ip != False:
			temp_ip = cleanZeros(temp_ip)
			if temp_ip != False:
				ips.addHost(Item(temp_ip))
	print "OpenPhish OK"

def getZeusTracker():
	url = "https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist"
	data = getData(url)
	urls = data.split("\n")
	for i in urls:
		if not i.__contains__("#"):
			temp_ip = cleanZeros(i)
			if temp_ip != False:
				ips.addHost(Item(temp_ip))
	print "Zeus OK"

def getUsom():
	url="https://www.usom.gov.tr/url-list.txt"
	data = getData(url)
	urls = data.split("\n")
	for i in urls:
		i = i.replace("\r","")
		if not isIp(i):
			print  i
			temp_ip = socket.gethostbyname(i)
			print temp_ip
			if temp_ip != False:
				ips.addHost(Item(temp_ip))
		else:
			ips.addHost(Item(i))
	print "USOM OK"

#getDshield()
#getOpenPhish()
#getZeusTracker()
getUsom()
#writeList(ips)
print len(ips.hosts)