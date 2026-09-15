# Program to add two matrices using NumPy

import numpy as np

# Create first matrix
matrix1 = np.array([
    [1, 2],
    [3, 4]
])

# Create second matrix
matrix2 = np.array([
    [5, 6],
    [7, 8]
])

# Add the two matrices
result = matrix1 + matrix2

# Display matrices
print("First Matrix:")
print(matrix1)

print("\nSecond Matrix:")
print(matrix2)

print("\nAddition of Two Matrices:")
print(result)