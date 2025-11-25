import timeit
import random
from common import q
from ntt import mul_zq
from naive_ringmul import naive_mul_getcoeff
from falcon import SecretKey, PublicKey
from ntrugen import ntru_gen

def generate_random_poly(n):
    return [random.randint(0, q - 1) for _ in range(n)]

def benchmark_mul():
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

def benchmark_verify():
    ns = [64, 128, 256, 512, 1024]
    iterations = 100
    indices_counts = [1, 8]

    print("\nBenchmarking Verify vs Fast Verify (fverify)")
    print(f"{'n':<6} {'Indices':<8} {'Verify (ms)':<12} {'fVerify (ms)':<12} {'Speedup':<10}")
    print("-" * 55)

    for n in ns:
        # Setup keys and signature
        f, g, F, G = ntru_gen(n)
        sk = SecretKey(n, [f, g, F, G])
        pk = PublicKey(sk)
        message = b"benchmark"
        sig = sk.sign(message)
        
        # Benchmark standard verify
        t_verify = timeit.timeit(lambda: pk.verify(message, sig), number=iterations)
        avg_verify = (t_verify / iterations) * 1000

        # Prepare for fverify (excluded from benchmark)
        s0,s1,signature_bound,salt = pk.fverify_prepare(message, sig)
        
        for count in indices_counts:
            if count > n: continue
            
            # Select random indices
            indices = [random.randint(0, n - 1) for _ in range(count)]
            
            # Benchmark fverify
            t_fverify = timeit.timeit(lambda: pk.fverify(message, s0, s1, signature_bound, salt, indices), number=iterations)
            avg_fverify = (t_fverify / iterations) * 1000
            
            speedup = avg_verify / avg_fverify if avg_fverify > 0 else float('inf')
            
            print(f"{n:<6} {count:<8} {avg_verify:<12.4f} {avg_fverify:<12.4f} {speedup:<10.2f}")

if __name__ == "__main__":
    # benchmark_mul()
    benchmark_verify()
