#就是把m个球放到n个相同盒子里面的数目，每个盒子至少1个

dp_dict = {}
def solve(m,n):#解决把m个球放到n个相同盒子里面的数目，不要求每个盒子至少1个
    if m<0:
        return None,0
    if m == 0:
        return [[0 for _ in range(n)] ], 1
    if n==1:
        return [[m]],1
    if (m,n) in dp_dict:
        return dp_dict[(m,n)]

    re1,re_num1 = solve(m,n-1)
    re2,re_num2 = solve(m-n,n)
    re_num = re_num1+re_num2
   

    if re_num1==0:
        re =  [ [rrr+1 for rrr in rr] for rr in re2]
    elif re_num2==0:
        re = [[0]+rr for rr in re1]
    else:
        re = [[0]+rr for rr in re1]+ [ [rrr+1 for rrr in rr] for rr in re2]
    dp_dict[(m,n)] = (re,re_num)
    return re,re_num

if __name__ == '__main__':
    m = 100  # m个球
    n= 3 # n个相同盒子
    re,re_num = solve(m - n, n)
    if re_num>0:
        re = [[rrr+1 for rrr in rr] for rr in re]
    print(m ,n,re_num)