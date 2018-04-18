class symbolTable:
    # SYMBOL_TABLE[token] = [type, value]
    # example:
    # SYMBOL_TABLE['age'] = ['number', 21]

    FILE_RESERVED_WORD = 'SymbolTable/RESERVED_WORD.txt'
    SYMBOL_TABLE = {}
    STR_RESERVED_WORD = 'reserved_word'

    def __init__(self):# global variable

        # read file
        f = open(self.FILE_RESERVED_WORD)
        # for remember reserved word
        self.LIST_RESERVED_WORD = self.readReservedWord(f)
        f.close()

        for reserved_word in self.LIST_RESERVED_WORD:
            self.SYMBOL_TABLE[reserved_word] = attribute(token=self.STR_RESERVED_WORD)

    def readReservedWord(self, f):
        return set(f.read().split())

    def contain(self, item):
        return item in self.LIST_RESERVED_WORD

    def addToken(self, word, type):
        if not self.contain(word) and 'ID' in type.upper():
            self.SYMBOL_TABLE[word] = attribute(token=type)
            return True
        return False

    def showSymbolTable(self):
        for word in self.SYMBOL_TABLE.keys():
            atb = self.SYMBOL_TABLE[word]
            print('{} => token:{}, value:{}'.format(word, atb.type, atb.value))


class attribute:
    type = None
    value = None

    def __init__(self, token=None, value=None):
        self.type = token
        self.value = value
