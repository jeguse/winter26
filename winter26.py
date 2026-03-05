from itertools import product


n = 4

def dotprod(x,y):
    total = 0
    for i in range(n):
        total = total ^ (x[2 * i] and y[2 * i + 1]) ^ (x[2 * i + 1] and y[2 * i])
    return total

def isotropic(x,y):
    return not dotprod(x,y)

def rrefcheck(x,y):
    if x < y or x[y.find('1')] == '1': return False
    return True

# Pauli matrices
paulis = ['01', '10', '11']
# Pauli matrices and I
paulisi = ['00', '01', '10', '11']


# If row 1 starts with I, then we will have a dead end, so we force row 1 to start with non-I
# This will eventually store all candidates to be row 1
row1s = paulis

# This will eventually store all vectors at all
vecs = paulisi


#for row in product('01', n+1):



# # This fills in all possible vectors
# for i in range(n-1):
#     temp1 = []
#     temp2 = []
#     for m in paulisi:
#         for vec in row1s:
#             # take every possible vector currently in row1 and every possible "next tensor component" and pairwise concatenate
#             temp1.append(vec + m)
#         for vec in vecs:
#             temp2.append(vec + m)
#     row1s = temp1
#     vecs = temp2

# # No point considering the all-0 vector
# vecs.pop(0)

# # Improvement idea: instead of looping over length-2n bit strings, loop over length-(n+1) bit strings

# allspaces = []
# # gives all possible starts
# for row in vecs: # row1s
#     allspaces.append([row])
# for i in range(n-1):
#     temp = []
#     for mat in allspaces:
#         for vec in vecs:
#             conflict = False
#             for row in mat:
#                 if not(rrefcheck(vec,row) and isotropic(vec,row)):
#                     conflict = True
#             if not conflict:
#                 temp.append(mat + [vec])
#     allspaces = temp


# # printing some results for checking
# for mat in allspaces:
#     print("__________")
#     for row in mat:
#         print(row)


# print(len(allspaces))

n = 5
# count = 0
# for matrix in product(product('01', repeat=n+1), repeat=n):
#     count += 1
# print(count)


# Gives all nonzero boolean vectors of length n+1, which is enough data to define the next row at each step of our algorithm
row_data_list = list(product([True, False], repeat=n+1))
# Remove the all-False vector (improves efficiency very slightly, more importantly this makes later code more convenient to write)
row_data_list.pop()

# A small note: there is an issue that I am building all 2-row matrices before building a single 3-row matrix,
# rather than a depth-first approach
# TODO I would like to refactor the code so it uses recursion to generate the RREF matrices in a depth-first manner
# Keeping track of the pivoting indices for each matrix separately is the primary concern, though,
# and I'm optimistic that this is not a large issue.
pivot_indices = []


# This list will eventually hold boolean RREFs for every possible maximal isotropic subspace
# We set this list to be the unique 0-row matrix
all_spaces = list()
all_spaces.append([])

# We will want n many rows, so we iterate over the number of rows we've computed so far
for row_number in range(n):

    # Set up a place to store all partial matrices of height row_number + 1
    temp = list()

    # For each matrix-in-progress of height row_number...
    for mat in all_spaces:
        # TODO would be preferred to not recompute pivot_indices over and over
        pivot_indices = []
        for prev_row in mat:
            pivot_indices += [prev_row.index(True)]
        
        # ... and for each candidate for the next row
        for row_data in row_data_list:
            
            # Get the n+1 bits of data required to build the next row into a form we can use easily
            next_row_data = iter(row_data)

            # Build the next row by allowing n+1 bits of data to control our n+1 degrees of freedom...
            # Start by setting everything to 0
            next_row = [False] * (2 * n)
            # Fill in the bits that are not "too far to the left" or "under previous pivots" using the n+1 given bits of data
            for index_within_row in range(n - row_number - 1, 2 * n):
                if index_within_row not in pivot_indices:
                    next_row[index_within_row] = next(next_row_data)

            # Check RREF condition and update pivot_indices for future RREF checks
            # TODO updating pivot_indices currently doesn't help, since we are just recomputing it every time
            if (True in next_row) and (next_row.index(True) < min(pivot_indices + [3 * n])):
                pass
                # pivot_indices += [next_row.index(True)]
            else:
                continue

            # Check isotropic condition
            conflict = False
            for prev_row in mat:
                if not isotropic(next_row, prev_row):
                    conflict = True
                    # break
            if conflict:
                continue
            
            # RREF and isotropic conditions satisfied, so append this row to the in-progress-matrix
            # and store this matrix-in-progress of height row_number + 1
            temp.append(mat + [next_row])

    # Update all_spaces so it now stores the height row_number + 1 matrices in preparation for the next iteration
    all_spaces = temp

count = 0
for space in all_spaces:
    count += 1
print(count)




# TODO essentially do the same thing as above, except the length of each row_data should be n+2
# and the height of the matrix at the end should be n-1, corresponding to isotropic (n-1)-dimensional subspaces.


# Gives all nonzero boolean vectors of length n+2
subspace_row_data_list = list(product([True, False], repeat=n+2))
# Remove the all-False vector (improves efficiency very slightly, more importantly this makes later code more convenient to write)
subspace_row_data_list.pop()


# TODO Again, I would like to refactor the code so it uses recursion to generate the RREF matrices in a depth-first manner


# This list will eventually hold boolean RREFs for every possible isotropic subspace of dimension n-1
# We set this list to be the unique 0-row matrix
all_subspaces = list()
all_subspaces.append([])

# We will want n-1 many rows, row_number represents the number of rows we've computed so far
for row_number in range(n):

    # Set up a place to store all partial matrices of height row_number + 1
    temp = list()

    # For each matrix-in-progress of height row_number...
    for mat in all_subspaces:
        # TODO would be preferred to not recompute pivot_indices over and over
        pivot_indices = []
        for prev_row in mat:
            pivot_indices += [prev_row.index(True)]
        
        # ... and for each candidate for the next row
        for row_data in subspace_row_data_list:
            
            # Get the n+1 bits of data required to build the next row into a form we can use easily
            next_row_data = iter(row_data)

            # Build the next row by allowing n+1 bits of data to control our n+1 degrees of freedom...
            # Start by setting everything to 0
            next_row = [False] * (2 * n)
            # Fill in the bits that are not "too far to the left" or "under previous pivots" using the n+1 given bits of data
            for index_within_row in range(n - row_number - 2, 2 * n):
                if index_within_row not in pivot_indices:
                    next_row[index_within_row] = next(next_row_data)

            # Check RREF condition and update pivot_indices for future RREF checks
            # TODO updating pivot_indices currently doesn't help, since we are just recomputing it every time
            if (True in next_row) and (next_row.index(True) < min(pivot_indices + [3 * n])):
                pass
                # pivot_indices += [next_row.index(True)]
            else:
                continue

            # Check isotropic condition
            conflict = False
            for prev_row in mat:
                if not isotropic(next_row, prev_row):
                    conflict = True
                    # break
            if conflict:
                continue
            
            # RREF and isotropic conditions satisfied, so append this row to the in-progress-matrix
            # and store this matrix-in-progress of height row_number + 1
            temp.append(mat + [next_row])

    # Update all_spaces so it now stores the height row_number + 1 matrices in preparation for the next iteration
    all_subspaces = temp

count = 0
for space in all_subspaces:
    count += 1
print(count)


# TODO: Initialize the bipartite graph
# TODO: Adding the COB matrices to the edges
# TODO: Akey[matrix] = randomized
# TODO: create the loop for doing one step of optimization (max bob's stuff subject to the two-hop neighbors)
# TODO: implement the hill-climb (simple)
