#Different algorithms for finding matrix multiplication

#brute force vs different methods, understanding time complexity for each


def dot_product(a,b):
    sum(x*y for x,y in zip(a,b))
    #generator comprehension vs a list comprehension: sum([x*y for x,y in zip(a,b)])

def brute_mult(a,b):
    n = len(a)

    result = [[0] * n for _ in a]
    for i in range(len(a)):
        for j in range(len(b)):
            for x in range(len(a[0])):
                result[i][j] += a[i][x] * b[x][j]
    return result

def mat_add(A, B):
    n = len(A)
    result = [[0] * n for _ in A]

    for i in range(len(A)):
        for j in range(len(A)):
            result[i][j] = A[i][j] + B[i][j]

    return result

def strassen_mult(a,b):
    if len(a) == 1:
        return brute_mult(a,b)

def get_quadrant(a, hhalf, vhalf):
    """
    :param a: the matrix we want a piece of
    :param hhalf: 0 for top, 1 for bottom
    :param vhalf: 0 for left, 1 for right
    :return: that quadrant of the matrix
    """
    n = len(a)
    hstart = hhalf * n//2
    vstart = vhalf * n//2

    return [row[vstart:vstart+n//2] for row in a[hstart: hstart + n//2]]

def assemble(top_left, top_right, bottom_left, bottom_right):
    n = len(top_left[0])
    result = []
    for i in range(n):
        result.append([vals for vals in zip(top_left[i], top_right[i])])
    return result
tleft = [[1,2],[3,4]]
tright = [[5,6],[7,8]]





#a = [[2,3],
 #    [5,1]]
#b = [[8,6],
  #   [0,4]]

#some notes
#1 means 10th digit, 0 means ones digit, 10^1 or 10^0

#a = a1a0
#b = b1b0
#c = a*b
# c2 = a1 * b1
# c0 = a0 * b0
# c1 = (a1 + a0) * (b1+b0) - (c2 + c0)

#recursive so t(n) = {1 if n=1, 3T(n/2) otherwise}, 3 operations that are halving each time



#more notes

#t(n) = 7t(n/2)
# 2^k = n
#t(2^k) = 7t(2^(k-1))
# after simplifications we get n^~2.8, strassens matrix multiplication





