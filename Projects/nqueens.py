
def nqueens(n):
    row,col = n,n

    def f(solution):
        if len(solution) == n:
            return solution
        for r in range(col):
            if not conflict(r, solution):
                result = f(solution+[r])
                if result:
                    return result
        return False

    def conflict(i, queens):
        for c,r in enumerate(queens):
            if r == i:
                return True
            if abs(i-r) == abs(len(queens)-c):
                return True
        return False
    return f([])


#idea for backtracking is to have an array we append our solution to, if no solutions
#are possible in the next column over, we remove (pop) the previous choice from our solution and try again
#if no choices are possible we return False


def nqueens_backtracking(n):
    def f(solution):
        if len(solution) == n:
            return solution
        for r in range(n):
            if not conflict(r, solution):
                solution.append(r)
                result = f(solution)
                if result:
                    return result
                solution.pop()
        return False
    def conflict(i, queens):
        for c,r in enumerate(queens):
            if r == i:
                return True
            if abs(i-r) == abs(len(queens)-c):
                return True
        return False
    return f([])

"""
AVG TIMES, ran tests 5 times, average for each category
        nqueens         nqueens_backtracking
3         0 seconds            0 seconds
5         0 seconds            0 seconds
8         0 seconds            0 seconds
20      1.602 seconds        1.568 seconds

The backtracking seems to be faster, more tests would have to be run but from what 
I've seen backtracking is almost always faster 
 
"""