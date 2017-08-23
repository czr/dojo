# def anagrams(words):
    # Some method to generate index from words

# def getFile(filename):
#     content = open(file, 'r')
#     list_of_words = content.readlines()
#     result = anagrams(

def generate_index_key(word):
    return ''.join(sorted(word))

class AnagramFinder():
    """docstring for Anagrams."""
    def __init__(self):
        self.index = {}

    def add_word(self, word):
        key = generate_index_key(word)
        if key in self.index:
            if not word in self.index[key]:
                self.index[key].append(word)
                self.index[key].sort()
        else:
            self.index[key] = [word]

    def dump_anagrams(self):
        return sorted(
            self.index.values(),
            key = lambda wordlist: wordlist[0]
        )
