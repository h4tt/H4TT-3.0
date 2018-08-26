def signed32(x):
	# Convert number to signed int
	return ((x & 0xFFFFFFFF) ^ 0x80000000) - 0x80000000

def prev_seed(seed):
	# 0xDFE05BCB1365 * 0x5DEECE66D = 1 mod 2^48
	return ((seed - 0xB) * 0xDFE05BCB1365) & ((1 << 48) - 1)

def next_int(seed):
	'''Java Random.nextInt() implementation'''
	s = ((seed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1))

	# Convert number to signed int
	return s, signed32(s >> 16)

def get_seed(n1, n2):
	# Brute force bottom 16 bits to find current seed
	for i in xrange(0x10000):
		seed = (n1 << 16) | i
		s, x = next_int(seed)
		if x == n2:
			return s
	return None

x = 8181022999593810210

# Java's Random.nextLong() = (nextInt() << 32) + nextInt()
num2 = signed32(x & 0xFFFFFFFF)
num1 = signed32((x - num2) >> 32)

cur_seed = get_seed(num1, num2)

if cur_seed is not None:
	print 'Current seed: %lu' % cur_seed
	orig_seed = prev_seed(prev_seed(cur_seed))
	print 'Original seed: %lu' % orig_seed

	# Verify num1 and num2 can be regenerated
	s, x = next_int(orig_seed)
	assert x == num1
	s, x = next_int(s)
	assert x == num2
	assert s == cur_seed
	print 'Sanity check passed'

	s, x1 = next_int(s)
	s, x2 = next_int(s)
	print 'Next long: %lu' % ((x1 << 32) + x2)
else:
	print 'Could not find current seed'
