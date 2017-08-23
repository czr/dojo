import anagrams

def test_willGenerateIndexKeyFromWord():
    assert anagrams.generate_index_key('fred') == 'defr'

def test_addWordToAnagramFinder():
    finder = anagrams.AnagramFinder()
    finder.add_word('fred')
    assert finder.dump_anagrams() == [['fred']]

def test_addDistinctWordsToAnagramFinder():
    finder = anagrams.AnagramFinder()
    finder.add_word('fred')
    finder.add_word('barry')
    assert finder.dump_anagrams() == [['barry'], ['fred']]

def test_addAnagramWordsToAnagramFinder():
    finder = anagrams.AnagramFinder()
    finder.add_word('pinkish')
    finder.add_word('kinship')
    assert finder.dump_anagrams() == [['kinship', 'pinkish']]

def test_addDuplicateAnagramsToAnagramFinder():
    finder = anagrams.AnagramFinder()
    finder.add_word('fred')
    finder.add_word('fred')
    assert finder.dump_anagrams() == [['fred']]

def test_generateIndexFromWordlist():
    pass

def test_readWordlistFromFile():
    pass
