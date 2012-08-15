"""The module with functions specifically pertaining
to primitive abundant numbers"""

import number_theory2
import primes2

#This first group treats primitive abundant numbers as primitive abundant numbers.
#One is a helper function, one tests whether a given number is prim. ab., and the
#last provides a sieve for prim. ab. numbers below a threshold.

def impfact(n, primelist = None, primefactorization = None):
	"""returns all of the factors needed to test whether a
number is primitive abundant"""
	if primefactorization == None:
		primefactorization = primes2.pf(n, primelist)
	r = []
	for x in primefactorization:
		r.append(n/x[0])
	return r
	
def isprimab(n, primelist = None, primefactorization = None):
	'''test whether n is primitive abundant'''
	if n == 0:
		return False
	else:
		if primefactorization == None:		#initiate prime factorization
			p = primes2.pf(n, primelist)
		else:
			p = primefactorization
		m = number_theory2.nu(n, None, p)	#we need to see if n is at all a valid candidate
		if m == 2:
			return True			#all perfect numbers are primitive abundant
		elif m > 2:				#abundant case more complex
			f = impfact(n, None, p)		#find the necessary factors
			x = True			#initiate bool results
			for i in range(len(f)):		#check each factor
				if x:			#if the last factor was deficient . . .
					x = number_theory2.isdeficient(f[i], primelist)	#check if this one is
				else:			#if the last one already wasn't abundant . . .
					break		#no need to check further
			return x 			#return our bool result
		else:
			return False			#clearly, no deficient numbers are primitive abundant
			
def primab(n):
	''' a sieve for primitive abundant numbers
less than or equal to n'''
	plist = primes2.eratosthenes(int(n**0.5))	#the version of pf with a primelist is more efficient for work with ranges
	pab = []	#initiate result
	lst = []	#initiate array
	i = 0		#initiat index
	while i < n+1:	#fill the array with bools
		lst += [True]
		i += 1	
	i = 1		#reset index to 1, so as not to test 0
	#end of initialization
	while i < n + 1:
		if lst[i]:	#if it is not a multiple of the previously discovered primitive abundant numbers . . .
			m = number_theory2.nu(i, plist)	#check if it is abundant or perfect.
			if m >=2:			#if it is, ...
				pab += [i]		#then it is primitive abundant.
				k = i			#cancel out all multiples of i; this initiates the index, ...
				while k < n +1:		#and this actually makes the array values "false"
					lst[k] = False
					k += i
			else:
				lst[i] = False
		i +=1
	return pab
	
#This next set of functions looks at primitive abundant numbers in terms of
#their prime factorizations. As in the paper, the focus is on testing
#their prime factorization for the potential to generate primitive abundant,
#as well as on generating those prim. ab. numbers by the process of progressive
#minimization.

def hasabs(primelist, n = 1, primefactorization = None):
	"""As promised in the paper, here is a function to test whether or not
a set of primes is the (non-distinct) prime factorization for
any abundant or perfect numbers. The n here is the same as
in the paper; a number, none of whose factors are in primelist,
and with whose sigma it is needed to test the primitive abundance
of the set of primes."""
	numerator = reduce(lambda x, y: x*y,primelist,number_theory2.sigma(n, None, primefactorization))
	denominator = reduce(lambda x, y: x*y,[x -1 for x in primelist], n)
	q, r = numerator/denominator, numerator%denominator
	return test(q, r)
	
def hasprimab(primelist):
	"""Tests whether or not a prime list is capable of
forming primitive abundant numbers"""
	p = primelist[-1]
	M = maxdef(primelist[:-1])
	if M == None:
		return False
	num, den = M[-2]*p, M[-1]*(p-1)
	return test(num/den, num%den)
	
def test(q, r, end = False):
	"""oft utilized test in functions. Convenient,
because this quotient-remainder test is
more accurate than the floating point,
which suffers from odd digits at the
end due to memory, which are otherwise
insignificant except for the fact that
\'==\' and other such tests require
exact values."""
	if end == False:
		return (q == 2 and r!= 0) or q>2
	else:
		return q>=2

def onemin(p, otherprimes, n = 1, primefact = None, num = None, den = None):
	"""Finds the minimum exponent with which a prime and the
rest of the primelist with infinite exponent is
abundant. The extra variables \'n\' and
\'primefact\' allow one to include a number
along with the prime and the prime list;
the other extra arguments are designed to
override the internal structure of this
function, thus allowing more efficient
calls in other functions, such as
progmin."""
	if num == None or den == None:	#if the programmer wants the computer to find out, or has omitted one variable
		num = reduce(lambda x, y: x*y, otherprimes, number_theory2.sigma(n, None, primefact))#see paper to see why
		den = reduce(lambda x, y: x*y, [x-1 for x in otherprimes], n)#see paper to see why
	q, r = (num*p)/(den*(p-1)), (num*p)%(den*(p-1))#The quotioent and the remainder are assigned
	if test(q, r, otherprimes == []): #if this has the potential of being abundant at all
		e = -1			#initiate exponent one below first necessary value
		q, r = 1, 0		#Give bogus initial values for quotient and remainder that will not pass "test"
		while not test(q, r, otherprimes == []):	#While we have not yet found the right exponent. . .
			e += 1					#Incrememnt the exponent by one from what it used to be
			x, y = number_theory2.sigma(1, None, [(p, e)]), p**e #These values are what are multiplied to num, den
			a, b = num*x, den*y 	#We must take above values into account in num and den now
			q, r = a/b, a%b 		#Reassign quotient and remainder correctly
		return [y, (p, e)]			#If we are done, this p**e (or y) has passed. We return it and prime fact.
	elif q == 2:		#if this is a perfect number in the infinite case (have yet to find one) . . .
		return ["infinity", (p, "infinity")]	#Our process will never end, but the infinite exponent checks out
	else:				#An exceptional case; no abundance whatsoever on the horizon
		print "error: always deficient"			#No reason to return anything; this is a bogus argument

def progmin(ordprimes, showfact = False):
	"""Progresive minimization, as in paper, starting with the first
prime of the list, returning a prim. ab. number.
Note: ORDER MATTERS. showfact, if True, will
show the prime factorization of the number
along with the number itself, the two in
a tuple."""
	c = ordprimes[:]			#This way, we will not modify "ordprimes" if we need it later
	z = len(c)					#It is easier here to use list.pop(0), rather than "for x in list"; thus, the index
	primefact = []				#Initiate one of the results
	n = 1						#initiate other of the results
	num = reduce(lambda x, y: x*y, ordprimes, 1)				#Initiate num with default value
	den = reduce(lambda x, y: x*y, [x-1 for x in ordprimes], 1)	#Initiate den with default value
	for i in range(z):			#The loop; we want to do what follows to all elements of c
		p = c.pop(0)			#Take out next prime; shorten remaining list to exclude said prime
		num /= p 				#No reason to include p in num anymore, as it is now an external prime
		den /= (p-1)			#Same as above
		r = onemin(p, c, n, primefact, num, den)			#Find the exponent of the prime
		primefact.append(r[1])	#This is one of the factors of n that we have found	
		n *= r[0]				#Ditto
		num *= number_theory2.sigma(r[0], None, [r[1]])		#Faster to build up num than recalculate sigma(n)
		den *= r[0]			#Seeing as we are building up, why not build den as well
	if showfact:		#If user wants the prime factorization, . . .
		return (n, primes2.remtriv(primefact))	#We return number AND prime factorization
	else:				#If not, . . .
		return n		#We assume they don't, and only return the number.

def permutations(lst):
	"""Returns all permutations in the order of lst.
A generator. NOTE: because of the necessity
of this generator, many of the functions
below take time proportional to the factorial
of the quantity of primes in the primelist;
thus, these functions should not be used with
long prime lists."""
	if lst == []:
		yield lst
	else:
		p = []
		for x in lst:
			c = lst[:]
			c.remove(x)
			last = permutations(c)
			for y in last:
				yield [x] + y

def allprogmin(primelist, showfact = False, showord = False):
	"""Returns all primitive abundant numbers that
may be obtained from primelist by progressive
minimization. If you can find a set of primes
which generates any prime other than the ones
obtained by this function, that is a notable
result for primitive abundant numbers.
showfact will show the primefactorizations
along with the numbers; showord will show
the order of minimization that generated
each primitive abundant number."""
	result = []					#Initiate the results
	p = permutations(primelist) #All possible orders
	if showord:					#If user wants the order of minimization. . .
		if showfact:				#And the prime factorization
			for x in p:					#Then, for every permutation,
				r = progmin(x, showfact)		#Finds its corresponding prim. ab.,	
				result.append((x, r[0], r[1]))	#and append it to result. (with the order, and the tuple expanded)	
		else:						#...but not prime factorization,
			for x in p:					#Then, for every permutation,
				r = progmin(x, showfact)	#Find its corresponding prim. ab.
				result.append((x, r))		#and still append it to result (with the order)
	else:						#If they just want all the numbers
		for x in p:					#Then skip straight to permutations,
			r = progmin(x, showfact)	#Find the corresponding prim. ab.,
			if r not in result:			#And if you have not yet seen it,
				result.append(r)			#Do append it to result. (without the order that generated it).
	return result				#We do want the result, right?
	
#This next batch of functions focuses on maximal deficient numbers, and maximal deficiency

def test2(q, r, hasinf = False):
	"""This other quotient-remainder test tests for deficiency."""
	if hasinf:
		return (q <= 1) or (q == 2 and r == 0)	#If the infinite case is to be allowed, q == 2 and r == 0 is allowed
	else:
		return q == 1 #If finite, must be strictly deficient
		
def numdeninf(primelist, n = 1, primefactorization = None):
	"""Returns the num, den, and hasinf for primelist, n, and
primefactorization. More convenient than retyping each time."""
	if n == "infinity":		#Not unlikely.
		hasinf = True		#Clearly
		nunum, nuden = 1, 1	#We need to start at the multiplicative identity and move on from there
		for x in primefactorization:
			if x[1] == "infinity":		#Not unlikely . . .
				nunum *= p 		#We use the limit behavior of the nu function (see paper)
				nuden *= (p-1)
			else:
				nunum *= number_theory2.sigma(1, None, [x])	#Otherwise, just treat this as a normal prime factorization
				nuden *= (x[0]**x[1])
	else:
		hasinf = False		#Clearly
		nunum, nuden = number_theory2.sigma(n), n	#No need to care about the limit scenario. 
	num = reduce(lambda x, y: x*y, [x+1 for x in primelist], nunum)		#Here, we are dealing with deficiency. For more detail, see paper
	den = reduce(lambda x, y: x*y, primelist, nuden)
	return [num, den, hasinf]	#What we are after
	
def hasdef(primelist, n = 1, primefactorization = None):
	"""tests whether or not the primelist can make
any deficient numbers at all"""
	ndh = numdeninf(primelist, n, primefactorization)
	return test2(ndh[0]/ndh[1], ndh[0]%ndh[1], ndh[2])
	
def onemax(p, primelist, n = 1, primefactorization = None, num = None, den = None, hasinf = None):
	"""Finding the maximum exponent of that still generates
a deficient number (with n and with primelist)"""
	if num == None or den == None or hasinf == None:		#Works just like onemin, but with the extra detail of the infinite scenario.
		ndh = numdeninf(primelist, n = 1, primefactorization = None)
	else:
		ndh = [num, den, hasinf]
	a, b = ndh[0]*(p+1), ndh[1]*p
	q, r = a/b, a%b
	if test2(q, r, ndh[2]):
		a, b = ndh[0]*p, ndh[1]*(p-1)
		q, r = a/b, a%b
		if test2(q, r, True):			#The infinite case: we wish to avoid infinite loops
			return ["infinity", (p, "infinity")]
		else:
			e = 0 
			q, r = 1, 0
			while test2(q, r, ndh[2]):
				e += 1
				x, y = number_theory2.sigma(1, None, [(p, e)]), p**e 
				a, b = ndh[0]*x, ndh[1]*y 
				q, r = a/b, a%b 
			return [y/p, (p, e-1)]
	else:
		return None
		
def progmax(ordprimes, showfact = False, shownumden = False):
	"""This function will find the deficient number
(possibly infinite) that comes about from
progressively maximizing the exponents of
ordprimes in the order given. It will
also return the nu value of the number
generated. On our way to finding the
maximum deficient number of a set of primes."""
	c = ordprimes[:]			#This way, we will not modify "ordprimes" if we need it later
	hasinf = False				#We assume no infinite exponents until we find them
	z = len(c)					#It is easier here to use list.pop(0), rather than "for x in list"; thus, the index
	primefact = []				#Initiate one of the results
	n = 1						#initiate other of the results
	num = reduce(lambda x, y: x*y, [x+1 for x in ordprimes], 1)	#Initiate num with default value
	den = reduce(lambda x, y: x*y, ordprimes, 1)				#Initiate den with default value
	for i in range(z):			#The loop; we want to do what follows to all elements of c
		p = c.pop(0)			#Take out next prime; shorten remaining list to exclude said prime
		num /= (p+1) 			#No reason to include p+1 in num anymore, as it is now an external prime
		den /= p				#Same as above
		r = onemax(p, c, n, primefact, num, den, hasinf)			#Find the exponent of the prime
		if r == None:			#If this was not deficient, ever . . .
			return None
		primefact.append(r[1])	#This is one of the factors of n that we have found	
		if r[0] == "infinity":	#Now, if we have found an infinite exponent, we need to be tricky
			hasinf = True		#First, we now know we are dealing with infinity
			n = "infinity"		#Likewise
			num *= p			#Look at the section on nu in paper
			den *= (p-1)		#Likewise
		else:				#Otherwise,
			if not hasinf:		#Unless we are already dealing with infinity,
				n *= r[0]		#We need to change the value of n
			num *= number_theory2.sigma(r[0], None, [r[1]])		#Faster to build up num than recalculate sigma(n)
			den *= r[0]			#Seeing as we are building up, why not build den as well
	result = (n, float(num)/den)
	if showfact:
		result += (primefact,)
	if shownumden:
		result += (num, den)
	return result
		
def maxdef(primes):
	"""The entire point of this group of functions:
finding the maximum deficiency of a list
of primes, assuming progressive maximization
will always succeed."""
	M = (1, 1, [])		#Give generic, bogus value that will always be exceeded for the maximum
	for x in permutations(primes):	#Test each permutation of primes
		d = progmax(x, True, True)	#Get the deficient number corresponding to each, showing all
		if d == None:
			return None
		if d[1] > M[1]:				#If less deficient than current value . . .
			M = d					#Maximum reset to it
	return M			#Return computed maximum, with num and den
	
#The following set of sections contains miscellaneous (and interesting) functions.

def firstnotdiv(n, primelist = None):
	"""Finds the set of primes not divisible by the
first n primes, with the least quantity of primes,
that is the distinct prime factorization of at least
one primitive abundant number"""
	if primelist == None:			#... then we have to include a parallel prime sieve, like with primes2.pf
		p = 3				#The first odd prime
		plist = [2]			#The only even prime
		if n == 0:			#If they want 6 as the result . . .
			res = [2]		#Then we have to include two in the result. We wouldn't otherwise.
			num = 2			#Why not give the numerator, denomerator, quotient and remainder straight away?
			den = 1
			q = 2
			r = 0
		else:				#Otherwise, . . .
			res = []		#We start with an empty result list.
			num = 1			#We give 1's as the num and den, as we will be using *= extensively.
			den = 1	
			q = 1			#We give bogus quotient and result, that will not pass the test the first time
			r = 0
		while len(plist)<n:		#Build up the first n primes, before we worry about the numerator and denominator.
			low = primes2.low(primes2.lim(p)+1, plist)	#Standard parallel prime sieve.
			if primes2.divtest(low, p):
				plist.append(p)
				p += 2
			else:
				p += 2
		while not test(q,r):		#While we have not found enough primes . . . (stops at the first sufficient prime)
			low = primes2.low(primes2.lim(p)+1, plist)		#Standard parallel prime sieve
			if primes2.divtest(low, p):
				plist.append(p)
				res.append(p)		#if it is prime, add it to the list
				num *= p		#Change the numerator
				den *= (p - 1)		#Change the denominator
				q, r = num/den, num%den	#Change quotient and remainder. For justification, see earlier functions.
				p += 2
			else:
				p += 2
		return res			#We do want a result, right?
	else:
		c = primelist[n:]		#Cut the first n off
		i = 0				#Initiate; index at 0, num and den at 1 (to be multiplied), q and r non-passing bogus, empty result
		num = 1
		den = 1
		q = 1
		r = 0
		res = []			#End initiation
		while not test(q,r):		#As long as we do not have enough primes, . . .
			res.append(c[i])	#We need at least one more.
			num *= c[i]		#Check if it was enough; multiply to num and den, and reset q and r.
			den *= (c[i] - 1)
			q, r = num/den, num%den
			i += 1			#Index must increase
		return res			#We are done.
			
def firstsquarefree(n, primelist = None):
	"""Returns the first squarefree prim. ab.
num. not divisible by the first n primes."""
	if primelist == None:			#...then another parallel prime sieve
		p = 3				#See firstnotdiv for details on the prime sieve initiation
		plist = [2]
		if n == 0:			#We save time by only checking odds for primality; 2 must be a special case.
			res = [(2, 1)]		#Just give the true values for initiation here.
			num = 3
			den = 2
			q = 1
		else:				#Initiate empty result, multiplicative identity for num and den, and bogus, not-passing q
			res = []
			num = 1
			den = 1
			q = 1
		while len(plist)<n:		#Standard prime sieve. Build up the list of primes to the necessary length.
			low = primes2.low(primes2.lim(p)+1, plist)
			if primes2.divtest(low, p):
				plist.append(p)
				p += 2
			else:
				p += 2
		while q<2:			#Will stop just after we pass the test, for the first time
			low = primes2.low(primes2.lim(p)+1, plist)	#Standard parallel prime sieve
			if primes2.divtest(low, p):
				plist.append(p)
				res.append((p, 1))			#In this case, we are returning prime factorization, not just a prime list
				num *= (p+1)				#Exponent, of one, not infinity, here; must be remembered
				den *= p
				q = num/den				#Reset the quotioned
				p += 2
			else:
				p += 2
		return (den, res) 		#As the denominator is the product of the primes, it is also the sought-after number. res is its pf.
	else:
		c = primelist[n:]
		i = 0
		num = 1
		den = 1
		q = 1
		res = []
		while q<2:
			res.append((c[i], 1))
			num *= (c[i] + 1)
			den *= c[i]
			q = num/den
			i += 1
		return (den, res)
		
def lastprime(factors, primelist = None):
	"""Finds the last prime such that the list
of primes in factors and that prime
are the distinct prime factorization
of at least one primitive abundant
number"""
	if primelist == None:		# . . . then yet another parallel prime sieve.
		M = maxdef(factors)	#We need the maximum deficiency of the set of numbers
		if M == None:		#If there is no maximum deficiency to speak of . . .
			return None	#There is no last prime
		if M[1] == 2:		#If this was one of those infinite perfect numbers (only known: 2**inifinity), we don't want an infinite loop
			return "all primes valid"	# . . . as there is no last prime
		num = M[-2]		#Otherwise, we read off num and den from the maximum deficiency
		den = M[-1]
		cand = []		#This is the list of all the primes that satisfy the conditions, except the last element
		plist = [2]		#We must include the oddest prime, as all we will check is odd numbers.
		p = 1			#Because it is 2 less than three, and here, on a whim, I decided to increment at the beginning of the loop.
		q, r = 3, 0		#Bogus passing values.
		while test(q,r):	# . . . while we are still dealing with satisfactory primes.
			p += 2		#Increment our prime
			l = int(p**0.5)	#Standard parallel prime sieve.
			low = primes2.low(primes2.lim(p)+1, plist)
			if primes2.divtest(low, p):		#If p is prime
				plist.append(p)			#We add it to the list of primes.
				if p not in factors:		#We don't want repetitions
					cand.append(p)		#Add it to the list of candidates, . . .
					a, b = num*p, den*(p-1)
					q, r = a/b, a%b 	#And recaluculate q and r
		if len(cand) <= 1:	#If the first new prime failed . . .
			return None	#Then there is no last passing prime
		else:
			return cand[-2]		#Otherwise, we return the last prime that did not fail.
	else:
		M = maxdef(factors)	#Same as above, but without the parallel prime sieve.
		if M == None:
			return None
		if M[1] == 2:
			return "all primes valid"
		num = M[-2]
		den = M[-1]
		m = max(factors)
		c = [x for x in primelist if x > m]
		i = -1 
		q, r = 3, 0 
		while test(q, r):	
			i += 1
			p = c[i]
			a = num*p 
			b = den*(p-1)
			q, r = a/b, a%b
		if i == 0:
			return None
		else:
			return c[i-1]
		
		
