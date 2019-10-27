import random
from itertools import product

def gen_words(chars, length):
    for letters in product(chars, repeat=length):
        yield ''.join(letters)

def main():
    letters = "abc"
    for wordlen in range(3, 10):
        for word in gen_words(letters, wordlen):
            print(word)
            number = random.randint(1, 5)
            print(str(number))

if __name__== "__main__":
    main()