from string import ascii_lowercase
from search import search


def word_ladder(source, dest, wordlist):
    success = lambda path: path[-1] == dest
    children = lambda path: wordlist.filter(
        mutations(path[-1], ascii_lowercase)
    )
    return search(source, success=success, children=children)


def mutations(word, alphabet):
    ret = []
    for pos in range(len(word)):
        for c in alphabet:
            ret.append(word[:pos] + c + word[pos+1:])
    return ret
