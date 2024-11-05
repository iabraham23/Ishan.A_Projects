#implementation of Hoorspool's string matcher

#graphs the time the algorithm takes as our input text and pattern increase in size
#each test (for each length of text; 10,100,1000 characters) is run 50 times then the average is plotted


import random
import string
from random import randint
import time
import matplotlib.pyplot as plt


class HorspoolStringMatcher():
    def __init__(self, pattern):
        self.pattern = pattern
        self.shift_table = {}
        #self.shift_table = dict((ch,0) for ch in set(pattern)) #don't need to set keys
        for i in range(len(pattern)-1):
            self.shift_table[pattern[i]] = len(pattern) -1 -i

    def __str__(self): #used to help make sure init is correct
        for key, val in self.shift_table.items():
            print(f"key: {key} val: {val}")

    def __repr__(self):
        return str(self)

    def match(self, text):
        m = len(self.pattern)
        n = len(text)


        j = m-1 #pattern index
        k = m-1 #text index should start at the same as len(pattern)-1

        c=0
        match_found = -1

        while j>=0 and k<=n:
            if self.pattern[j] == text[k]:

                j-=1

                k-=1

                c+=1

                if c == len(self.pattern):
                    match_found = k+1
                    break
            else:

                shift = self._get_shift(text[k+c])
                j = m - 1
                #print(f"shifted character: {text[k+c]}, index:{k}")
                k+=shift+c
                c = 0


        return match_found

    def _get_shift(self, character):
        if character in self.shift_table:
            return self.shift_table[character]
        return len(self.pattern)



def generate_random_text(n):
    text = ''.join(random.choices(string.ascii_lowercase,k=n))
    return str(text)
    
def pattern_from_text(text):
    start = randint(0, len(text)//2)
    end = randint(len(text)//2 +1, len(text))
    #print(f" start: {start}, end: {end}")
    return text[start:end]
    
def random_match(n):
    text = generate_random_text(n)
    pat = pattern_from_text(text)
    matcher = HorspoolStringMatcher(pat)
    start = time.time()
    index = matcher.match(text)
    end = time.time()
    time_elapsed = end-start
    #print(f"pattern: {pat}, text: {text}, index: {index}")
    return time_elapsed

avg_time = []

def do_match(n, k): # n is length of text, k is how many times we run to get avg
    total_time = 0
    for _ in range(k):
        timed = random_match(n)
        total_time += timed
    average = (total_time / k)
    avg_time.append([average, n])

    return average, n, k

#running tests, each n value run 50 times
do_match(10,50)
do_match(100,50)
do_match(1000,50)
print(avg_time)

times = [entry[0] for entry in avg_time]
lengths = [entry[1] for entry in avg_time]

# Creating the plot
plt.figure(figsize=(8, 5))
plt.plot(lengths, times, marker='o', linestyle='-', color='b', label='Avg time per length')
plt.xlabel('Length of Text')
plt.ylabel('Average Time (seconds)')
plt.title('Average Time vs. Length of Text')
plt.grid(True)
plt.legend()
plt.show()















