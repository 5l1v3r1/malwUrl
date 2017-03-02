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


def cleanZeros(ip):
	octets = ip.split(".")
	return str(int(octets[0])) + "." + str(int(octets[1])) + "." + str(int(octets[2])) + "." +str(int(octets[3]))

def getHostName(url):
	import socket
	name = url.split("//")[1].split("/")[0]
	try:
		print name,socket.gethostbyname(name)
	except Exception as e:
		print name,"err"
	

iplist = ["0.0.0.0","012.095.025.254","12.0.24.10"]

for i in iplist:
	print cleanZeros(i)