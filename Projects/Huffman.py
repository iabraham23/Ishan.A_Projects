from heapq import heapify, heappush, heappop


"""
Compression using the Huffman Algorithm! 

 CALL create_code('any-string-to-codify') to create a codebook and code

 CALL decode_huffman('code', codebook) to decode
 
Small problem: The way I've written the code if you try to run different strings multiple times it
might not work because node_array and bin_dict are outside of the functions

"""



class Node:  # Node that holds the character and frequency
    def __init__(self, char, freq = 0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    #had to define comparison methods so I could use the heap

    def __eq__(self, other):
        return self.freq == other.freq

    def __lt__(self, other):
        return self.freq < other.freq

    def __gt__(self, other):
        return self.freq > other.name

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)

    def __str__(self):
        return f'[{self.left} {self.char}, {self.freq} {self.right}]'
    def __repr__(self):
        return str(self)


node_array = [] #array of nodes, should turn into a function to get.node_array

def create_frequency(string):
    freq = {}
    for i in string:
        if i in freq:
            freq[i] +=1
        else:
            freq[i] = 1

    for c,f in freq.items():
        node_array.append(Node(c,f))
    #node_array.append(Node(c,f) for c,f in freq.items()): generator doesn't produce string

    return create_min_heap(node_array) #sorts the array of nodes using a min heap


#creating a min heap based on the frequency values, as stated in the comparison methods
def create_min_heap(node_array):
    heap = []
    heapify(heap)
    for n in node_array:
        heappush(heap,n) #inserting into the heap
    return heap

"""
two lowest

pops two lowest frequencies 

also adds a new node that combines the characters and sums the frequencies
- the first node I pop, x, should add a 0 to each character in the node 
- the second node I pop, y, should add a 1 to each character in the node

NOTE: HAVE TO REVERSE THE BITS AT THE END (done in create_code) 

"""

bin_dict = {} #the codebook, should turn into a function to get.bin_dict
def two_lowest(min_heap):
    if len(min_heap) <2:
        return f'Cant pop two lowest'

    x = heappop(min_heap)
    y = heappop(min_heap)

    for i in x.char:
        #print(i)
        if len(y.char) >1:
            if i in bin_dict:
                bin_dict[i] += '1'
            else:
                bin_dict[i] = '1'

        elif i in bin_dict:
            bin_dict[i] += '0'
        else:
            bin_dict[i] = '0'

    for v in y.char:
        #print(v)
        if len(y.char) >1:
            if v in bin_dict:
                bin_dict[v] += '0'
            else:
                bin_dict[v] = '0'

        elif v in bin_dict:
            bin_dict[v] += '1'
        else:
            bin_dict[v] = '1'

    heappush(min_heap, Node((x.char + y.char), (x.freq + y.freq)))
    return f'first popped: {x}, second popped: {y}, bin_dict: {bin_dict}'

def create_code(string):
    x = create_frequency(string)
    i=0

    while i < len(node_array)-1:
        two_lowest(x)
        i+=1

    for key,vals in bin_dict.items(): #reversing the bits in bit_array
        x = vals[::-1]
        bin_dict[key] = x

    code = ''
    for j in string:
        code += bin_dict[j]
    return f'codebook: {bin_dict}, code: {code}'

#huffman decoding
def decode_huffman(code, codebook):

    original_word = ''

    invert_dict = {v: k for k,v in codebook.items()}

    code_check = ''
    for bit in code:
        code_check += bit
        if code_check in invert_dict:
            original_word += invert_dict[code_check]
            code_check = ''
    return original_word






