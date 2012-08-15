import number_theory2

"""This module was expressly created to calculate the natural density
of abundant numbers"""

#def LCMs0(lst):
#		"""Returns a list of all the LCMs of subsets of lst;
#		LCMs of subsets with even and odd quantities of elements
#		in separate lists"""
#		if lst == []:
#			return [[1],[]]
#		else:
#			last = LCMs0(lst[:-1])
#			even = [number_theory.LCM(lst[-1], x) for x in last[1]]
#			odd =  [number_theory.LCM(lst[-1], x) for x in last[0]]
#			last[0] += even
#			last[1] += odd
#			return last

def LCMs(lst, lim = None):
	"""Returns a list of all the LCMs of subsets of lst;
	LCMs of subsets with even and odd cardinalites
	appear in different lists. If lim is given, only 
	returns values less than lim"""
	if lim == None:	#the purest and generally used case; I have no idea of the error margin after adding a limit to the LCMs.
		if lst == []:		#the base case for recursion
			return [[1],[]]	#only subset is here the null set, which has an even (0) number of elements, whose LCM is by default 1.
		else:
			last = LCMs(lst[:-1])	#all the LCMs but the last element
			z = len(last[0])	#when we add LCMs to last[1] (odd-elemented LCMs), we do not want to include newly generated LCMs.
			last[0] += [number_theory2.LCM(lst[-1], x) for x in last[1]] #add all the LCMs of an odd # of elements and x to even-elemented LCMs
			for i in range(z):	#for i in even-elemented LCMs, before last modification,
				last[1].append(number_theory2.LCM(lst[-1], last[0][i]))#add the LCM of last[0][i] and the last element of lst.
			return last		#return modified (and now misnamed) last, or the list of two lists of LCMs
	else:		#Same as before, except . . .
		if lst == []:
			return [[1],[]]
		else:
			last = LCMs(lst[:-1])
			z = len(last[0])
			for x in last[1]:
				l = number_theory2.LCM(x, lst[-1])
				if l<lim:	#we ignore LCMs greater than a margin.
					last[0].append(l)
			for i in range(z):
				l = number_theory2.LCM(last[0][i], lst[-1])
				if l<lim:	#This saves much space, as each iteration throws out LCMs, which would have proliferated into more LCMs.
					last[1].append(l)
			return last
	
def cmp(x,y):
	"""We will need to sort backwards in probdiv to minimize error"""
	if x > y:
		return -1
	elif x == y:
		return 0 
	else:
		return 1

#def probdiv(lst, lim = None):
#		"""The probability that a randomly selected natural number
#		is divisible by at least one of the elements of lst. If
#		lim is given, value approximate, as all LCMs above lim
#		are ignored."""
#		l = LCMs(lst, lim)
#		l[0].pop(0)
#		l[0].sort(cmp)
#		l[1].sort(cmp)
##		pos = sum([1.0/x for x in l[1]])-- old method
##		neg = sum([1.0/x for x in l[0]])-- old method
#		pos = 0 
#		neg = 0 
#		while not l[1] == []:
#			pos += 1.0/l[1].pop(0)
#		while not l[0] == []:
#			neg += 1.0/l[0].pop(0)
#		return pos - neg
#
#The above version takes too long; bottom version circa 8 times faster
		
def probdiv(lst, lim = None):
		"""The probability that a randomly selected natural number
		is divisible by at least one of the elements of lst. If
		lim is given, value approximate, as all LCMs above lim
		are ignored."""
		#The reason that this function works is not at all clear. In fact, it takes several pages of mathematics to prove that it does.
		#Thus, commentary on this function is provided separately, in calc_commentary.pdf
		l = LCMs(lst, lim)
		l[0].pop(0)
		l[0].sort(cmp)
		l[1].sort(cmp)
#		pos = sum([1.0/x for x in l[1]]) -- old
#		neg = sum([1.0/x for x in l[0]]) -- old
		pos = 0 
		neg = 0 
		for x in l[1]:
			pos += 1.0/x
		for x in l[0]:
			neg += 1.0/x
		return pos - neg		

