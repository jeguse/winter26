from itertools import product


n = 4

def dotprod(x,y):
    total = 0
    for i in range(n):
        total += int(x[2*i]) * int(y[2*i+1]) + int(x[2*i+1]) * int(y[2*i])
    return total % 2

def isotropic(x,y):
    return not bool(dotprod(x,y))

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
count = 0
for matrix in product(product('01', repeat=n+1), repeat=n):
    count += 1
print(count)


# TODO: Initialize the bipartite graph
# TODO: Adding the COB matrices to the edges
# TODO: Akey[matrix] = randomized
# TODO: create the loop for doing one step of optimization (max bob's stuff subject to the two-hop neighbors)
# TODO: implement the hill-climb (simple)
