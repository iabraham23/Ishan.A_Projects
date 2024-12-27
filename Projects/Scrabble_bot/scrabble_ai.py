# Wade McDermott, Ronen Rosenberg, Ishan Abraham, Suri Castro
from location import *
from board import *
from move import *
from time import time
from collections import Counter

ALL_TILES = [True] * 7
empty_squares = (DOUBLE_LETTER_SCORE, TRIPLE_LETTER_SCORE, DOUBLE_WORD_SCORE, TRIPLE_WORD_SCORE, NO_PREMIUM)


class NigelRichardsAI:
    """ Designed to hopefully beat Nigel Richards (the goat of scrabble) """

    def __init__(self):
        self._gatekeeper = None
        self.played_tiles = set()
        self.last_time = 0

    def set_gatekeeper(self, gatekeeper):
        self._gatekeeper = gatekeeper
        self.played_tiles = set()
        self.last_time = 0

    # could be further optimized to remove from self.played_tiles the tiles which are completely surrounded and thus irrelevant to any further moves
    def scan_board(self):
        for i in range(WIDTH):
            for j in range(WIDTH):
                current_tile = self._gatekeeper.get_square(Location(i, j))
                if (current_tile, (i, j)) not in self.played_tiles and current_tile not in empty_squares:
                    self.played_tiles.add((current_tile, (i, j)))

    def possible_words(self, letter):
        """
        function that finds all words from dict that are possible with hand + a specifc letter on the board
        """
        possible_letters = [letter]
        possible_words = []
        hand = self._gatekeeper.get_hand()
        # the more blanks we have in our hand, the more mismatched letters we can accommodate for
        possible_mistakes = 0
        for letter in hand:
            if letter == '_':
                possible_mistakes += 1
            else:
                possible_letters.append(letter)
        possible_letters = set(possible_letters)
        # iterate through each word in the dictionary and see which are possible to make with our hand + board tiles
        for word in list(DICTIONARY):
            mistakes = 0
            for letter in word:
                if letter not in possible_letters:
                    mistakes += 1
                    if mistakes > possible_mistakes:
                        break
            if mistakes <= possible_mistakes:
                possible_words.append(word)
        return possible_words

    def choose_move(self):
        """Chooses the best move considering score """
        print(time() - self.last_time)
        self.last_time = time()
        best_move = None
        best_score = -1
        # scan board for new plays
        self.scan_board()
        # Try all possible moves: one-tile and multi-tile
        best_move = self._find_best_move()
        if best_move:
            return best_move
        else:
            # If no move is found, exchange tiles
            return ExchangeTiles(ALL_TILES)

    def first_move(self):
        """ This Function is for when our AI goes first"""
        hand = self._gatekeeper.get_hand()
        hand_length = len(hand)
        result = []
        words = []
        for word in list(DICTIONARY):
            words.append((word, Counter(word)))
        new_hand = Counter(hand)
        for scrabble_word, letter_count in words:
            if len(scrabble_word) <= hand_length and not (
                    letter_count - new_hand):
                result.append(scrabble_word)
        best_score = -1
        best_move = None
        for w in result:
            score = self._gatekeeper.score(w, CENTER, HORIZONTAL)
            if score > best_score:
                best_score = score
                best_move = w
        return best_move

    def _find_best_move(self):
        """Evaluates all possible moves and returns the best one."""
        '''broad_possible_words = self.possible_words()'''
        best_score = -1
        best_move = None
        if not self.played_tiles:
            first = self.first_move()
            return PlayWord(first, CENTER, HORIZONTAL)
        # for each tile that has been played so far
        for tile_and_location in self.played_tiles:
            (current_tile_letter, (row, col)) = tile_and_location
            # add additional constraint that current place letter we're anchoring around should be in the possible word
            specific_possible_words = [word for word in self.possible_words(current_tile_letter)]
            # try playing all specific words
            for word in specific_possible_words:
                # at all possible offsets
                for offset in [i for i, letter in enumerate(word) if letter == current_tile_letter]:
                    # and we try playing them both horizontally and vertically
                    location = Location(row - offset, col)
                    # add the spaces necessary to play the word vertically
                    word_with_blanks = word
                    for i in range(len(word)):
                        try:  # try here b/c sometimes this will blindly try to play stuff off the board
                            check_square = self._gatekeeper.get_square(Location(row - offset + i, col))
                        except:
                            break
                        if check_square not in empty_squares:
                            word_with_blanks = word[:i] + " " + word[i + 1:]
                    # try playing vertically
                    if self._is_legal_move(word_with_blanks, location, VERTICAL):
                        score = self._gatekeeper.score(word_with_blanks, location, VERTICAL)
                        if score > best_score:
                            best_score = score
                            best_move = PlayWord(word_with_blanks, location, VERTICAL)
                    location = Location(row, col - offset)
                    # add the blanks necessary to play the word horizontally
                    word_with_blanks = word
                    for i in range(len(word)):
                        try:
                            check_square = self._gatekeeper.get_square(Location(row, col - offset + i))
                        except:
                            break
                        if check_square not in empty_squares:
                            word_with_blanks = word[:i] + " " + word[i + 1:]
                    # try playing horizontally
                    if self._is_legal_move(word_with_blanks, location, HORIZONTAL):
                        score = self._gatekeeper.score(word_with_blanks, location, HORIZONTAL)
                        if score > best_score:
                            best_score = score
                            best_move = PlayWord(word_with_blanks, location, HORIZONTAL)
        return best_move

    def _is_legal_move(self, word, location, direction):
        """Checks if the word is a legal move at the given location and direction and only returns true or false"""
        try:
            self._gatekeeper.verify_legality(word, location, direction)
            return True
        except:
            return False

    # These were some additional ideas we did not get to

    # def test_blank_values()

    # def _evaluate_move(self, word, location, direction):
    #     """Evaluates the move considering score and board state."""
    #     base_score = self._gatekeeper.score(word, location, direction)
    #
    #     # Consider blocking opponent's moves or opening strategic tiles
    #     opponent_block_bonus = self._check_opponent_blocking(word, location, direction)
    #
    #     # Total score considering base and blocking
    #     total_score = base_score + opponent_block_bonus
    #     return total_score

    # def _check_opponent_blocking(self, word, location, direction):
    #     """Checks if the move blocks an opponent's high-scoring opportunity."""
    #     score = 0
    #     # Implement logic to check if the word blocks the opponent’s potential high score
    #     return score