def perevod(a):
    n = a["num"]
    s1 = a["sis1"]
    s2 = a["sis2"]
    if s1 != 10:
        ch = 0
        for i in range(len(str(n))):
            ch += int(str(n)[i]) * (s1 ** (len(str(n)) - i - 1))
        n = ch
        s1 = 10
    ot = ""
    while n // s2 != 0:
        ot = str(n % s2) + ot
        n //= s2
    ot = str(n % s2) + ot
    return ot


def sequences(a):
    if a["f"] == "a":
        a1 = a["a1/b1"]
        d = a["d/q"]
        n = a["n"]
        s = (2 * a1 + (n - 1) * d) * n / 2
    else:
        b1 = a["a1/b1"]
        q = a["d/q"]
        n = a["n"]
        if n == 1:
            s = b1
        elif n == 0:
            s = 0
        else:
            s = b1 * ((q ** n) - 1) / (q - 1)
    return s