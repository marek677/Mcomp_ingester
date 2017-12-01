import sys

class harness:
	def __init__(self):
		#LOGS
		self.LogContext = ""
		self.LogFunctionName = ""
		self.Logkwargs = []
		#EXCEPTION HANDLER
		self.ExceptionContext = ""
		self.ExceptionFunc = ""
		#FILE_READING COMPONENT
		self.FileContext = ""
		self.FileFunctionName = ""
		self.Filekwargs = []
		self.filebuff = ""
		#PARSING
		self.ParseContext = ""
		self.ParseFunctionName = ""
		self.Parsekwargs = []
		self.parsebuff = ""
		#AGGREGATION
		self.AggregationContext = ""
		self.AggregationFunctionName = ""
		self.Aggregationkwargs = []
		self.Aggregationbuff = ""
		#SENDING
		self.SendingContext = ""
		self.SendingFunctionName = ""
		self.Sendingkwargs = []
	def setExceptionFunction(self,Context, FunctionName):
		self.ExceptionContext = Context
		self.ExceptionFunc = FunctionName
	def Exception(self, arg):
		try:
			func = getattr(self.ExceptionContext, self.ExceptionFunc)
			func(arg)
		except:
			print("Exception() Exception:")
			print(sys.exc_info())
	# LOGGING - set && test
	def setLogFunction(self, Context, FunctionName, **kwargs):
		try:
			self.LogContext = Context
			self.LogFunctionName = FunctionName
			self.Logkwargs = kwargs
		except:
			print("setLogFunction() Exception:")
			self.Exception(sys.exc_info())
	def Log(self, LogText, **kwargs):
		try:
			local_kwargs = dict(kwargs)  # or orig.copy()
			local_kwargs.update(self.Logkwargs) # append one dic to another.
			func = getattr(self.LogContext, self.LogFunctionName)
			func(LogText, **local_kwargs)
		except:
			print("Log() Exception:")
			self.Exception(sys.exc_info())
	# FILE HANDLING - set && test
	def setFileFunction(self, Context, FunctionName, **kwargs):
		try:
			self.FileContext = Context
			self.FileFunctionName = FunctionName
			self.Filekwargs = kwargs
		except:
			print("setLogFunction Exception:")
			self.Exception(sys.exc_info())
	def File(self, filename, **kwargs):
		try:
			local_kwargs = dict(kwargs)  # or orig.copy()
			local_kwargs.update(self.Filekwargs) # append one dic to another.
			func = getattr(self.FileContext, self.FileFunctionName)
			self.filebuff = func(filename, **local_kwargs)
		except:
			print("File() Exception:")
			self.Exception(sys.exc_info())
	# PARSING
	def setParseFunction(self, Context, FunctionName, **kwargs):
		try:
			self.ParseContext = Context
			self.ParseFunctionName = FunctionName
			self.Parsekwargs = kwargs
		except:
			print("setParseFunction Exception:")
			self.Exception(sys.exc_info())
	def Parse(self,**kwargs):
		try:
			local_kwargs = dict(kwargs)  # or orig.copy()
			local_kwargs.update(self.Parsekwargs) # append one dic to another.
			func = getattr(self.ParseContext, self.ParseFunctionName)
			self.parsebuff = func(self.filebuff, **local_kwargs)
		except:
			print("Parse() Exception:")
			self.Exception(sys.exc_info())
	# AGGREGATION
	def setAggregationFunction(self, Context, FunctionName, **kwargs):
		try:
			self.AggregationContext = Context
			self.AggregationFunctionName = FunctionName
			self.Aggregationkwargs = kwargs
		except:
			print("setAggregationFunction Exception:")
			self.Exception(sys.exc_info())
	def Aggregate(self,**kwargs):
		try:
			local_kwargs = dict(kwargs)  # or orig.copy()
			local_kwargs.update(self.Aggregationkwargs) # append one dic to another.
			func = getattr(self.AggregationContext, self.AggregationFunctionName)
			self.Aggregationbuff = func(self.parsebuff, **local_kwargs)
		except:
			print("Aggregation() Exception:")
			self.Exception(sys.exc_info())
	# SENDING
	def setSendingFunction(self, Context, FunctionName, **kwargs):
		try:
			self.SendingContext = Context
			self.SendingFunctionName = FunctionName
			self.Sendingkwargs = kwargs
		except:
			print("setSendingFunction Exception:")
			self.Exception(sys.exc_info())
	def Send(self,**kwargs):
		try:
			local_kwargs = dict(kwargs)  # or orig.copy()
			local_kwargs.update(self.Sendingkwargs) # append one dic to another.
			func = getattr(self.SendingContext, self.SendingFunctionName)
			self.Sendingbuff = func(self.Aggregationbuff, **local_kwargs)
		except:
			print("Send() Exception:")
			self.Exception(sys.exc_info())