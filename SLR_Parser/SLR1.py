NON_TERMINAL_SET = set()

# read a grammar from file to list
GRAMMAR = []
with open('SLR_Parser/Grammar.txt', 'r') as grammar_file:
    for line in grammar_file:
        # if line start with '#'. it means this line just is a comment. we need to ignore
        if line.startswith('#'):
            continue

        line = line.strip().split(' -> ')
        head = line[0].strip()
        tail = line[1].split()
        GRAMMAR.append((head, tail))
        NON_TERMINAL_SET = NON_TERMINAL_SET.union(set([head]))

# read follow from file to dict
# the follow is already calculate by http://hackingoff.com/compilers/predict-first-follow-set
FOLLOW = {}
with open('SLR_Parser/Follow.txt') as follow_file:
    for line in follow_file:
        if line.startswith('#'):
            continue

        line = line.split('\t')
        non_terminal = line[0].strip()
        follow = line[1].split()
        FOLLOW[non_terminal] = follow


def add_point(rule, idx):
    '''
    เติมจุดลง tail ของกฎ
    :param rule: กฏที่อยู้ในรูป ('A', ['B', 'C', 'D'])
    :param idx: ตำแหน่งที่ต้องการใส่จุด
    :return: กฎที่มีการเติมจุดลงใน tail แล้ว
    '''
    head, tail, point = rule[0], list(rule[1]), idx
    return (head, tail, point)


def get_closer(rule):
    # rule = ('relExp', ['arithExp', 'relOp', 'arithExp'], idx_point)
    queue = [rule]
    closer = []
    while len(queue) != 0:
        rule = queue.pop(0)
        closer.append(rule)
        # rule = (head -> tail)
        head, tail, idx_point = rule

        if len(tail) != idx_point:
            next_head = tail[idx_point]
            # loop for find all rule which head start with ''
            for each_rule in GRAMMAR:
                if next_head == each_rule[0]:
                    each_rule = add_point(each_rule, 0)

                    # append tmp_rule into queue
                    if each_rule not in closer and each_rule not in queue:
                        queue.append(each_rule)
    return closer


def is_completed_item(item):
    return len(item[1]) == item[2]


def is_repeated_stage(list_stages, tmp_stage):
    for i, stage in enumerate(list_stages):
        # check that 2 stage are repeat or not

        # first, we check size of items_set
        if len(tmp_stage['items']) != len(stage['items']):
            continue

        # now, we confident that 2 items_set size are same
        # let's check that 2 items_set are same
        # loop each item in tmp_stage
        for item1 in tmp_stage['items']:
            visit = False

            # loop each item in stage
            for item2 in stage['items']:
                if item1 == item2:
                    visit = True
                    break

            # from looping on recently items_set, if not visit any same item, it means this 2 stage is not repeated
            if not visit:
                repeated = False
                break
            else:
                repeated = True

        # check that
        if repeated:
            return stage['stage_number']
    return -1


def is_accept_stage(stage):
    rule = stage['items'][0]
    return START_RULE[0] == rule[0] and START_RULE[1] == rule[1] and len(START_RULE[1]) == rule[2]


# # --------------------- Create a graph of stages ------------------------------------------
# create start stage
START_RULE = GRAMMAR[0]

# define start_rule and start_stage
# rule format: (head, tail, point_idx)
START_RULE = add_point(START_RULE, 0)
items = get_closer(START_RULE)
start_stage = {
    'items': items,
    'stage_number': 0
}

# variable to count the number if existed stage
cnt_number_stage = 0
# define queue
queue = []

# add first stage into queue
queue.append(start_stage)
cnt_number_stage += 1

# STAGES is a list of all stage
STAGES = []

# loop for create stage's detail
while len(queue) != 0:
    cur_stage = queue.pop(0)
    STAGES.append(cur_stage)

    # list_key_items is list of tuple (token, stages) ***
    list_key_items = []
    for item in cur_stage['items']:
        if not is_completed_item(item):
            # get a idx of splitter point
            point_idx = item[2]

            # get next token (next of '.')
            next_token = item[1][point_idx]

            # create a new item which slide '.' already
            next_items = add_point(rule=item, idx=point_idx + 1)
            next_items = get_closer(next_items)

            # merge all items with same key (next_token) together
            exist_key = False
            for (key, key_items) in list_key_items:
                if key == next_token:
                    exist_key = True
                    # add new item into key_items
                    for it1 in next_items:
                        if it1 in key_items:
                            break
                        else:
                            key_items.append(it1)
                if exist_key:
                    break

            if not exist_key:
                list_key_items.append((next_token, next_items))

    for (next_token, next_items) in list_key_items:
        # create a temp stage
        tmp_stage = {
            'items': next_items,
        }

        # find that this tmp_stage is exist or not (find on both queue and STAGES_list)
        number_stage = is_repeated_stage(queue, tmp_stage)
        if number_stage < 0:
            number_stage = is_repeated_stage(STAGES, tmp_stage)

        # if number_stage is < 0, it mean this stage is not existing
        if number_stage < 0:
            # if number_stage still < 0, it mean this stage is not existing
            # so we add new number equal cnt_number_stage to number_stage
            number_stage = cnt_number_stage
            tmp_stage['stage_number'] = number_stage
            queue.append(tmp_stage)
            cnt_number_stage += 1

        # when we set the number if this tmp_stage already,
        # next we will set pointer of the current_stage
        cur_stage['__GET__', next_token] = number_stage

# # ------------------------ Construct a SLR table ---------------------------------------
SLR_TABLE = {}
for cur_stage in STAGES:
    # get a number of current stage
    stage_number = cur_stage['stage_number']

    if is_accept_stage(cur_stage):
        # add Acc-Value
        SLR_TABLE[stage_number, '$'] = ('Accept', None)
    else:
        # add Shift-Value
        for key in cur_stage.keys():
            if type(key) == tuple:
                # get a token for move to next stage. get at index 1 because index 0 is '__GET__'
                token = key[1]
                # get a number of next stage
                next_stage_number = cur_stage[key]

                if token in NON_TERMINAL_SET:
                    # add Shift-Value
                    SLR_TABLE[stage_number, token] = (None, next_stage_number)
                else:
                    # add Normal-Value
                    SLR_TABLE[stage_number, token] = ('Shift', next_stage_number)

        # add Reduce-Value
        for item in cur_stage['items']:
            if is_completed_item(item):
                head = item[0]
                for non_terminal in FOLLOW[head]:
                    tail = item[1]
                    rule = (head, tail)
                    SLR_TABLE[stage_number, non_terminal] = ('Reduce', rule)


# # ------------------------ Parse tree ---------------------------------------
def print_derive_img(derive_img):
    for line in derive_img:
        stack, input, action = line
        print(stack, '\t', input, '\t', action)

def print_line_derive(stack, input, action):
    print(stack, '\t', input, '\t', action)

def slr_parse_tree(steam_of_tokens):
    derive_img = []
    STEAM_OF_TOKEN = steam_of_tokens
    STEAM_OF_TOKEN.append('$')
    # STEAM_OF_TOKEN = 'id = id * id + n $'.split()

    # i is use to seek a index of current input token
    i = 0

    # define a stack
    STACK = []

    # append start token and start stage into STACK
    STACK.append('$')
    STACK.append(0)

    while True:
        token = STEAM_OF_TOKEN[i]
        # current stage is a top of stack
        number_cur_stage = STACK[-1]

        action_tuple = SLR_TABLE[number_cur_stage, token]
        action = action_tuple[0]

        derive_img.append(tuple([list(STACK), STEAM_OF_TOKEN[i:], action]))
        # print_line_derive(STACK, STEAM_OF_TOKEN[i:], action)

        # action can be 4 case
        #   1) ('Shift', number_next_stage)
        #   2) ('Reduce', rule)
        #   3) (None, number_next_stage) << use after reduce
        #   4) ('Accept', None)
        if action == 'Shift':
            number_next_stage = action_tuple[1]
            STACK.append(token)
            i += 1
            STACK.append(number_next_stage)
        elif action == 'Reduce':
            rule = action_tuple[1]
            head, tail = rule
            for j in range(0, len(tail)):
                # pop stage
                STACK.pop()

                # pop token
                tmp_token = STACK.pop()
                if tmp_token != tail[-j - 1]:
                    print('Error: can not reduce, the token is not match')
            number_cur_stage = STACK[-1]
            _, number_next_stage = SLR_TABLE[number_cur_stage, head]
            STACK.append(head)
            STACK.append(number_next_stage)
        elif action == 'Accept':
            print('finish')
            break
        else:
            print('Error: out of action case')
            break
    return derive_img