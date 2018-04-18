import Scanner.ScannerPL as scner
import LL1_Parser.ParserPL as pser
import SymbolTable.SymbolTablePL as symb_table

FILE_SOURCE_CODE = 'source_code.txt'


def readQuestion(file_name, n_quest):
    f = open(file_name)

    # loop for find question
    while True:
        string = f.readline().split('#')[0].strip()
        if string == str(n_quest) or string == '_end_':
            break

    if string != '_end_':
        # read content of question
        s_code = f.readline().strip()
        f.close()
        return s_code

    f.close()
    return None


if __name__ == '__main__':
    # read source code
    S_CODE = readQuestion(FILE_SOURCE_CODE, 8)

    if S_CODE is not None:
        SYMBOL_TABLE = symb_table.symbolTable()
        STREAM_OF_TOKEN = scner.Scanner(S_CODE, SYMBOL_TABLE)

        tf, PARSE_TREE = pser.Parser(STREAM_OF_TOKEN)

        print('From source code:')
        print(S_CODE)
        print()
        print('Stream of token:')
        print(STREAM_OF_TOKEN)
        print()
        print(tf)

        if tf:
            print('Derivation:')
            PARSE_TREE.showDerivation()
            print('LL1_Parser Tree:')
            PARSE_TREE.showTree()
    else:
        print('have not a received question number.')
