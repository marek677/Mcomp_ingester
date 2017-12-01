
class ExceptionHandler:
	def __init__(self):
		pass#print "ExceptionHandler Init"
	def DefaultExceptionHandler(self,exc_info):
		print "\tException:",exc_info[1]

class LogClass:
	def __init__(self):
		pass#print "LogClass Init"
	def LogFunction(self,logstr, LogName = "ExampleLog"):
		print "Log - %s: %s" % (LogName,logstr)

#DECLARE GLOBAL INSTANCES
ExceptionHandler = ExceptionHandler()
LogInstance = LogClass()