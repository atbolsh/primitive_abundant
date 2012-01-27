#!/usr/bin/python

def lim(n):	
	'''This useful function appears often\n
	in sieves, and saves typing time'''
	return int(n**0.5)

def upperodd(n):
	'''As all but one primes are odd, it is useful to round\n
	to the nearest top odd and from there to count by 2'''
	if n%2 ==1:
		return n
	else:
		return n+1

def primes(n):
	'''An efficient mechanism for computing\n
	primes, based on Eratosthenes sieve'''
	base = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
	if n < 101:
		return [x for x in base if x < n+1]
	elif n < 10001:
		l = lim(n)
		p = primes(l)
		q = range(101, n+1, 2)
		for i in range(1,len(p)):
			q = [x for x in q if not x%p[i] == 0]
		return base + q
	else:
		l = lim(n)
		p = primes(l)
		q = range(upperodd(l), n+1, 2)
		for i in range(1,len(p)):
			q = [x for x in q if not x%p[i] == 0]
		return p + q

def eratosthenes( n ):
	'''A more efficient mechanism for computing primes'''
	#odd bug: eratosthenes(100000) waits for a long time after a prime in the 97000's before continuing.
	#for 1000000, after 978287
	lst = []
	l = lim(n) + 1
	i = 0
	while i < n/2 :
		lst += [True]
		i += 1
	primes = []
	i = 0
	#end of initialization
	while i < (n/2) - 1:
		j = i
		while j < (n/2) :
			if lst[ j ] :
				primes += [2*j + 3]
				break
			else:
				j += 1
		k = j
		if j < l:
			while k < (n/2):
				lst[ k ] = False
				k +=  (2*j + 3)
		i = j+1
	return [2] + primes

def exponent(prime,n):
	'''returns the exponent of a prime(preferably) or\n
	any number that exactly divides the second number'''
	if n == 0:
		return 'infinity'
	else:
		i = 0
		while n%prime == 0:
			i+= 1
			n /= prime
		return i

def divtest(primelist, n):
	'''tests divisibility by all elements of "primelist". If divisible\n
	by at least 1, returns False; otherwise, returns True'''
	x = True
	i = 0
	while i < len(primelist):
		if x :
			x = x and (not (n % primelist[i] == 0))
			i+=1
		else:
			break
	return x

def pf(n):
	'''A mechanism for computing the prime\n
	factorization of a number. Rather efficient'''
	p = 3
	plist = []
	pf = []
	e = exponent(2,n)
	if not e == 0:
		pf+=[(2,e)]
		n/=(2**e)
	while p < int(n**0.5)+1:
		if n == 1:
			break
		else:
			low = [x for x in plist if x < lim(p) +1]
			if divtest(low,p):
				plist += [p]
				e = exponent(p,n)
				if e == 0:
					p+=2
				else:
					pf+=[(p,e)]
					n/=(p**e)
					p+=2
			else:
				p+=2
	if n == 1:
		return pf
	else:
		return pf + [(n,1)]

def number(primefactorization):
	'''returns the number that a\n
	prime factorization corresponds to'''
	n = 1
	for i in range(len(primefactorization)):
		n *= (primefactorization[i][0]**primefactorization[i][1])
	return n 
	
def remtriv(primefactorization):
	'''removes trivial (0 exponent)\n
	entries in a prime factorization'''
	return [x for x in primefactorization if not x[1] == 0]
	
def mult(n, list):
	'''Multiplies every element of a list by n.'''
	return [x*n for x in list]
	
def permult(list1, list2):
	'''returns the list of all possible combinations of\n
	elements of list one and of list 2, multiplied'''
	res = []
	for i in range(len(list2)):
		res += mult(list2[i], list1)
	return res 
	
def factors(n):
	'''returns the list of factors of n'''
	f = [1]
	p = pf(n)
	for i in range(len(p)):
		q = [p[i][0]**x for x in range(p[i][1]+1)]
		f = permult(f, q)
	return sorted(f)
	
def propdiv(n):
	'''returns the list of proper divisors of n'''
	return factors(n)[:-1]
	

