import usocket as socket
import logger

logger.level = logger.LOG_LEVEL.VERB
log = logger.Logger('http' , logger.LOG_LEVEL.VERB)

def make_form_urlencoded_data(payload):
	#TODO : urlencode the value
	if type(payload) is dict:
		return '&'.join([ '%s=%s' % (key, value) for key,value in payload.items()])
	return ''

import ure as re

status_code_regex = re.compile(r'^HTTP\/1\.1\s(\d+)')
header_regex = re.compile(r'^(.*)\:\s(.*)')

class HttpClient:

	def __init__(self, url):
		host, port, path = urlparse(url)
		self.host = host
		self.port = port
		self.path = path

	def do_request(self, method='GET', payload=None):
		host = self.host
		port = self.port
		path = self.path

		sock = socket.socket()
		addr = socket.getaddrinfo(host, port)[0][-1]
		log.verb('Connecting to: %s' % str(addr))
		sock.connect(addr)		
		stream = sock.makefile('rwb', 0)

		def writeln(msg):
			log.verb('Sending: %s' % msg)
			stream.write( bytes('%s\r\n' % (msg), 'utf-8') )

		writeln('%s %s HTTP/1.1' % (method, path))
		host_string = host if port == 80 else '%s:%s' % (host, port)
		writeln('%s: %s' % ('Host', host_string))
		writeln('User-Agent: deohttp')
		writeln('Accept: */*')
		if method == 'POST':
			if payload:
				writeln('Content-Type: application/x-www-form-urlencoded')
				data = make_form_urlencoded_data(payload)
				_bytes_ = bytes(data, 'utf-8')
				writeln('Content-Length: %s' % len(_bytes_))
				writeln('')
				stream.write(_bytes_)
			else:
				writeln('Content-Length: 0')
				writeln('')
		else:
			writeln('')

		#status code

		response_line = stream.readline()
		log.verb('Received: %s' % response_line)
		line = response_line.decode('utf-8')
		match = status_code_regex.match(line)

		if match:

			status_code = int(match.group(1))
			log.verb('Status Code: %s' % status_code)

		#parsing headers
		headers = {}
		while True:
			response_line = stream.readline()
			log.verb('Received: %s' % response_line)
			if response_line : 
				line = response_line.decode('utf-8')
			else:
				line = None

			if line == '\r\n' or not line:
				break

			match = header_regex.match(line)
			if match:
				key = match.group(1)
				value = match.group(2)

				value = value if value[-2:] != '\r\n' else value[:-2]

				headers[key] = value

		if line:
			try:
				length = int(headers['Content-Length'])
			except Exception as e:
				length = 0

			if length:
				data = stream.read(length)
			else:
				# assuming some small trivial data here
				data = stream.read(100)
			log.verb('Received: %s' % data)
		stream.close()
		return (status_code, headers, data)

def urlparse(url):
	parts = url.split('/', 3)
	# host, port = host.split(':') if ':' in host else (host, 80)
	host = parts[2]
	length = len(parts)
	if length == 4 and parts[3] == '':
		path = '/'
	elif length == 4 and parts[3] != '':
		path = '/' + parts[3]
	elif length == 3:
		path = '/'
	
	if ':' in host:
		host_parts = host.split(':') 
		port = int(host_parts[1])
		host = host_parts[0]
	else:
		port = 80

	# if type(port) == str : port = int(port)
	return (host, port, path)

def get(url):
	host, port, path = urlparse(url)
	s = socket.socket()
	addr = socket.getaddressinfo(host, port)[0][-1]
	s.connect(addr)

if __name__ == '__main__':
	log.verb('Running test')
	client = HttpClient('http://micropython.org/ks/test.html')
	resp = client.do_request()
	print(resp)