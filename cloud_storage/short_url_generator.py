DEFAULT_ALPHABET = 'mn6j2c4rv8bpygw95z7hsdaetxuk3fq'
DEFAULT_BLOCK_SIZE = 24
MIN_LENGTH = 5

class UrlEncoder(object):
	
	def __init__(self, alphabet=DEFAULT_ALPHABET, block_size=DEFAULT_BLOCK_SIZE):
		self.alphabet = alphabet
		self.block_size = block_size
		self.mask = (1 << block_size) - 1
		self.mapping = range(block_size)
		self.mapping.reverse()
	def encode_url(self, n, min_length=MIN_LENGTH):
		return self.enbase(self.encode(n), min_length)
	def decode_url(self, n):
		return self.decode(self.debase(n))
	def encode(self, n):
		return (n & ~self.mask) | self._encode(n & self.mask)
	def _encode(self, n):
		result = 0
		for i, b in enumerate(self.mapping):
			if n & (1 << i):
				result |= (1 << b)
		return result
	def decode(self, n):
		return (n & ~self.mask) | self._decode(n & self.mask)
	def _decode(self, n):
		result = 0
		for i, b in enumerate(self.mapping):
			if n & (1 << b):
				result |= (1 << i)
		return result
	def enbase(self, x, min_length=MIN_LENGTH):
		result = self._enbase(x)
		padding = self.alphabet[0] * (min_length - len(result))
		return '%s%s' % (padding, result)
	def _enbase(self, x):
		n = len(self.alphabet)
		if x < n:
			return self.alphabet[x]
		return self._enbase(x / n) + self.alphabet[x % n]
	def debase(self, x):
		n = len(self.alphabet)
		result = 0
		for i, c in enumerate(reversed(x)):
			result += self.alphabet.index(c) * (n ** i)
		return result

DEFAULT_ENCODER = UrlEncoder()

def encode(n):
	return DEFAULT_ENCODER.encode(n)

def decode(n):
	return DEFAULT_ENCODER.decode(n)

def enbase(n, min_length=MIN_LENGTH):
	return DEFAULT_ENCODER.enbase(n, min_length)

def debase(n):
	return DEFAULT_ENCODER.debase(n)

def encode_url(n, min_length=MIN_LENGTH):
	return DEFAULT_ENCODER.encode_url(n, min_length)

def decode_url(n):
	return DEFAULT_ENCODER.decode_url(n)

if __name__ == '__main__':
		
	print 'example usage'
	url = DEFAULT_ENCODER.encode_url(12)
	print url
	key = DEFAULT_ENCODER.decode_url(url)
	print key
	
	
	short_uniques = []

	print 'short_uniques', short_uniques	
	print 'searching for uniques...'
	
	for a in range(0, 1000000):
		
		b = encode(a)
		c = enbase(b)
		d = debase(c)
		e = decode(d)
		#print a,'->', b, '->', c, '->', d, '->', e
		
		key = a
		url = DEFAULT_ENCODER.encode_url(key)
		key = DEFAULT_ENCODER.decode_url(url)
		#print 'key:', a,
		#print ', url:', url,
		#print ', key:', key
		
		if not a in short_uniques:
			short_uniques.append(a)
		else:
			import time
			print 'duplicate!! '*10000, key, url
			time.sleep(100)


	