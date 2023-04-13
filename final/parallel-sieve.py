import math
import numpy as np
from mpi4py import MPI
from argparse import ArgumentParser

# Эта программа находит все простые числа на интервале 1..N,
# используя для этого P параллельных процессов.
#
# Для запуска этой программы требуется вызвать команду:
#
#       mpiexec -n P python3 parallel-sieve.py N
#
# где   N - граница интервала рассматриваемых чисел,
#       P - требуемое число процессов.
#
# При этом между этими величинами должно выполняться следующее соотношение:
#
#       (N / P) > sqrt(N)
#

# Получаем границы интервала рассматриваемых чисел n,
# количество процессов size и номер процесса rank

parser = ArgumentParser()
parser.add_argument("n")
args = parser.parse_args()

n = int(args.n)

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

# Вычисляем границы и размеры интервалов, рассматриваемых в каждом процессе
# (игнорируя числа 0 и 1 как заведомо не являющиеся простыми)

first = math.floor(rank * (n - 2) / size) + 2
last = math.floor((rank + 1) * (n - 2) / size) + 1
length = last - first + 1


# Инициализируем маску простоты arr
# (элемент arr[i] отражает простоту числа first + i)
arr = np.full(length, True)

# Инициализируем первое простое число k = 2
k = 2

while k * k < n:
    # Получаем индекс первого числа, кратного k, на рассматриваемом интервале
    idx = 0 if first % k == 0 else k - first % k

    # Помечаем все числа на рассматриваемом интервале, кратные k,
    # как не-простые (шаг решета Эратосфена)
    for i in range(idx, length, k):
        arr[i] = False

    # В первом процессе:
    if rank == 0:
        # - отмечаем k как простое
        arr[idx] = True

        # - находим следующее простое число
        k += 1
        while not arr[k - first]:
            k += 1

    # Передаем найденное простое число всем процессам
    k = comm.bcast(k, root=0)

# Преобразуем маску простоты arr в массив простых чисел l_primes
l_primes = [first + i for i in range(length) if arr[i]]

# Агрегируем простые числа со всех процессов в массив g_primes
g_primes = comm.reduce(l_primes, MPI.SUM, root=0)

# Выводим результат
if rank == 0:
    print(g_primes)
