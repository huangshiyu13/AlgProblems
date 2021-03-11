#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: Shiyu Huang
@contact: huangsy1314@163.com
@file: question1.py
"""

def true_search(k):
    # 输入k字符串，比如k='165465',输出也为字符串
    # 这是一个正确的，但是暴力搜索的代码, 只用作测试
    if k == '0':
        print('you can\'t use zero value as input!')
    sum_original = sum([int(k0) for k0 in str(k)])
    int_k = int(k)
    while True:
        int_k+=1
        sum_k = sum([int(k0) for k0 in str(int_k)])
        if sum_k == sum_original:
            return str(int_k)

def good_search(k):
    # 输入k字符串，比如k='165465',输出也为字符串
    # 这是一个非常好的代码
    if k == '0':
        print('you can\'t use zero value as input!')
    k = [k0 for k0 in k]
    if len(k) == 1:
        k = ['0']+k
    sum = int(k[-1])
    findIndex = None
    for index in range(len(k)-2,-1,-1):
        sum+=int(k[index])
        if (not k[index] == '9') and sum > int(k[index]):
            findIndex = index
            break
    if findIndex is None:
        k=['0']+k
        index = 0
    else:
        index = findIndex
    k[index]=str(int(k[index])+1)
    for i in range(index+1, len(k)):
        k[i] = '0'
    res = sum-int(k[index])
    n = res//9
    rres = res%9
    for i in range(n):
        k[len(k)-i-1] = '9'
    k[len(k)-n-1] = str(rres)
    return ''.join(k)

def test_number():
    find_wrong = False
    for k in range(1,10000):
        k = str(k)
        s_k = good_search(k)
        t_k = true_search(k)

        # 把最好的代码的结果和暴力搜索的代码的结果进行比较
        if not s_k==t_k:
            #如果最好的代码出错了，就输出来，hhh
            print('Wrong!',k,s_k,t_k)
            find_wrong = True
    if not find_wrong:
        print('All answer is right!')

    # 大数测试 true_search不可用
    k = '1436846754587112315461319912545446245341545354654136546131374643131631794124794641999457000004564541546487445468000146499999999999999999000000'
    s_k = good_search(k)
    print(k,'->',s_k)

    # 大数测试 true_search不可用
    k = '4641343461436846613199125454462453415453546541365461313746431316317941247946417545871123154613199999457000004564541546487445468000146499999999999999999'
    s_k = good_search(k)
    print(k,'->', s_k)

if __name__ == '__main__':
    test_number()

