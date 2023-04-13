import os
import math


def main():
    while True:
        while not (p := input("Enter P (P >= 0): ")).isnumeric():
            print(f'Invalid input: "{p}" is not a positive integer, try again')
        p = int(p)

        while not (n := input("Enter N (N >= 0): ")).isnumeric():
            print(f'Invalid input: "{n}" is not a positive integer, try again')
        n = int(n)

        if n / p <= math.sqrt(n):
            print(
                "Invalid input: ratio of N to P (~%.2f) must be greater than sqrt(N) (~%.2f)"
                % (n / p, math.sqrt(n))
            )
            continue

        break

    dirpath = os.getcwd()
    os.system(f"mpiexec -n {p} python3 {dirpath}/parallel-sieve.py {n}")


if __name__ == "__main__":
    main()
