import primes

def tau(n):
	'''the number-theoretic method for computing the number of factors of n'''
	p = primes.pf(n)
	product = 1
	for i in range(len(p)):
		product*= (p[i][1]+1)
	return product

def sigma(n):
	'''the number-theoretic method for computing the sum of the factors of n'''
	if n == 0:
		return 0 
	else:
		product = 1
		p = primes.pf(n)
		for i in range(len(p)):
			product *= ((p[i][0]**(p[i][1]+1))-1)/(p[i][0]-1)
		return product

def nu(n):
	'''sigma/n.'''
	return sigma(n)/float(n)

def isab(n):
	'''test whether or not a number is abundant'''
	if nu(n)>2:
		return True
	else:
		return False
		
def isper(n):
	'''test whether n is perfect'''
	if nu(n)==2:
		return True
	else:
		return False

def isdef(n):
	'''test whether n is deficient'''
	if nu(n)<2:
		return True
	else:
		return False
		
def isprimab(n):
	'''test whether n is primitive abundant'''
	if isper(n):
		return True
	elif isab(n):
		f = primes.propdiv(n)
		x = True
		for i in range(len(f)):
			if x:
				x = x and isdef(f[i])
			else:
				break
		return x 
	else:
		return False
	

def phi(n):
	'''The Euler phi function'''
	p = primes.pf(n)
	for i in range(len(p)):
		n=(n/p[i][0])*(p[i][0]-1)
	return n
	
def GCD(a,b):
	'''Euclidean Algorithm method of computing greatest common divisor'''
	while not b == 0:
		r = a%b
		a = b 
		b = r
	return a
		
def LCM(a,b):
	'''returns least common multiple'''
	return a*b/GCD(a,b)
	
def mu(n):
	'''mu inversion function'''
	p = primes.pf(n)
	i = 0
	t = 1
	while i < len(p):
		if p[i][1] == 1:
			t*=(-1)
			i+= 1
		else:
			t = 0 
			break
	return t 
	
def sumfactorbuilder(fn):
	''' returns a function that is the sum of the values\n
	of the original function of all the divisors of n'''
	def F(n):
		f = primes.factors(n)
		s = 0
		for i in range(len(f)):
			s += fn(f[i])
		return s 
	return F 
	
def muinversebuilder(fn):
	"""reverses sumfactorbuilder's operation."""
	def F(n):
		f = primes.factors(n)
		s = 0 
		for i in range(len(f)):
			s+= (mu(f[i])*fn(n/f[i]))
		return s 
	return F 
	
