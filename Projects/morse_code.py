"""
RULES

* a dot lasts for one second
* a dash last for three seconds

* the space between dots and dashes that are part of the same letter is one second
* the space between different letters is three seconds
* the space between different words is seven seconds

NOTE: doesn't need to be a second, any unit
"""

def morse_dict(): #1 is dot 3 is dash
    #codebook = {chr(x): [] for x in range(ord('A'), ord('Z')+1)}
    #return codebook
    codebook = {'A': ['*', '-'], 'B': ['-', '*', '*', '*'], 'C': ['-', '*', '-', '*'],
                'D': ['-', '*', '*'], 'E': ['*'], 'F': ['*', '*', '-', '*'], 'G': ['-', '-', '*'],
                'H': ['*', '*', '*', '*'], 'I': ['*', '*'], 'J': ['*', '-', '-', '-'], 'K': ['-', '*', '-'],
                'L': ['*', '-', '*', '*'], 'M': ['-', '-'], 'N': ['-', '*'], 'O': ['-', '-', '-'], 'P': ['*', '-', '-', '*'],
                'Q': ['-', '-', '*', '-'], 'R': ['*', '-', '*'], 'S': ['*', '*', '*'], 'T': ['-'], 'U': ['*', '*', '-'],
                'V': ['*', '*', '*', '-'], 'W': ['*', '-', '-'], 'X': ['-', '*', '*', '-'],
                'Y': ['-', '*', '-', '-'], 'Z': ['-', '-', '*', '*']}
    return codebook


def dash_dot():
    book = morse_dict()
    for key,vals in book.items():
        c = 0
        while c < len(vals):
            if vals[c] == 1:
                vals[c] = '*'
            else:
                vals[c] = '-'
            c+=1
    return book



def word_to_morse(string):
    codebook = morse_dict()
    code = ""
    upper_str = string.upper()

    for letter in upper_str:
        x = codebook[letter]
        code+='2'

        for i in x:
            code+= i
            code += '1'
    return code

def text_to_morse(text):
    translate = ''

    for word in text.split():
        translate += word_to_morse(word) +'4'
    return translate[1:-2] #gets rid of leading 1, final 1 and 4

def no_spacing(morse):
    result = ''
    for val in morse:
        if not val.isdigit():
            result+=val
    return result

