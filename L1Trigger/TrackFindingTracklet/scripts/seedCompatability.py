import numpy as np

my_seeds = ['L3L4', 'L5L6', 'L4L5L6', 'L2L3L4', 'L2L3', 'L2L3D1', 'L1L2', 'L2D1', 'D1D2L2', 'D1D2', 'D3D4', 'L1D1']
seed_vals = [2, 3, 9, 8, 1, 10, 0, 7, 11, 4, 5, 6]

seeds = {
    'L1L2'   : [  1,  2 ],
    'L2L3'   : [   2,  3 ],
    'L3L4'   : [  3,  4 ],
    'L5L6'   : [ 5,  6 ],
    'D1D2'   : [  11, 12 ],
    'D3D4'   : [  13, 14 ],
    'L1D1'   : [  1, 11 ],
    'L2D1'   : [  2, 11 ],
    'L2L3L4' : [ 2,  3,  4 ],
    'L4L5L6' : [  4,  5,  6 ],
    'L2L3D1': [  2,  3, 11 ],
    'D1D2L2' : [  2, 11, 12 ]
}

# my_seeds = seeds.keys()

seedplusprojection = {
    'L1L2'   : [  1,  2,  3,  4,  5,  6, 11, 12, 13, 14 ],
    'L2L3'   : [  1,  2,  3,  4,  5,  6, 11, 12, 13, 14 ],
    'L3L4'   : [  1,  2,  3,  4,  5,  6, 11, 12 ],
    'L5L6'   : [  1,  2,  3,  4,  5,  6 ],
    'D1D2'   : [  1,  2, 11, 12, 13, 14, 15 ],
    'D3D4'   : [  1, 11, 12, 13, 14, 15 ],
    'L1D1'   : [  1, 11, 12, 13, 14, 15 ],
    'L2D1'   : [  1,  2, 11, 12, 13, 14 ],
    'L2L3L4' : [  1,  2,  3,  4,  5,  6, 11, 12, 13 ],
    'L4L5L6' : [  1,  2,  3,  4,  5,  6 ],
    'L2L3D1': [  1,  2,  3, 11, 12, 13, 14 ],
    'D1D2L2' : [  1,  2, 11, 12, 13, 14 ]
}

my_array = np.zeros((len(my_seeds), len(my_seeds)))

for i, iseed in enumerate(my_seeds):
    for j, jseed in enumerate(my_seeds):
        if j >= i:
            if set(seeds[iseed]).issubset(set(seedplusprojection[jseed])) and set(seeds[jseed]).issubset(set(seedplusprojection[iseed])):
                my_array[i][j], my_array[j][i] = 1, 1

            # print(seeds[iseed], seeds[jseed])
            # print(seedplusprojection[jseed], seedplusprojection[iseed])
            # print(" ")

print(my_array)

def submatrix(arr, indices):
    """Return the square submatrix of `arr` restricted to `indices` in both rows and columns.

    Parameters
    ----------
    arr : np.ndarray, shape (N, N)
    indices : sequence of int (or bool mask of length N)
        Order is preserved; repeats are allowed and will be duplicated.

    Returns
    -------
    np.ndarray, shape (len(indices), len(indices)) -- a copy, not a view.
    """
    arr = np.asarray(arr)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"expected a square 2-D array, got shape {arr.shape}")

    idx = np.asarray(indices)
    if idx.dtype == bool:
        if idx.size != arr.shape[0]:
            raise ValueError("boolean mask length must equal N")
        idx = np.flatnonzero(idx)
    else:
        idx = idx.astype(np.intp, copy=False).ravel()
        if idx.size and (idx.min() < -arr.shape[0] or idx.max() >= arr.shape[0]):
            raise IndexError(f"index out of range for N={arr.shape[0]}")

    return arr[np.ix_(idx, idx)]

# seed_vals = [10, 1, 2, 3, 9, 8, 0, 7, 11, 4, 5, 6]

# print(submatrix(my_array, [1, 2, 3, 9, 8, 0]))
# print(submatrix(my_array, [0, 1, 10]))
# print(submatrix(my_array, [0, 4, 7, 11]))
# print(submatrix(my_array, [4, 5, 6]))

# for i, iseed in enumerate(seeds):
#     for j, jseed in enumerate(seeds):
#         if j >= i and i == 1:
#             print(i, j)
#             print(set(seeds[iseed]).union(set(seeds[jseed])))
#             print(seedplusprojection[jseed]) 
#             print(seedplusprojection[iseed])
#             print(" ")

#             # print(seedplusprojection[jseed], seedplusprojection[iseed])
#             # if seeds[iseed] in seedplusprojection[jseed] and seeds[jseed] in seedplusprojection[iseed]:
#             #     print(iseed, jseed)

# # print(my_array)

# # [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
# # [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0]

# containment = np.array([
#     [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],  # L1L2
#     [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],  # L2L3
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],  # L3L4
#     [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],  # L5L6
#     [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],  # D1D2
#     [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # D3D4
#     [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # L1D1
#     [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],  # L2D1
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],  # L2L3L4
#     [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],  # L4L5L6
#     [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],  # L2L3D1
#     [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],  # D1D2L2
# ], dtype=np.int8)

# result = containment & containment.T 

# print(result)