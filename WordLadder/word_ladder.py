def word_ladder(source, dest, wordlist):
    return [source, dest]

def mutations(word, alphabet):
    ret = []
    for pos in range(len(word)):
        for c in alphabet:
            ret.append(word[0:pos] + c + word[pos+1:])
    return ret
