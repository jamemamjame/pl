'''
Mr. Aphisit Phankosol
Mr. Nattapan Meepiean
'''

import sys


def readFA(f):
    # create new dict(), list_of_qf
    tmp_delta = {}
    tmp_qf = {}

    # read & set dict which keep qf as QF
    ListA = f.readline().strip().split()
    while len(ListA) > 0:
        tmp_qf[int(ListA[0])] = ListA[1]
        ListA = f.readline().strip().split()

    # read again for skip '/n'
    ListA = f.readline().strip().split()

    # read & set transition function as delta
    while len(ListA) > 0:
        # set isLookahead from string -> boolean
        if len(ListA) == 4:  # if length of ListA == 4, it mean this transition has lookahead
            cur_state, symbol, nxt_state, isLookahead = ListA
            isLookahead = True
        else:
            cur_state, symbol, nxt_state = ListA
            isLookahead = False

        # append new (keys, value) into dict
        tmp_delta[int(cur_state), symbol] = (int(nxt_state), isLookahead)

        ListA = f.readline().strip().split()

    return tmp_delta, tmp_qf


def get_symbol_class(sym):
    '''
    This function get char like 'a'-> return this is letter, '5' -> return this is digit
    :param sym: String
    :return: String
    '''
    # is digit
    if sym.isdigit():
        return SYM_DIGIT

    # is letter
    if sym.isalpha():
        return SYM_LETTER
    return None


def isQF(q):
    '''
    Thsi fuction get the state q and it will return that state q is 1 of state final True/False?
    :param q: String
    :return: boolean
    '''
    if q in QF.keys():
        return True
    return False


def Scanner(S_CODE, SYMB_TABLE):
    '''
    This function will return stream of token which contains type
    :param S_CODE: String of source code
    :return:
    '''

    # TRICK: add blank word into last txt (make easy for check that complete)
    S_CODE = S_CODE + BLANK  # เช่น v = s/t บอกได้ว่า v=id = is = s= id / = / แต่ t อะไม่รุ้เพราะมันต้องอ่านตัวต่อไปก่อนถึงจะบอกได้เลยใส่ spacebar ไว้เช็ต lookahead

    # variable preprocessing
    head = 0  # pointer of tape

    # processing
    try:
        while head != len(S_CODE) - 1:  # it mean always do if head != last index(BLANK)
            tmp_string = ''  # geb word to change to id,>,<,blah,blah
            cur_state = 0  # current state
            symbol = S_CODE[head]

            if (symbol is BLANK) or (symbol is NEWLINE) or (symbol is TAB):
                head += 1
            else:
                while not isQF(cur_state):  # while current state not in QF
                    # get a symbol(char) from source code at index == head
                    symbol = S_CODE[head]

                    # calculate & set nxt_state, lookahead
                    if (cur_state,
                        symbol) in delta.keys():  # กรณีนี้ถ้าเจอ  a เช็คกับ letter ไม่ได้,เลขก็เช็คกับ digit ไม่ได้เข้า else หมด เข้าเฉพาะพวก * กับ /
                        nxt_state, lookahead = delta[cur_state, symbol]
                    else:
                        symbol_class = get_symbol_class(
                            symbol)  # เอาsymbol ไปเช็คว่าเป็น digit หรือตัวอักษรจะออกมาเป็นletterหรือdigitเลย
                        if (cur_state, symbol_class) in delta.keys():
                            nxt_state, lookahead = delta[cur_state, symbol_class]  #
                        else:
                            nxt_state, lookahead = delta[cur_state, SYM_OTHER]

                    if not lookahead:  # ไม่เป็น lookahead จะเก็บstringและเลื่อนหัวเลยเพราะเช็คครบแล้ว
                        head += 1  # head tape move 1 step
                        tmp_string += symbol
                    cur_state = nxt_state  # วนเคอต่อด้วnext stage

                # add data into symbol table and stream of token
                # check that in case identifier
                if 'id'.upper() in QF[cur_state].upper():
                    # can add to symbol table -> real identifier
                    if SYMB_TABLE.addToken(tmp_string, QF[cur_state]):
                        STREAM_OF_TOKEN.append(QF[cur_state])  # add สำเร็จก็จะแอดลงโดยไปเช็คใน symbolTable มา
                    else:  # can't add to symbol table -> reserved word
                        STREAM_OF_TOKEN.append(tmp_string)
                else:
                    STREAM_OF_TOKEN.append(QF[cur_state])
    except:
        print(STREAM_OF_TOKEN)
        print(TXT_ERROR)
        sys.exit(0)

    return STREAM_OF_TOKEN


SYM_LETTER = 'letter'  # A-Z, a-z
SYM_DIGIT = 'digit'
SYM_OTHER = 'other'

TXT_ERROR = '\033[93m''syntax is invalid!'  # use warning color
TXT_RESERVED_WORD = 'reserved_word'

# FILE_FA = 'Scanner/mew_fa_scaner.txt'
FILE_FA = 'Scanner/FA.txt'

BLANK = ' '
NEWLINE = '\n'
TAB = '\t'

delta = {}
QF = {}

colorDefault = '\033[99m'
colorMagenta = '\033[95m'

STREAM_OF_TOKEN = []  # answer list

# read a finite automata
with open(FILE_FA, 'r') as scner_file:
    delta, QF = readFA(scner_file)
