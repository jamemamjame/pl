import LL1_Parser.ParseTree as pTree
import Other.String2Color as scolor
from Other.Constant import constant as cont


def readGrammar(f):
    set_nonterminal = set()  # set of non-terminal symbol
    table_grammar = {}  # dict() to save grammar rule

    # # i use for remember production rule
    i = 1

    while True:
        # read line
        tmpStr = f.readline()

        # if this line have no word, it mean we should stop read file
        if len(tmpStr) == 0:
            break

        # ListA will be: ['ifSt', 'if cond then thenPart']
        ListA = tmpStr.strip().split(' -> ')

        # add grammar in dataStruc like: table_grammar[1, 'ifSt'] = ['if', 'cond', 'then', 'thenPart']
        table_grammar[i, ListA[0].strip()] = ListA[1].strip().split(' ')

        # get a start symbol
        if i == 1:
            start_symbol = ListA[0]# start_symbol = prog

        i += 1

    # setup to know what is non-terminal
    for _, item in table_grammar.keys():#บรรทัด กับ  item
        set_nonterminal = set_nonterminal.union({item})

    return start_symbol, table_grammar, set_nonterminal


def isTerminal(item):
    return item not in SET_NONTERMINAL


def Find_FirstSet():
    # create tmp of first dict
    first = {}  # first is dict

    for n_tmn in SET_NONTERMINAL:
        first[n_tmn] = set()

    # for loop check every production rule that has A -> Empty
    for Head in TABLE_GRAMMAR.keys():
        # for loop check every symbol of value of production rule
        if EMPTY in TABLE_GRAMMAR[Head]:
            first[Head[1]] = first[Head[1]].union({EMPTY})  # Head = key มี 2ค่า(เลขบรรทัด,nontermianl)และมันจะเอา first nonterminal ที่มี empty จะมี empty
            break  #

    while True:  # Python ไม่มี do while Python ต้องเขียนเป็น While True และ มี if ข้างล่าง
        hvChange = False  # boolean เช็คการเปลี่ยนแปลง

        # for loop in every production rule
        for Head in TABLE_GRAMMAR.keys():  # วน Head ใน key
            head = Head[1]  # Head[1] คือ nonterminal นะจ๊ะ

            # get a value list
            tmpProduction = TABLE_GRAMMAR[Head]  # ได้อันขวาอะ(production)

            # remember old size for decide that number of item was changed
            old_size = len(first[head])  # จำ Size เดิมของ first nontermainal

            i = 0
            hvEmp = True

            # algorithm for add first item
            while i < len(tmpProduction) and hvEmp:
                symbol = tmpProduction[i]  # Ri คือ symbol
                hvEmp = False  # ไม่มีการเปลี่ยนแปลง

                if isTerminal(symbol):  # ถ้ามันเป็น Terminal มันแล้วก็เอา มันมาเลย
                    first[head] = first[head].union(set([symbol]))
                else:
                    first[head] = first[head].union(
                        first[symbol] - set([EMPTY]))  # ถ้ามันไม่เป็น Terminal มันแล้วก็เอา มันมาเลย
                    if EMPTY in first[symbol]:  # มีว่าง
                        hvEmp = True
                        i += 1  # เลื่อดูตัวต่อไป

            # check that every symbol in value production can rewrite to EmptyString
            if hvEmp:
                first[head] = first[head].union(set([EMPTY]))

            # check that size of first is change
            if old_size != len(first[head]):
                hvChange = True

        if not hvChange:
            break

    return first


def Find_FollowSet():
    hvChange = False

    # create tmp of follow dict
    follow = {}

    for n_tmn in SET_NONTERMINAL:
        follow[n_tmn] = set()  # follow is dict

    follow[START_SYMBOL] = set(['$'])  # start symbol follow is $

    while True:  # Python ไม่มี do while Python ต้องเขียนเป็น While True และ มี if ข้างล่าง
        hvChange = False

        for Head in TABLE_GRAMMAR.keys():
            head = Head[1]

            # get a value list
            tmpProduction = TABLE_GRAMMAR[Head]

            i = 0
            while i < len(tmpProduction):
                # get the symbol from production
                symbol = tmpProduction[i]

                # we don't care a symbol which is terminal
                if not isTerminal(symbol):  # ดูเฉพาะ non-terminal
                    # remember old size for decide that number of item was changed
                    old_size = len(follow[symbol])

                    # find next first
                    nextFirst = getFirst(tmpProduction[i + 1:])  # i+1: คือตัดทีี่ i+1 ถึงตัวสุดท้าย

                    follow[symbol] = follow[symbol].union(nextFirst - {EMPTY})  # followของตัวเอง U first ของตัวข้างหลังจนถึงตัวสุดท้าย(เพื่อเช่น first(B) is ก ข ค e ต้องมี e เพื่่อเมื่อ  first B = e ให้ไปเอา first ตัวต่อไป
                    # และ nextFirst หาได้จาก getFirst
                    if EMPTY in nextFirst:  # ถ้ามี empty ทุกตัวใน first fllow ของ Ri ต้อง U กับหัวด้วย ไอเจมมันหามาแล้วว่าถ้าใน newtFirst มี empty คือ firstตัวหลังมี emptyทุกตัว
                        follow[symbol] = follow[symbol].union(follow[head])

                    # check that size of first is change
                    if old_size != len(follow[symbol]):  # ถ้ามีการเปลี่ยนแปลง
                        hvChange = True

                i += 1

        if not hvChange:
            break

    return follow


def getFirst(list_production):
    '''
    This function get a list that contain many symbol but it will find a first of possible non-terminal rewrite
    :param list_production:
    :return:
    '''

    tmpFirst = set()

    for symbol in list_production:
        if isTerminal(symbol):
            tmpFirst = tmpFirst.union({symbol})
            return tmpFirst
        else:
            tmpFirst = tmpFirst.union(FIRST[symbol] - {EMPTY})

            # if this symbol can rewrite to EmpString
            if EMPTY in FIRST[symbol]:
                # go to next symbol
                continue
            else:
                return tmpFirst

    return tmpFirst.union({EMPTY})


def Find_LL1(FIRST, FOLLOW):
    LL1 = {}  # LL1 เป็น dict

    for Head in TABLE_GRAMMAR:  # วนทุกกฏ
        # head -> X
        head = Head[1]

        # X is the first symbol of production such as A -> XYZ (focus on left item only, then we use tail index = 0 (tail[0]))
        X = TABLE_GRAMMAR[Head]

        # loop on each symbol which is First of X
        # symbol always be a terminal
        for symbol in (getFirst(X) - set([EMPTY])):
            if (head, symbol) in LL1.keys():
                print('{}, old: LL1[{}, {}] = {}'.format(scolor.StringColor('Error', color='Red'), head,
                                                         symbol, LL1[head, symbol]))
            LL1[head, symbol] = Head

        if EMPTY in getFirst(X):
            # just check for sure
            if head in FOLLOW.keys():
                for symbol in FOLLOW[head]:
                    if (head, symbol) in LL1.keys():
                        print('{}, old: LL1[{}, {}] = {}'.format(scolor.StringColor('Error', color='Red'), head,
                                                                 symbol, LL1[head, symbol]))
                    LL1[head, symbol] = Head

    return LL1


def printRevive(stack, steam_of_token, index):
    for a in steam_of_token[0: index]:
        print('{} '.format(scolor.StringColor(a, color='Magenta')), end='')
    for i in range(1, len(stack) + 1):
        print('{} '.format(stack[-i]), end='')
    print()


def generateTree(STEAM_OF_TOKEN):  # รับพวก id = id + id
    # create new stack
    STACK = []

    STACK.append('$')
    STACK.append(START_SYMBOL)

    # create the Parse Tree which start symbol be root
    parseTree = pTree.ParseTree(root=START_SYMBOL, set_non_terminal=SET_NONTERMINAL)

    # i use to count index of stream of token
    i = 0
    while i < len(STEAM_OF_TOKEN) and len(STACK) != 0:  # stack ไม่ว่าง และ ไอ id = id + id != null
        # print derive
        # printRevive(STACK, STEAM_OF_TOKEN, i)

        top_of_stack = STACK.pop()
        token = STEAM_OF_TOKEN[i]  # always be non-terminal

        # check that if top_of_stack is Empty, we will don't care about this top_of_stack
        if top_of_stack == EMPTY:
            parseTree.change_focus()
            continue

        # check that top of stack is non-terminal or not?
        if not isTerminal(top_of_stack):
            # check exist key
            if (top_of_stack, token) in LL1_TABLE.keys():
                # Head can tell what is the number of production rule that we should uses -> ex. (1, ifSt)
                Head = LL1_TABLE[top_of_stack, token]
                Production = TABLE_GRAMMAR[Head]

                # loop for push element into stack from last index to first index
                for k in range(1, len(Production) + 1):
                    STACK.append(Production[-k])

                # set parse tree
                parseTree.derive(top_of_stack, Production)  # ส่ง top of stack กับ ลูกมันคือการเชื่อม แม่กับลูก
            else:
                # wrong grammar!
                break

        # top of stack is terminal
        else:
            if top_of_stack == token:
                i += 1
                parseTree.change_focus()  # pop ทิ้งไป
            else:
                # wrong grammar!
                break

    if i >= len(STEAM_OF_TOKEN) and len(STACK) == 0:
        return True, parseTree
    else:
        return False, None


LINE = '--------------------------------------'
EMPTY = cont.EMPTY

FILE_GRAMMAR = 'LL1_Parser/GRAMMAR_verA.txt'
# FILE_GRAMMAR = 'LL1_Parser/Khong_Grammar.txt'
f = open(FILE_GRAMMAR)

START_SYMBOL, TABLE_GRAMMAR, SET_NONTERMINAL = readGrammar(f)  # มันคือตาราง grammar SET_NONTERMINAL คือฝั่งซ้าย

# Find first & follow
FIRST = Find_FirstSet()
FOLLOW = Find_FollowSet()

# Find LL(1) table
LL1_TABLE = Find_LL1(FIRST, FOLLOW)


def Parser(streamOftoken):
    # pp.pprint(TABLE_GRAMMAR)
    # pp.pprint(FIRST)
    # pp.pprint(FOLLOW)
    # pp.pprint(LL1_TABLE)

    STEAM_OF_TOKEN = list(streamOftoken)
    STEAM_OF_TOKEN.append('$')
    tf, P_TREE = generateTree(STEAM_OF_TOKEN)
    return tf, P_TREE
