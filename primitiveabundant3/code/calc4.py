import number_theory2
import primes2

def probdiv(lst):
	l = number_theory2.LCM2(lst)
	count = 0
	i = 0
	while i<l:
		i += 1
		count += not primes2.divtest(lst, i)
	return float(count)/l


