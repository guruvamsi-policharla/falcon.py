import timeit
import random
from common import q
from ntt import mul_zq
from naive_ringmul import naive_mul_getcoeff

def generate_random_poly(n):
    return [random.randint(0, q - 1) for _ in range(n)]

def benchmark():
    # You can modify these values to test different parameters
    ns = [64, 128, 256, 512, 1024]
    iterations = 1000

    print(f"{'n':<10} {'NTT (ms)':<15} {'Naive GetCoeff (ms)':<20} {'Speedup (NTT/Naive)':<20}")
    print("-" * 65)

    for n in ns:
        f = generate_random_poly(n)
        g = generate_random_poly(n)
        
        # Benchmark NTT
        # ntt.mul_zq computes the full product (all n coefficients)
        t_ntt = timeit.timeit(lambda: mul_zq(f, g), number=iterations)
        avg_ntt = (t_ntt / iterations) * 1000 # in ms

        # Benchmark Naive GetCoeff
        # We only compute 1 coefficient
        idx = random.randint(0, n - 1)
        t_naive = timeit.timeit(lambda: naive_mul_getcoeff(f, g, idx), number=iterations)
        avg_naive = (t_naive / iterations) * 1000 # in ms

        speedup = avg_ntt / avg_naive if avg_naive > 0 else float('inf')

        print(f"{n:<10} {avg_ntt:<15.4f} {avg_naive:<20.4f} {speedup:<20.2f}")

if __name__ == "__main__":
    benchmark()
