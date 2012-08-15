#!/usr/bin/python

'''This module is designed to provide prime sieves and
do basic operations necessary for other number theory
functions, such as generating prime factorizations and
lists of proper divisors. The backbone for the number
theory modules; imported by the other modules'''

def lim(n):	
	'''This useful function appears often
in sieves, and saves typing time'''
	return int(n**0.5)

def upperodd(n):
	'''As all but one primes are odd, it is useful to round
to the nearest top odd and from there to count by 2'''
	if n%2 ==1:
		return n
	else:
		return n+1

def low(lim, ordlist):
	"""For a list ordered in increasing order, this
wonderful function computes the list of elements
of ordlist less than lim, without using the time
necessary for list comprehension"""
	res = []
	z = len(ordlist)
	i = 0
	while i < z and ordlist[i]<lim:
		res.append(ordlist[i])
		i += 1
	return res

#def primes(n):
#	'''An efficient mechanism for computing
#primes, based on Eratosthenes sieve.
#A historic relic; the Eratosthenes
#function is much better.'''
#	base = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
#	if n < 101:
#		return [x for x in base if x < n+1]
#	elif n < 10001:
#		l = lim(n)
#		p = primes(l)
#		q = range(101, n+1, 2)
#		for i in range(1,len(p)):
#			q = [x for x in q if not x%p[i] == 0]
#		return base + q
#	else:
#		l = lim(n)
#		p = primes(l)
#		q = range(upperodd(l), n+1, 2)
#		for i in range(1,len(p)):
#			q = [x for x in q if not x%p[i] == 0]
#		return p + q 
#
		
def eratosthenes( n ):
	'''A more efficient mechanism for computing primes.
Universally referenced.'''
	#odd bug: eratosthenes(100000) waits for a long time after a prime in the 97000's before continuing.
	#for 1000000, after 978287
	lst = []		#the array of bools
	l = lim(n) + 1		#the upper bound
	i = 0			#the index
	while i < n/2 :		#the array of bools made into an array of bools. Note: only up to n/2, as only odds considered
		lst += [True]
		i += 1
	primes = []		#The eventual result
	i = 0			#reset index
	#end of initialization
	while i < (n/2) - 1:	#starting at 0, so adjustments must be made not to run out of the array
		j = i		#prime-seeking index
		while j < (n/2) :	#prime-seeking loop
			if lst[ j ] :	#if corresponding lst element is still True (has not been made False by being a multiple of previous primes) . . .
				primes += [2*j + 3]	#it is prime
				break			#stop here
			else:		#if not, has been made False; is some multiple; keep going
				j += 1
		k = j		#index for loop making all multiples of found prime False in the array
		if j < l:	#otherwise, no multiples left as True, no need to run extra loop
			while k < (n/2):
				lst[ k ] = False	#and thus ignored by prime-seeking loops
				k +=  (2*j + 3)	#Although we are looking at odd numbers, we still add the prime, not index; we basically add 2x the value.
		i = j+1		#Start next time after the last discovered prime
	return [2] + primes	#As 2 is the oddest prime, it must be given special consideration

def exponent(prime,n):
	'''Gives the exponent of a prime preferably or any number
that exactly divides the second number'''
	if n == 0:
		print 'infinity'
	else:
		i = 0
		while n%prime == 0:
			i+= 1
			n /= prime
		return i

def divtest(primelist, n):
	'''Tests divisibility by all elements of primelist. If divisible
by at least 1, returns False; otherwise, returns True'''
	x = True
	for p in primelist:
		if x :
			x = (n % p != 0)
		else:
			break
	return x

def pf(n, primelist = None):
	'''A mechanism for computing the prime
factorization of a number. Rather efficient.
The version without a primelist is faster for
a single number; the primelist version is
intended for work with ranges. The single
most important function for the number theory
modules.'''
	if primelist == None:		# . . . then we have to generate primes at the same time as we search for the prime factorization
		p = 3
		plist = [] 		#It is more efficient to generate primes only as needed for the function, if there is no given list of them.
		pf = [] 		#The empty "result" list
		e = exponent(2,n)	#As it is more efficient to only check odd numbers for primality, 2 must be a special case.
		l = lim(n)		#loop limit
		if not e == 0:
			pf+=[(2,e)]
			n/=(2**e)	#As these are divisors, it is better to continually make n smaller. Less primes to check that way.
			l = lim(n)	#The value of l must be changed
		while p < l+1:		#This is crucial: we only check up to the square root of the CURRENT (aka after all known primes taken out) n
			if n == 1:
				break	#We have completely factored n if n is 1.
			else:
				lowset = low(lim(p)+1, plist)	#We must test each potential prime; only makes sense to use eratosthenes.
				if divtest(lowset,p):		#aka if p is prime
					plist += [p]		#makes sense to test future potential primes for primality with this one
					e = exponent(p,n)	#how much of p goes into n?
					if e == 0:		#If p is not a factor of n . . .
						p+=2		#move on to the next potential prime
					else:
						pf+=[(p,e)]	#add it and its exponent to the prime factorization
						n/=(p**e)	#no need to test more primes than needed
						l = lim(n)	#lower the limit for p's
						p+=2		#move on to the next potential prime
				else:
					p+=2	#If p is not prime, move on to the next odd number.
		if n == 1:		#If n is completely factored . . .
			return pf	#Then we are done.
		else:
			return pf + [(n,1)]  #If not, then what remains is prime, is a factor, and has an exponent of 1 (or < l, and already in pf)
	else:				#By far the simpler case, as there is no need for a parallel prime sieve.
		l = lim(n)		#Why not optimize
		i = 0 			#Initiation of result
		pf = []			#Initiation of index
		p = 0 			#Necessary for first run of while loop
		z = len(primelist)	#We really shouldn't run out, but if we do, it helps to stop the loop
		while p < l + 1 and i < z:#No point in not using the upper bound that follows from eratosthenes's theorem; shouldn't run out of primes
			p = primelist[i]	#saves typing
			e = exponent(p,n)	#The rest of the loop is the same as before, minus the prime sieve, and works the same way.
			if e == 0:
				i += 1
			else:
				pf += [(p,e)]
				n /= (p**e)
				l = lim(n)
				i += 1
		if n == 1:		#Same story with returning results as in the other case
			return pf
		else:
			return pf + [(n,1)]

def number(primefactorization):
	'''returns the number that a
prime factorization corresponds to'''
	n = 1
	for x in primefactorization:
		n *= (x[0]**x[1])
	return n 

def cmp(x, y):
	if x[0]<y[0]:
		return -1
	elif x[0] == y[0]:
		return 0
	else:
		return 1
	
def remtriv(primefactorization):
	'''removes trivial (0 exponent)
entries in a prime factorization'''
	i = 0
	while i<len(primefactorization):
		if primefactorization[i][1] == 0:
			primefactorization.pop(i)
		else:
			i += 1
	primefactorization.sort(cmp)
	return primefactorization
	
def mult(n, lst):
	'''Multiplies every element of a list by n.'''
	return [x*n for x in lst]
	
def permult(list1, list2):
	'''returns the list of all possible combinations of
elements of list one and of list 2, multiplied'''
	res = []
	for x in list2:
		res += mult(x, list1)
	return res 
	
def factors(n, primelist = None, primefactorization = None):
	'''returns the list of factors of n'''
	f = [1]		#Universally a factor; good first start
	if primefactorization == None:	#initiate prime factorization
		p = pf(n, primelist)
	else:
		p = primefactorization
	for y in p:
		q = [y[0]**x for x in range(y[1]+1)]	#All the possible powers of y[0] that a factor of n may be divisible by
		f = permult(f, q)			#Multiplied by all the factors of n not divisible by y[0] (except for larger primes)
	return sorted(f)		#helps to have things in order
	
def propdiv(n, primelist = None, primefactorization = None):
	'''returns the list of proper divisors of n'''
	return factors(n, primelist, primefactorization)[:-1]	#Sometimes, we don't want n as one of the factors
	

