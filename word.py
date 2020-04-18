class Word:
    def __init__(self, name, _type):
        self.letterValue = {'a': 1, 'b': 2, 'c': 3, 'ç': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'ğ': 9, 'h': 10, 'ı': 11,
                            'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18, 'ö': 19, 'p': 20, 'r': 21,
                            's': 22, 'ş': 23, 't': 24, 'u': 25, 'ü': 26, 'v': 27, 'y': 28, 'z': 29}
        self.name = name
        self._type = _type
        self.value = self.__find_value__()

    def __find_value__(self):
        total = 0
        for letter in self.name:
            if letter not in self.letterValue:
                continue
            total += self.letterValue[letter]

        return total
