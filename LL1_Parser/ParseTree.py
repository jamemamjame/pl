'''
Left most derivation
'''

import LL1_Parser.Node as tNode
import Other.String2Color as scolor
from Other.Constant import constant as cont


class ParseTree:
    EMPTY = cont.EMPTY

    def __init__(self, root=None, set_non_terminal=None):# self คือ syntax ของ python = None คือถ้าเค้าไม่ใส่มาให้ระบุเป็น None
        self.root = tNode.Node(root, parent=None)  # root node has no parent tNode.classNode(constructor)
        self.stack = ['$', self.root]  # take $ because we copy algorithm from ParserPL
        #self.focus = None
        self.SET_NONTERMINAL = set_non_terminal
        self.tree_level = 0

    def derive(self, head, tail):#tail รับมาเปน list
        self.focus = self.stack.pop()

        # check for sure that derive is not wrong
        if head != self.focus.data:
            print(scolor.StringColor('ERROR: buliding parse tree is error about head != current focus', color='Red'))
            exit(1)

        self.focus.child = self.gen_node_list(self.focus, tail)#tail ไปสร้างเป็น node ลูกกับสร้างเส้น = คือสร้างเส้น gennodelist สร้าง node ลูก
        for k in range(1, len(self.focus.child) + 1):#กลับด้าน add ลูกลง stack
            self.stack.append(self.focus.child[-k])

    def gen_node_list(self, cur_focus, list_child):
        '''
        This function will convert the list of String to list of Node
        each Node is come from the symbol in list_child and each Node will have head be parent
        :param list_child:
        :return:
        '''
        list_node = []

        # loop for generate list of node which each node can get data, parent
        for symbol in list_child:#แม่ชี้ลูกและลูกชี้แม่
            list_node.append(tNode.Node(symbol, parent=cur_focus))
        return list_node

    def change_focus(self):#pop stack
        self.stack.pop()

    def isTerminal(self, item):
        return item not in self.SET_NONTERMINAL

    def getHight(self, node):
        if self.isTerminal(node.data):
            return -1
        else:
            tmp_h = []
            for n in node.child:
                tmp_h.append(self.getHight(n))
            return 1 + max(tmp_h)

    def showTree(self):

        def printLine(node, level, list2write):
            if level == 0:
                print('{:8s}'.format(node.data))
            else:
                for i in range(level - 1):
                    if list2write[i] == 1:
                        print('{}{:5s}'.format(GO_D, ''), end='')
                    else:
                        print('{}{:5s}'.format(' ', ''), end='')

                # check that this node is last child
                if self.isTerminal(node.data):
                    str_tmn = scolor.StringColor(node.data, 'Magenta')
                    if node.parent.child[-1] == node:
                        print('{} {:8s}'.format(GO_R2, str_tmn))
                    else:
                        print('{} {:8s}'.format(GO_R, str_tmn))
                else:
                    if node.parent.child[-1] == node:
                        print('{} {:8s}'.format(GO_R2, node.data))
                    else:
                        print('{} {:8s}'.format(GO_R, node.data))

        def recursive_showTree(root, list2write, level=0):
            if self.isTerminal(root.data):
                printLine(root, level, list2write)
            else:
                printLine(root, level, list2write)

                if root.parent != None and root == root.parent.child[-1]:
                    list2write[level - 1] = 0

                if len(root.child) > 1:
                    # if list2write[i] = 1 -> must write '|'
                    list2write[level] = 1

                for node in root.child:
                    recursive_showTree(node, list2write, level=level + 1)

        GO_R = '┣━━━━'
        GO_R2 = '┗━━━━'
        GO_D = '┃'

        list2write = [0] * self.getHight(self.root)
        recursive_showTree(self.root, list2write, 0)
        print()

    def showDerivation(self):
        L = []
        R = [self.root]

        while len(R) != 0:

            # beauty print
            for item in L:
                if item.data != self.EMPTY:
                    print('{} '.format(scolor.StringColor(item.data, color='Magenta')), end='')
            for item in R:
                if item.data != self.EMPTY:
                    print('{} '.format(item.data), end='')
            print()

            node = R[0]
            child = node.child

            if self.isTerminal(node.data):
                L.append(node)
                R = R[1:]
            else:
                R = child + R[1:]
        print()
