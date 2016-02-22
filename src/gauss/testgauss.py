#sc2-guess

#we are looking for probability that a random varibale
#X~ N(m,s) be greater than a given number a>m
#if F_{m,s} is the cumulative distribution funcion
#we are looking for 1-F(a)

import math.erf
def cumulativeDistribNormal(m,s,a):
	return 0.5*( 1+math.erf( (a-m)/(s*math.sqrt(2))) )

from scipy.stats import norm
##############
def main():
	print(norm.cdf(0.8))
	print(cumulativeDistribNormal(0,1,0.8))

if __name__ == '__main__':
	main()	

