from itertools import product
from time import time

n = 5
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



# This list will eventually hold boolean RREFs for every possible maximal isotropic subspace
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

count = 0
for space in all_spaces:
    # print("_________")
    # for row in space:
    #     print(bin(row))
    count += 1
print(count)




# # TODO essentially do the same thing as above, except the length of each row_data should be n+2
# # and the height of the matrix at the end should be n-1, corresponding to isotropic (n-1)-dimensional subspaces.


# # Gives all nonzero boolean vectors of length n+2
# subspace_row_data_list = list(product([True, False], repeat=n+2))
# # Remove the all-False vector (improves efficiency very slightly, more importantly this makes later code more convenient to write)
# subspace_row_data_list.pop()


# # TODO Again, I would like to refactor the code so it uses recursion to generate the RREF matrices in a depth-first manner


# # This list will eventually hold boolean RREFs for every possible isotropic subspace of dimension n-1
# # We set this list to be the unique 0-row matrix
# all_subspaces = list()
# all_subspaces.append([])

# # We will want n-1 many rows, row_number represents the number of rows we've computed so far
# for row_number in range(n):

#     # Set up a place to store all partial matrices of height row_number + 1
#     temp = list()

#     # For each matrix-in-progress of height row_number...
#     for mat in all_subspaces:
#         # TODO would be preferred to not recompute pivot_indices over and over
#         pivot_indices = []
#         for prev_row in mat:
#             pivot_indices += [prev_row.index(True)]
        
#         # ... and for each candidate for the next row
#         for row_data in subspace_row_data_list:
            
#             # Get the n+1 bits of data required to build the next row into a form we can use easily
#             next_row_data = iter(row_data)

#             # Build the next row by allowing n+1 bits of data to control our n+1 degrees of freedom...
#             # Start by setting everything to 0
#             next_row = [False] * (2 * n)
#             # Fill in the bits that are not "too far to the left" or "under previous pivots" using the n+1 given bits of data
#             for index_within_row in range(n - row_number - 2, 2 * n):
#                 if index_within_row not in pivot_indices:
#                     next_row[index_within_row] = next(next_row_data)

#             # Check RREF condition and update pivot_indices for future RREF checks
#             # TODO updating pivot_indices currently doesn't help, since we are just recomputing it every time
#             if (True in next_row) and (next_row.index(True) < min(pivot_indices + [3 * n])):
#                 pass
#                 # pivot_indices += [next_row.index(True)]
#             else:
#                 continue

#             # Check isotropic condition
#             conflict = False
#             # for prev_row in mat:
#             #     if not isotropic(next_row, prev_row):
#             #         conflict = True
#             #         # break
#             if conflict:
#                 continue
            
#             # RREF and isotropic conditions satisfied, so append this row to the in-progress-matrix
#             # and store this matrix-in-progress of height row_number + 1
#             temp.append(mat + [next_row])

#     # Update all_spaces so it now stores the height row_number + 1 matrices in preparation for the next iteration
#     all_subspaces = temp

# # count = 0
# # for space in all_subspaces:
# #     count += 1
# print(count)


# TODO: Initialize the bipartite graph
# TODO: Adding the COB matrices to the edges
# TODO: Akey[matrix] = randomized
# TODO: create the loop for doing one step of optimization (max bob's stuff subject to the two-hop neighbors)
# TODO: implement the hill-climb (simple)
