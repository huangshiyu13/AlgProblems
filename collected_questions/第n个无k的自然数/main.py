
import sys
import copy

# calculate the number with 0 as the first letter
def cal_An(letter_num):
	A = [0]
	n = 1
	while len(A)<letter_num:
		A.append(A[-1]+9**n)
		n+=1
	return A

def good(res,k):
	while res>0:
		# print(res,k)
		if res%10 == k:
			return False
		res=int(res/10)
	return True

# violent solution
def solution1(k,n):
	if k == 0:
		res = 1
	else:
		res = 0
	num = 1
	while num<n:
		res+=1
		if good(res,k):
			num+=1
	return res

# get the solution
def solution2(k,n,letter_num=20):
	a = list(range(10))
	a.pop(k)
	
	current_num = 9**letter_num
	res = 0

	for i in range(letter_num):
		current_num /= 9
		
		# print(current_num)
		for num in a:
			if current_num<n:
				n-=current_num
			else:
				res = res*10+num
				break
	return res

# get the solution with first letter is 0
def solution3(n,A,letter_num):
	res = 1
	for i in range(letter_num):
		current_num = A.pop()
		# print(current_num)
		if current_num<n:
			n-=current_num
			res = solution2(0,n,letter_num-i)
			break
	return res

def test():
	letter_num = 20
	A_origin = cal_An(letter_num)
	for k in range(10):
		# test 1e6-1
		n = 1e6-1
		res1 = solution1(k,n)
		if k == 0:
			A = copy.copy(A_origin)
			res2 = solution3(n,A,letter_num)
		else:
			res2 = solution2(k,n)
		if res1!=res2:
			print(k,n,res1,res2)
			return()


		for n in  range(1,1000):
			res1 = solution1(k,n)
			if k == 0:
				A = copy.copy(A_origin)
				res2 = solution3(n,A,letter_num)
			else:
				res2 = solution2(k,n)
			if res1!=res2:
				print(k,n,res1,res2)
				return()


if __name__ == "__main__":
	test()