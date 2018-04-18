import Scanner.ScannerPL as scner
from SLR_Parser.SLR1 import slr_parse_tree
import SymbolTable.SymbolTablePL as symb_table

SOURCE_CODE = 'year = 12 + 6'
SYMBOL_TABLE = symb_table.symbolTable()
STREAM_OF_TOKEN = scner.Scanner(SOURCE_CODE, SYMBOL_TABLE)
derive_img = slr_parse_tree(steam_of_tokens=STREAM_OF_TOKEN)

# for line in derive_img:
#     stack, input, action = line
#     print(stack, '\t', input, '\t', action)