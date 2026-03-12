from itertools import product
from random import getrandbits, seed
from time import time

t1 = time()

n = int(input("Value of n: "))
# ---------------------------
# 1 << 2n      =  10...0
# 1 << 2n - 1  =  011..1
all_bits = (1 << 2 * n) - 1
x_mask = all_bits // 3
# basically creates an alternating bitstring of 0's and 1's
# x_mask = 0b0101...
# uses the identity 1 + 4 + 4^2 + ... 4^n = (4^n-1)/3 = (2^2n - 1)/3
z_mask = x_mask ^ all_bits


def commutes(a, b):
    ax = x_mask & a
    az = (z_mask & a) >> 1
    bx = x_mask & b
    bz = (z_mask & b) >> 1
    res = (ax & bz) ^ (az & bx)
    return res.bit_count() & 1 == 0



# This list will eventually hold RREFs in the form [int] for every possible maximal isotropic subspace
# We set this list to be the unique 0-row matrix
all_spaces = list()
all_spaces.append([])

# We will want n many rows, row_number represents the number of rows we've computed so far
for row_number in range(n):

    # Set up a place to store all partial matrices of height row_number + 1
    temp = list()

    # For each matrix-in-progress of height row_number...
    for mat in all_spaces:
        # TODO would be preferred to not recompute pivot_bits over and over
        pivot_bits = set()
        for prev_row in mat:
            pivot_bits.add(2 * n - int.bit_length(prev_row))
            
        # ... and for each candidate for the next row
        for row_data in range(1, 1 << (n + 1)):
            
            # Build the next row by allowing n+1 bits of data to control our n+1 degrees of freedom...
            # Start by setting everything to 0
            next_row = 0
            # Fill in the bits that are not "too far to the left" or "under previous pivots" using the n+1 given bits of data
            k = 1 << n
            for index_within_row in range(n - row_number - 1, 2 * n):
                if index_within_row not in pivot_bits:
                    if (row_data & k).bit_count() == 1:
                        next_row ^= 1 << (2 * n - index_within_row - 1)
                    k >>= 1

            # Check RREF condition
            if len(mat) > 0 and mat[-1] > next_row:
                continue

            # Check isotropic condition
            conflict = False
            for prev_row in mat:
                if not commutes(next_row, prev_row):
                    conflict = True
                    break
            if conflict:
                continue
            
            # RREF and isotropic conditions satisfied, so append this row to the in-progress-matrix
            # and store this matrix-in-progress of height row_number + 1
            temp.append(mat + [next_row])
    # Update all_spaces so it now stores the height row_number + 1 matrices in preparation for the next iteration
    all_spaces = temp

# Some printing to partially verify correctness of the code so far
count = 0
for space in all_spaces:
    # print("_________")
    # for row in space:
    #     print(bin(row))
    count += 1
print("Number of maximal isotropic subspaces found: " + str(count))
print("Time used: " + str(time() - t1) + " seconds")
t1 = time()



# Next, essentially do the same thing as above, except the length of each row_data should be n+2
# and the height of the matrix at the end should be n-1, corresponding to isotropic (n-1)-dimensional subspaces.


# This list will eventually hold RREFs in the form [int] for every possible isotropic subspace of dimension n-1
# We set this list to be the unique 0-row matrix
all_subspaces = list()
all_subspaces.append([])

# We will want n-1 many rows, row_number represents the number of rows we've computed so far
for row_number in range(n-1):

    # Set up a place to store all partial matrices of height row_number + 1
    temp = list()

    # For each matrix-in-progress of height row_number...
    for mat in all_subspaces:
        # TODO would be preferred to not recompute pivot_indices over and over
        pivot_bits = set()
        for prev_row in mat:
            pivot_bits.add(2 * n - int.bit_length(prev_row))
        
        for row_data in range(1, 1 << (n + 2)):
            
            # Build the next row by allowing n+2 bits of data to control our n+2 degrees of freedom...
            # Start by setting everything to 0
            next_row = 0
            # Fill in the bits that are not "too far to the left" or "under previous pivots" using the n+2 given bits of data
            k = 1 << n+1
            for index_within_row in range(n - row_number - 2, 2 * n):
                if index_within_row not in pivot_bits:
                    if (row_data & k).bit_count() == 1:
                        next_row ^= 1 << (2 * n - index_within_row - 1)
                    k >>= 1

            # Check RREF condition
            if len(mat) > 0 and mat[-1] > next_row:
                continue

            # Check isotropic condition
            conflict = False
            for prev_row in mat:
                if not commutes(next_row, prev_row):
                    conflict = True
                    break
            if conflict:
                continue
            
            # RREF and isotropic conditions satisfied, so append this row to the in-progress-matrix
            # and store this matrix-in-progress of height row_number + 1
            temp.append(mat + [next_row])

    # Update all_subspaces so it now stores the height row_number + 1 matrices in preparation for the next iteration
    all_subspaces = temp

# Some printing to partially verify correctness of the (n-1)-dimensional subspace computation
count = 0
for space in all_subspaces:
    count += 1
print("Number of (n-1)-dimensional isotropic subspaces: " + str(count))
print("Time used: " + str(time() - t1) + " seconds")
t1 = time()

# Next, we will compute the bipartite graph of n-dimensional and (n-1)-dimensional isotropic subspaces,
# where edges represent containment of the (n-1)-dimensional space on one side in the n-dimensional space on the other side

# TODO store edges and vertices in a more graph-like structure (e.g. so we can easily find all neighbors of a given vertex)

# Helper function which takes in a vector, of type int, and a matrix in reversed RREF, of type [int],
# and outputs an [int] denoting the coefficients when writing vector in the row span of the matrix,
# or [] if the vector is not in the row span of the matrix
def write_in_basis(vector, basis):
    output = []

    # If vector is in the row span, then it is just a bitwise xor of entries in basis
    # By reversing the basis, we check that the leftmost bits can be satisfied, then move to the right
    for basis_element in reversed(basis):
        # If the vector has a set bit too far to the left to be zeroed out, we will never be able to xor to 0
        if vector.bit_length() > basis_element.bit_length():
            return []
        # If the vector's leftmost set bit and the basis_element's set bit are in the same position, we must xor with this
        # basis_element if we want any hope of xoring to 0
        elif vector.bit_length() == basis_element.bit_length():
            # Record that we xor with this basis_element for expansion in this basis
            output = [1] + output
            vector ^= basis_element
        # Otherwise, we should not xor with this basis_element
        else:
            # Record that we do not xor with this basis_element for expansion in this basis
            output = [0] + output
    # Report either that we couldn't xor to 0 or report the expansion in basis
    if vector != 0:
        return []
    return output


# This dict will eventually hold all edges in the form (large_space, small_space): change_of_basis_matrix
# where the data types are (tuple(int), tuple(int)): [[int]]
cob_matrices = {}

# We check all pairs of n-dimensional spaces and (n-1)-dimensional spaces
for (space_matrix, subspace_matrix) in product(all_spaces, all_subspaces):
    conflict = False
    cob_matrix = []
    # We check that every row of the small matrix is in the row span of the large matrix and compute the COB matrix as we go
    for row in subspace_matrix:
        cob_row = write_in_basis(row, space_matrix)
        if len(cob_row) == 0:
            conflict = True
            break
        cob_matrix += [cob_row]
    # If every basis vector of the small space is indeed in the large space, store the edge for this pair of spaces
    if not conflict:
        cob_matrices[(tuple(space_matrix), tuple(subspace_matrix))] = cob_matrix


# Some code to partially verify that the edges are correct
# TODO find a better way to verify that our set of edges is correct and comprehensive
print("A few samples of edges, for verification purposes:")
for (space_matrix, subspace_matrix) in product(all_spaces[::100], all_subspaces[::100]):
    if (tuple(space_matrix), tuple(subspace_matrix)) in cob_matrices:
        print("_________Large Space_________")
        for row in space_matrix:
            print(row)
        print("_________Small Space_________")
        for row in subspace_matrix:
            print(row)
        print("_______Change of Basis_______")
        print(cob_matrices[(tuple(space_matrix), tuple(subspace_matrix))])
print("Total number of edges found: " + str(len(cob_matrices)))
print("Time used: " + str(time() - t1) + " seconds")
t1 = time()


# For each maximal isotropic subspace Ref could give Alice, she chooses a dual vector.
# To start with, let's make this dual vector random
alice_key = {}

# For repeatability
seed(0)

for matrix in all_spaces:
    alice_key[tuple(matrix)] = getrandbits(n)


# TODO: create the loop for doing one step of optimization (max bob's stuff subject to the two-hop neighbors)

# Basic idea:
# for bob_matrix in all_spaces:
#     # TODO improve graph structure of data storage so that we can compute distance-two neighbors easily
#     for alice_matrix in distance_two(bob_matrix):
#         # TODO write a function that takes in neighboring spaces A and B and a dual vector on A and outputs all compatible dual vectors on B
#         for dual_vector_option in compatible_bob_dual_vectors(alice_key[alice_matrix], bob_matrix):
#             # TODO set up a good way to both count votes and determine who won the election
#             cast_vote(dual_vector_option)
#     elect(dual_vector_with_most_votes)


# TODO: implement the hill-climb (simple)
