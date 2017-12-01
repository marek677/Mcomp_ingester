import re
import ingester_harness
import sys
import g_global
import json
import time
import threading
from Queue import Queue

'''
HOW TO INTERACT WITH MODULE:
	import syslog_module
	syslog_module.start_thread("thread_name")
	syslog.q.put("filename")
	DONE.

> The idea is that parser is fed one log at the time.		
THINGS TO CONSIDER:
	> Sender Class might be moved to global namespace - it is all the same, just push the data out somewhat.
	> File Handler might not be needed at all - the datasource may vary. <- there will be an option to feed the data directly to Parser
	> If we still need the File Handler -> Move it to global namespace
	> Agregator class might be moved to global namespace - depending on what will be decided.
	So far I am assuming an additional service, which will feed the data into the DB
MORE STUFF - TODO(?):
	> Error/Exception Handling is done in global handler -> therefore, no try statements are needed in this code.
	> Error/Exception Handling is very poor - therefore, stopping an execution might be a good idea somewhere there.
	> Error Reporting is very poor.
	> Figgure out a way to parse HUGE files. Therefore, change the architecture a bit:
		- File Handler loading only a bit of a file, with a while loop checking, if the file has been loaded completly.
		- File Handler loading things to the que, where these would be parsed than.
'''

class FileHandler:
	def __init__(self, harness):
		self.harness = harness
	def Load(self,filename):
		retn = []
		with open("syslog") as f:
			for line in f:
				retn.append(line.replace("\n",""))
		self.harness.Log("LoadFile: %s - %d lines" % (filename, len(retn)))
		return retn
'''
Example log, taken from my VM
Nov 29 12:57:41 dev liblogging-stdlog:  [origin software="rsyslogd" swVersion="8.24.0" x-pid="323" x-info="http://www.rsyslog.com"] rsyslogd was HUPed
Nov 29 12:57:41 dev systemd[1]: Reloading Samba SMB Daemon.
'''
class Parser:
	def __init__(self,harness):
		self.harness = harness
	def Parse(self, data): #data comes from File Handler
		retn = []
		self.harness.Log("Parsing data - %d records" % (len(data)))
		for d in data:
			temp = []
			#TODO: ADD more Months names
			re_result = re.findall(r'((Jan|Nov) ([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}) (.*?) (.*?)\: (.*))',str(d),re.M|re.I)
			for r in re_result:
				retn.append(r[1:])
		return retn
class Aggregator:
	def __init__(self,harness):
		self.harness = harness
	def Aggregate(self, data):
		self.harness.Log("Aggregating - %d records" % (len(data)))
		return json.dumps(data)
class Sender:
	def __init__(self,harness):
		self.harness = harness
	def Send(self,data):
		self.harness.Log("Sending - %d Bytes" % (len(data)))
		#print data		
class syslog_class:
	def __init__(self):
		#CREATE INSTANCES
		self.harness = ingester_harness.harness()
		#unsure, whether these should be saved as self values, or just local values.
		#let it be for now
		self.m_file_handler = FileHandler(self.harness)
		self.m_parser = Parser(self.harness)
		self.m_aggregator = Aggregator(self.harness)
		self.m_sender = Sender(self.harness)
		#LINK GLOBAL CLASSES
		self.harness.setExceptionFunction(g_global.ExceptionHandler,"DefaultExceptionHandler")
		self.harness.setLogFunction(g_global.LogInstance,"LogFunction", LogName = "SYSLOG_MODULE")
		#LINK LOCAL CLASSES
		self.harness.setFileFunction(self.m_file_handler, "Load")
		self.harness.setParseFunction(self.m_parser,"Parse")
		self.harness.setAggregationFunction(self.m_aggregator,"Aggregate")
		self.harness.setSendingFunction(self.m_sender,"Send")
	def run(self,filename):
		self.harness.File(filename)
		self.harness.Parse()
		self.harness.Aggregate()
		self.harness.Send()

threads = []		
q = Queue()
def Worker():
	#Set-up env
	syslog_instance = syslog_class()
	while True:
		item = q.get()
		#here i am assuming, that things pushed down will be filenames
		syslog_instance.run(item)
		q.task_done()
	#"file.txt"
def start_thread(thread_name):
	#Start a thread
	t = threading.Thread(name=thread_name, target=Worker)
	t.daemon = True # so a process could be closed :)
 	t.start()
	threads.append(t)
if __name__ == "__main__":
	#SMALL UNIT TEST?
	start_thread('Syslog_Worker')
	#Fill Q
	q.put("file.txt")
	#Wait until the queue is empty.
	q.join()
	