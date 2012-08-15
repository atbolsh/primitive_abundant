'''A module with some of the most common
number-theoretic functions.'''


import primes2
#told you we would need this.

def tau(n, primelist = None, primefactorization = None):
	'''the number-theoretic method for computing the number of factors of n'''
	if primefactorization == None:		#initiate the prime factorization
		p = primes2.pf(n, primelist)
	else:
		p = primefactorization
	product = 1	#Good start for products
	for x in p:
		product*= (x[1]+1) #standard number-theoretic formula for this
	return product

def sigma(n, primelist = None, primefactorization = None):
	'''the number-theoretic method for computing the sum of the factors of n'''
	if n == 0:
		print 'infinity' #don't get too clever
	else:
		product = 1	#Good start for products
		if primefactorization == None:	#initiate prime factorization
			p = primes2.pf(n, primelist)
		else:
			p = primefactorization
		for x in p:
			product *= ((x[0]**(x[1]+1))-1)/(x[0]-1)	#standard number-theoretic method for the sigma function
		return product

def nu(n, primelist = None, primefactorization = None):
	'''sigma/n.'''
	return sigma(n, primelist, primefactorization)/float(n)

def isabundant(n, primelist = None, primefactorization = None, nuval = None):
	'''test whether or not a number is abundant'''
	if nuval == None:
		return nu(n, primelist, primefactorization)>2
	else:
		return nuval > 2
	
def isperfect(n, primelist = None, primefactorization = None, nuval = None):
	'''test whether n is perfect'''
	if nuval == None:
		return nu(n, primelist, primefactorization)==2
	else:
		return nuval == 2

def isdeficient(n, primelist = None, primefactorization = None, nuval = None):
	'''test whether n is deficient'''
	if nuval == None:
		return nu(n, primelist, primefactorization)<2
	else:
		return nuval < 2

def phi(n, primelist = None, primefactorization = None):
	'''The Euler phi function, or the quantity
of numbers <= n that are coprime to n.'''
	if primefactorization == None:	#initiate prime factorization
		p = primes2.pf(n, primelist)
	else:
		p = primefactorization
	for x in p:
		n=(n/x[0])*(x[0]-1)	#standard number-theoretic method for computing the Euler phi function
	return n
	
def GCD(a,b):
	'''Euclidean Algorithm method of computing greatest common divisor'''
	while not b == 0:
		a, b = b, a%b
	return a
	
def GCD2(lst):
	"""Finds the Greatest Common Divisor of a list"""
	d = 1
	for x in lst:
		d = GCD(d, x)
	return d
		
def LCM(a,b):
	'''returns least common multiple'''
	return a*b/GCD(a,b)

def LCM2(lst):
	"""Finds the least common multiple of a list"""
	l = 1
	for x in lst:
		l = LCM(l,x)
	return l 
		
def mu(n, primelist = None, primefactorization = None):
	'''mu inversion function'''
	if primefactorization == None:
		p = primes2.pf(n, primelist)
	else:
		p = primefactorization
	t = 1
	for x in p:
		if x[1] == 1:
			t*=(-1)
		else:
			t = 0 
			break
	return t 
	
def sumfactorbuilder(fn):
	''' returns a function that is the sum of the value
of the original function of all the divisors of n'''
	def F(n, primelist = None, primefactorization = None):
		f = primes2.factors(n, primelist, primefactorization)
		s = 0
		for x in f:
			s += fn(x, primelist)
		return s 
	return F 
	
def muinversebuilder(fn):
	"""reverses sumfactorbuilder's operation for
multiplicative functions."""
	def F(n, primelist = None, primefactorization = None):
		f = primes2.factors(n, primelist, primefactorization)
		s = 0 
		for x in f:
			s+= (mu(x)*fn((n/x), primelist))
		return s 
	return F 
	
