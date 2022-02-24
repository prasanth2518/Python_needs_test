import numpy as np

a = np.array([1, 2, 3])
print(a.shape, a.size, a.ndim)
b = np.array([(1.5, 2, 3), (4, 5, 6)], dtype=float)
print(b.size, b.shape, b.ndim)
c = np.array([[(1.5, 2, 3), (4, 5, 6)], [(3, 2, 1), (4, 5, 6)]], dtype=float)
print(c.shape, c.size, c.ndim)
# TODO Terminology Alert
'''
SHAPE in NUmpy: Shape relates to the size of the dimensions of an N-dimensional array.

SIZE in NUmpy: Size regarding arrays, relates to the amount (or count) of elements that are contained in the array (or sometimes, at the top dimension of the array - when used as length).

EX: 
a =
    1  2  3  4
    5  6  7  8
    9 10 11 12

the shape of a is (3, 4), the size of a is 12 and the size of a[1] is 4.
'''

# todo having "n" shape of zeros
a4 = np.zeros([5, 6])

# todo having "n" shape of ones
unit_matrix = np.ones([5, 9])

# todo having Create an array of evenly spaced values (step value)
step_matrix = np.arange(2, 16, 4)

# todo Create an array of evenly spaced values (number of samples) from start to end
space_value = np.linspace(0, 2, 9)

# todo create constant array os specific number
Constant_matrix = np.full((2, 2), 7)

# todo create identity matrix of required shape
Im = np.eye(2)

# todo create array with the random values
np.random.random((2, 2))

# todo create an empty array
np.empty((3, 2))

# TODO saving and loading to disk
a = np.full([7, 8], 9)
h = np.eye(3)
np.save("myarr1", a)
np.savez("myarray2.npz", a, h)
np.load("file_name.ext")

# TODO Saving & Loading Text Files
a1 = np.array([345, 46, 57])
np.loadtxt("myfile.txt")
np.genfromtxt("my_file.csv", delimiter=',')
np.savetxt("myarray.txt", a1, delimiter=" ")

# TODO DATA-TYPES

'''
np.int64                               Signed 64-bit integer types
np.float32                              Standard double-precision floating point
np.complex                              Complex numbers represented by 128 floats
np.bool                                  Boolean type storing TRUE and FALSE values
np.object                                Python object type
np.string_                               Fixed-length string type
np.unicode_                              Fixed-length unicode type
'''

# TODO INSPECTING ARRAY:

A = np.array([32, 5, 745, 85], [345, 534, 53, 53])
'''
a.shape = Array dimensions
len(a) = Length of array
a.ndim =Number of array dimensions
e.size = Number of array elements
a.dtype = Data type of array elements
a.dtype.name = Name of data type
a.astype(format) = Convert an array to a different type
'''
# todo ARRAY MATHEMATICS

a = np.array([[32523, 5234], [23552, 523]])
b = np.array([[235, 364], [2, 2423]])

sub = np.subtract(a, b)
sub = a - b

np.add(a, b)
a + b

np.exp(b)
np.sqrt(b)
np.square(b)
np.sin(a)
np.log(a)

# TODO COmparison
# Elememt wise comparision
d = a == b
r = np.array([[False, True, True],
              [False, False, False]], dtype=bool)
# array wise comparision
np.array_equal(a, b)

# TODO Aggregate functions
# Cumulative sum of the elements
b.cumsum(axis=1)

#
np.corrcoef()
np.std(a)
a.sum()
a.mean()
a.median()

# Todo Copying Array

h = a.view()  # Create a view of the array with the same data
nc = np.copy(a)  # normal_copy
dp = a.copy()  # deepcopy

# todo sorting rows
a.sort()
a.sort(axis=0)

# todo subsetting
a = np.array([543, 3434, 34634, 34, 345])
a[2]
a = np.array([[23, 423], [4, 23]])

# todo slicing

a[0:1]  # 23,423

a[0:1, 1]  # 423

a[::-1]  # reversrd array

# todo Array Manipulation

p = np.transpose(a)
p.T

# changing array shape
a.ravel()  # flattrenn the a as a vector
a.reshape(3, 3)

# appending elememts/removing element

h.resize([23, 4])

np.append(h, p)
np.delete(a, [1])

# combining arrays

np.concatenate((a, d), axis=0)
np.vstack((a, b))  # Stack arrays vertically (row-wise) =np.r_[e,f]
np.hstack((a, b))  # Stack arrays horizontally (row-wise)
np.column_stack((a, d))  # create stacked column wise arrayds  np.c_[a,d]

# todo splitting arrays

np.hsplit(a, 3)  # split horizontally
np.vsplit(c, 2)  # split vertically
