"""A less acurate but not memory-intensive at all
collection of functions for computing the natural
density of abundant numbers"""

import number_theory

def pairedLCMs(lst):
	if len(lst) == 1:
		yield (1, lst[0])
	else:
		for x in pairedLCMs(lst[:-1]):
			yield x
			yield (number_theory.LCM(x[1], lst[-1]), number_theory.LCM(x[0], lst[-1]))

def ind(n):
	a = n/1000000
	if a>999:
		return 999
	else:
		return a

def probdiv(lst):
	posl = []
	negl = []
	for i in range(1000):
		posl.append(0)
		negl.append(0)
	for x in pairedLCMs(lst):
		posl[ind(x[1])] += 1.0/x[1]
		negl[ind(x[0])] += 1.0/x[0]
	pos = 0
	neg = 0
	for i in range(1000):
		pos += posl[999-i]
		neg += negl[999-i]
	return 1+pos - neg
