"""
Text to Morse Code, to be displayed in a webpage

RULES

* a dot lasts for one unit
* a dash last for three unit

* the space between dots and dashes that are part of the same letter is one unit
* the space between different letters is three units
* the space between different words is seven units

text_to_morse: translates text to morse code with correct spacing
no_spacing(text_to_morse): gives morse code without spacing, used for display on webpage
"""

def morse_dict():
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


def word_to_morse(string):
    codebook = morse_dict()
    code = ""
    upper_str = string.upper()

    for letter in upper_str:
        if letter not in codebook:
            return f' Cannot translate to morse, unknown letter {letter}'
        x = codebook[letter]
        code+='2'

        for i in x:
            code+= i
            code += '1'
    return code

def text_to_morse(text):
    translate = ''

    for word in text.split():
        translate+=(word_to_morse(word) +'4')

    translate = translate[1:-2] #gets rid of leading 1, final 1 and 4
    cleaned = []

    val = 0
    while val <= len(translate)-1: #summing consecutive numbers, getting correct spacing
        if translate[val].isdigit() and translate[val+1].isdigit():
            if translate[val +2].isdigit():

                x = int(translate[val]) + int(translate[val+1]) + int(translate[val+2])
                cleaned.append(x)
                val +=3
            else:
                cleaned.append(int(translate[val]) + int(translate[val+1]))
                val+=2
        else:
            cleaned.append(translate[val])
            val+=1

    cleaned = ''.join(str(x) for x in cleaned)
    return cleaned

def no_spacing(morse):
    result = ''
    for val in morse:
        if not val.isdigit():
            result+=val
    return result

