"""
Quickly made simplistic guessing game where you try and guess the order of the numbers 1-5
Basic concept of Wordle or other guessing games 
"""

from random import shuffle

class guessing_game:
    def __init__(self):
        self.hand = None
        self.correct = False
        self.right_place = 0
        self.random_start()
        self.run()

    def random_start(self):
        lst = [1, 2, 3, 4, 5]
        shuffle(lst)
        self.hand = lst

    def is_guess_correct(self, g):
        return g == self.hand

    def run(self):
        guess = input("type a guess (numbers 1 to 5 separated by commas)")
        g = []
        for l in guess:
            if l != ',':
                g.append(int(l))
        if len(g) !=5:
            print('Guess 5 numbers')
            self.run()
        for index, num in enumerate(g):
            if num == self.hand[index]:
                self.right_place +=1
        if self.right_place == 5:
            print('you got it!')
        else:
            print(f'number of correct places: {self.right_place}')
            self.right_place = 0
            self.run()

game = guessing_game()

