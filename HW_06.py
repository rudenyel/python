def get_even_or_odd_numbers(stop, only_even):
    return [number for number in range(stop) if number % 2 != int(only_even)]


def search_words(phrase, words):
    return [word for word in words if phrase in word]


def flatten(sequence):
    yield from (item for subsequence in sequence for item in subsequence)


print(get_even_or_odd_numbers(10, True))

print(search_words('he', ['hello', 'orange', 'phenomenon']))

generator = flatten([[1, 2], [], [3, 4, 5]])
print(next(generator))
print(next(generator))
print(next(generator))
