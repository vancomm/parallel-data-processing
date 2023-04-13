#include <math.h>
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

long get_elem_at_index(long index, int rank, int p, long n) {
    long first_elem = floor(rank * (n - 2) / p) + 2;
    return first_elem + index;
}

int main(int argc, char* argv[]) {
    int p;     // number of processes
    int rank;  // rank of the current process
    int DEBUG = 0;
    unsigned long n;
    unsigned long first_elem;
    unsigned long last_elem;
    unsigned long size;
    unsigned long i;
    unsigned long k;
    unsigned long index_first_multiple;
    unsigned long next_k;
    unsigned int local_sum;
    unsigned int global_sum;

    MPI_Init(&argc, &argv);                // Initialize the MPI environment
    MPI_Comm_size(MPI_COMM_WORLD, &p);     // Get the number of processes
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // Get the rank of the process
    double time = MPI_Wtime();

    if (argc == 3)
        DEBUG = atoi(argv[2]);
    else if (!(argc == 2)) {
        if (rank == 1) printf("Error: expected 1 or 2 arguments but got %d \n", argc - 1);
        exit(1);
    }
    n = atol(argv[1]);

    // we must have that n/p > sqrt(n) to ensure that the next value of k is always in proc 0
    if (!(n / p > sqrt(n))) {
        if (rank == 1) printf("Error: there are too many processes! \n");
        MPI_Finalize();
        exit(1);
    }

    // We split the array into p contiguous blocks of equal size
    // for each process, get the values of the first and last elems and the number of elems
    first_elem = floor(rank * (n - 2) / p) + 2;
    last_elem = floor((rank + 1) * (n - 2) / p) - 1 + 2;
    size = last_elem - first_elem + 1;

    // initialize the array for this thread
    // note that in proc0 the elem at index 0 is 2 (we ignore 0 and 1)
    // bool array[size];
    bool* array = new bool[size];
    for (i = 0; i < size; i++) {
        array[i] = true;  // first every element is marked as prime
    }

    if (DEBUG) printf("Thread %d : %lu to %lu \n", rank, first_elem, last_elem);

    // first, set k to 2 for each task
    k = 2;

    while (k * k <= n) {
        // determine the index of the first multiple of k in the current thread
        index_first_multiple;
        if (first_elem % k == 0)
            index_first_multiple = 0;
        else
            index_first_multiple = k - first_elem % k;

        if (DEBUG) {
            printf("first multiple of k=%lu in thread %d: %lu \n", k, rank, get_elem_at_index(index_first_multiple, rank, p, n));
            sleep(1);
        }

        // from this first multiple, mark as non-prime every kth element
        for (i = index_first_multiple; i < size; i += k) {
            array[i] = false;
        }
        if (rank == 0) array[k - 2] = true;  // k is a prime number that belongs in thread0's array

        // set the next value of k to the smallest "true" number > current k
        // thread0 is in charge to find this value and broadcast it
        // note that this value is in thread 0 because we ensured that n/p > sqrt(n)
        if (rank == 0) {
            next_k = k + 1;
            while (!array[next_k - 2]) next_k = next_k + 1;
            k = next_k;  // index to real value
            if (DEBUG) printf("next value of k is %lu \n", k);
        }
        // Now we found the next value of k, we must broadcast it to the other threads
        MPI_Bcast(&k, 1, MPI_INT, 0, MPI_COMM_WORLD);
    }
    if (DEBUG) {
        printf("Prime numbers: \n");
        for (i = 0; i < size; i++) {
            if (array[i]) printf("%lu (thread %d) \n", get_elem_at_index(i, rank, p, n), rank);
        }
    }
    // count the number of primes we found and sum these counts
    // to get the toal number of primes we found
    local_sum = 0;
    global_sum;
    for (i = 0; i < size; i++) {
        if (array[i]) local_sum++;
    }
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        time = MPI_Wtime() - time;
        if (DEBUG) {
            printf("p=%d, n=%lu \n", p, n);
            printf("%lu elements per thread\n", size + 1);
            printf("There are %d prime numbers under %lu. \n", global_sum, n);
            printf("The algorithm took %f seconds to execute \n\n", time);
        } else
            printf("n=%lu p=%d t=%f \n", n, p, time);
    }
    // free memory
    delete (array);

    // Finalize the MPI environment.
    MPI_Finalize();
}