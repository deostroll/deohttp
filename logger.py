class LOG_LEVEL:
	VERB = 0
	ERRR = 1
	WARN = 2
	INFO = 3
	NONE = 5

_levels_ = { 3 : 'INFO', 2 : 'WARN', 1: 'ERRR', 5: 'VERB' }

level = LOG_LEVEL.INFO

def write(module, message, l):
	if module:
		print('%s: (%s) %s' % (l, module, message))
	else:
		print('%s: %s' %(l, message))

def info(message, module=None):
	if level >= LOG_LEVEL.INFO or level == LOG_LEVEL.VERB:
		lstr = 'INFO'
		write(module, message, lstr)

def warn(message, module=None):
	if level >= LOG_LEVEL.WARN or level == LOG_LEVEL.VERB:
		lstr = 'WARN'
		write(module, message, lstr)

def error(message, module=None):
	if level >= LOG_LEVEL.ERRR or level == LOG_LEVEL.VERB:
		lstr = 'ERRR'
		write(module, message, lstr)

def verb(message, module=None):
	if level == LOG_LEVEL.VERB:
		lstr = 'VERB'
		write(module, message, lstr)

class Logger:

	def __init__(self, module, level=LOG_LEVEL.INFO):
		self.level = level
		self.module = module

	def info(self, obj):
		if self.level >= LOG_LEVEL.INFO or level == LOG_LEVEL.VERB:
			lstr = 'INFO'
			write(self.module, str(obj), lstr)

	def error(self, obj):
		if self.level >= LOG_LEVEL.ERRR or level == LOG_LEVEL.VERB:
			lstr = 'ERRR'
			write(self.module, str(obj), lstr)

	def verb(self, obj):
		if self.level == LOG_LEVEL.VERB:
			lstr = 'VERB'
			write(self.module, str(obj), lstr)

	def warn(self, obj):
		if self.level >= LOG_LEVEL.WARN or self.level == LOG_LEVEL.VERB:
			lstr = 'WARN'
			write(self.module, str(obj), lstr)


if __name__ == '__main__':
	level = LOG_LEVEL.VERB
	info('this is a test message')
	warn('this is a warning')
	error('this is an error')
	verb('this is a debug message')

	logger = Logger('main', LOG_LEVEL.VERB)

	logger.info('info')
	logger.warn('warn')
	logger.error('error')
	logger.verb('verbose')


