def reverse( x):
    s = cmp(x, 0)
    r = int(str(s*x)[::-1])
    return s*r * (r < 2**31)

print reverse(-123)