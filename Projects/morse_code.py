"""
RULES

* a dot lasts for one unit
* a dash last for three unit

* the space between dots and dashes that are part of the same letter is one unit
* the space between different letters is three units
* the space between different words is seven units

text_to_morse: translates text to morse code with correct timings
no_spacing(text_to_morse): gives morse code without spacing, used for display on webpage

morse_to_text: takes in morse code (from this program) and turns it into text! 
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

def invert_dict():
    codebook = morse_dict()
    for k, v in codebook.items():
        new_v = ''
        for val in v:
            new_v += val
        codebook[k] = new_v
        new_v = ''
    invert = {v: k for k, v in codebook.items()}
    return invert


def morse_to_text(morse):
    invert = invert_dict()
    result = ''
    letter = ''

    c = 0
    while c < len(morse)-1:

        if morse[c+1] == '1': #bit in letter so just add to letter and move forward

            letter+= morse[c]
            c+=2

        elif morse[c+1] == '3': #if letter is complete

            letter += morse[c]
            result += invert[letter]
            letter = ''

            c+=2
        else: #if word is complete, c+1 is 7, same as letter just with a space

            letter += morse[c]
            result += invert[letter] + ' '
            letter = ''
            c+=2

    if len(morse) % 2 == 1: #if morse code is odd need to add the final bit to the incomplete letter
        result += invert[letter + morse[-1]]

    return result
    

