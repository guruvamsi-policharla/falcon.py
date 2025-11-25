"""
Naive implementation of ring element multiplication
"""
from common import q

def naive_mul(f, g):
    """
    Compute the product of two polynomials f and g in Z_q[x] / (x^n + 1).
    
    Args:
        f: a list of coefficients
        g: a list of coefficients
        
    Returns:
        The product f * g mod (x^n + 1)
    """
    n = len(f)
    assert len(g) == n
    h = [0] * n

    for i in range(n):
        for j in range(n):
            k = i + j
            val = (f[i] * g[j]) % q
            if k < n:
                h[k] = (h[k] + val) % q
            else:
                h[k - n] = (h[k - n] - val) % q
    return h

def naive_mul_getcoeff(f, g, i):
    """
    Compute the i-th coefficient of the product of two polynomials f and g in Z_q[x] / (x^n + 1).
    
    Args:
        f: a list of coefficients
        g: a list of coefficients
        i: the index of the coefficient to compute
        
    Returns:
        The i-th coefficient of the product f * g mod (x^n + 1)
    """
    n = len(f)
    assert len(g) == n
    hi = 0
    v = 0

    for u in range(n):    
        if u <= i:
            v = i - u
            val = (f[u] * g[v]) % q
            hi = (hi + val) % q
        else:
            v = i + n - u
            val = (f[u] * g[v]) % q
            hi = (hi - val) % q
    return hi
