def enc(x):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    xor = 177451812
    add = 8728348608
    s = [11, 10, 3, 8, 4, 6]
    x = (x ^ xor)+add
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x//58**i % 58]
    return ''.join(r)
