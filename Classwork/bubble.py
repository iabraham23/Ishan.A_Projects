#Implementation and time analysis of bubble sort

def bubble_sort(ls, key = lambda x: x):

    for i in range(len(ls)):
        for j in range(0, len(ls)-1-i):
            if key(ls[j]) >= key(ls[j + 1]):
                ls[j], ls[j + 1] = ls[j + 1], ls[j]



#there are two loops, outer runs at the length of the list, so n times, and the
#inner runs at the length of the list minus some integer values, so n times.

#the worst case run time of this algorithm would be when the algorithm must loop through
#both loops completely, so n^2 times, meaning runtime is 0(n^2)

def reverse(ls):
    if all(ls[i]>=ls[i+1] for i in range(len(ls)-1)): #detect if list is in reverse
        ls = ls[::-1] #reverse list in linear time
        return ls
    else:
        print("list is not fully in reverse")













