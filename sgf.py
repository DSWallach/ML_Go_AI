# map from numerical coordinates to letters used by SGF
SGF_POS = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Collection:
    def __init__(self, parser=None):
        self.parser = parser
        if parser:
            self.setup()
        self.children = []

    def setup(self):
        self.parser.start_gametree = self.my_start_gametree

    def my_start_gametree(self):
        self.children.append(GameTree(self, self.parser))

    def __len__(self):
        return len(self.children)

    def __getitem__(self, k):
        return self.children[k]

    def __iter__(self):
        return iter(self.children)

    def output(self, f):
        for child in self.children:
            child.output(f)


class GameTree(object):
    def __init__(self, parent, parser=None):
        self.parent = parent
        self.parser = parser
        if parser:
            self.setup()
        self.nodes = []
        self.children = []

    def setup(self):
        self.parser.start_gametree = self.my_start_gametree
        self.parser.end_gametree = self.my_end_gametree
        self.parser.start_node = self.my_start_node

    def my_start_node(self):
        if len(self.nodes) > 0:
            previous = self.nodes[-1]
        elif self.parent.__class__ == GameTree:
            previous = self.parent.nodes[-1]
        else:
            previous = None
        node = Node(self, previous, self.parser)
        if len(self.nodes) == 0:
            node.first = True
            if self.parent.__class__ == GameTree:
                if len(previous.variations) > 0:
                    previous.variations[-1].next_variation = node
                    node.previous_variation = previous.variations[-1]
                previous.variations.append(node)
            else:
                if len(self.parent.children) > 1:
                    node.previous_variation = self.parent.children[-2].nodes[0]
                    self.parent.children[-2].nodes[0].next_variation = node

        self.nodes.append(node)

    def my_start_gametree(self):
        self.children.append(GameTree(self, self.parser))

    def my_end_gametree(self):
        self.parent.setup()

    def __iter__(self):
        return NodeIterator(self.nodes[0])

    @property
    def root(self):
        # @@@ technically for this to be root, self.parent must be a Collection
        return self.nodes[0]

    @property
    def rest(self):
        class _:
            def __iter__(_):
                return NodeIterator(self.nodes[0].next)
        if self.nodes[0].next:
            return _()
        else:
            return None

    def output(self, f):
        f.write("(")
        for node in self.nodes:
            node.output(f)
        for child in self.children:
            child.output(f)
        f.write(")")


class Node:
    def __init__(self, parent, previous, parser=None):
        self.parent = parent
        self.previous = previous
        self.parser = parser
        if parser:
            self.setup()
        self.properties = {}
        self.next = None
        self.previous_variation = None
        self.next_variation = None
        self.first = False
        self.variations = []
        if previous and not previous.next:
            previous.next = self

    def setup(self):
        self.parser.start_property = self.my_start_property
        self.parser.add_prop_value = self.my_add_prop_value
        self.parser.end_property = self.my_end_property
        self.parser.end_node = self.my_end_node

    def my_start_property(self, identifier):
        # @@@ check for duplicates
        self.current_property = identifier
        self.current_prop_value = []

    def my_add_prop_value(self, value):
        self.current_prop_value.append(value)

    def my_end_property(self):
        self.properties[self.current_property] = self.current_prop_value

    def my_end_node(self):
        self.parent.setup()

    def output(self, f):
        f.write(";")
        for key, values in sorted(self.properties.items()):
            f.write(key)
            for value in values:
                if "\\" in value:
                    value = "\\\\".join(value.split("\\"))
                if "]" in value:
                    value = "\\]".join(value.split("]"))
                f.write("[%s]" % value)


class NodeIterator:

    def __init__(self, start_node):
        self.node = start_node

    def __next__(self):
        if self.node:
            node = self.node
            self.node = node.next
            return node
        else:
            raise StopIteration()

    next = __next__  # Python 2


class ParseException(Exception):
    def __init__(self, ch, state, lineNum):
        self.state = state
        self.ch = ch
        asc = ord(self.ch)
        print("Exception: Char "+self.ch+" ord("+str(asc)+") in state "+str(self.state)+" on line "+str(lineNum)+"\n")
    #pass


class Parser:
    def parse(self, sgf_string):

        self.curLine = 0

        def whitespace(ch):
            if ch == "\r" or ch == "\n":
                self.curLine += 1

            return ch in " \t\r\n" or ord(ch) == 10

        def ucletter(ch):
            return ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        state = 0
        prevState = 0
        nestingLevel = 0

        for i in range(len(sgf_string)):
            ch = sgf_string[i]
            if state == 0:
                if whitespace(ch):
                    state = 0
                elif ch == '(':
                    if sgf_string[i+1] == ";":
                        self.start_gametree()
                        state = 1
                    else:
                        state = 0
                else:
                    state = 0  # ignore everything up to first (
                    # raise ParseException(ch, state)
            elif state == 1:
                if whitespace(ch):
                    state = 1
                elif ch == ";":
                    self.start_node()
                    state = 2
                elif ch == "C":
                    prevState = state
                    state = 8
                else:
                    raise ParseException(ch, state, self.curLine)
            elif state == 2:
                if whitespace(ch):
                    state = 2
                elif ch == "C":
                    prevState = state
                    state = 8
                elif ucletter(ch):
                    prop_ident = ch
                    state = 3
                elif ch == ";":
                    self.end_node()
                    self.start_node()
                    state = 2
                elif ch == "(":
                    self.end_node()
                    self.start_gametree()
                    state = 1
                elif ch == ")":
                    self.end_node()
                    self.end_gametree()
                    state = 4
                else:
                    raise ParseException(ch, state, self.curLine)
            elif state == 3:
                if ucletter(ch):
                    prop_ident = prop_ident + ch
                    state = 3
                elif ch == "[":
                    self.start_property(prop_ident)
                    prop_value = ""
                    state = 5
                elif whitespace(ch):
                    pass
                else:
                    raise ParseException(ch, state, self.curLine)
            elif state == 4:
                if ch == ")":
                    self.end_gametree()
                    state = 4
                elif whitespace(ch):
                    state = 4
                elif ch == "(":
                    self.start_gametree()
                    state = 1
                elif ch == "-" and sgf_string[i+1] == "-":
                    #End 
                    break 
                else:
                    raise ParseException(ch, state, self.curLine)
            elif state == 5:
                #print("state 5 ch "+ch+" line "+str(self.curLine))
                if ch == "\\":
                    self.curLine += 1
                    state = 6
                # Handle backspace
                #elif ord(ch) == 10:
                #    pass
                elif ch == "]":
                    self.add_prop_value(prop_value)
                    state = 7
                else:
                    prop_value = prop_value + ch
            elif state == 6:
                prop_value = prop_value + ch
                state = 5
            elif state == 7:
                if whitespace(ch):
                    state = 7
                elif ch == "[":
                    prop_value = ""
                    state = 5
                elif ch == ";":
                    self.end_property()
                    self.end_node()
                    self.start_node()
                    state = 2
                elif ucletter(ch):
                    self.end_property()
                    prop_ident = ch
                    state = 3
                elif ch == ")":
                    self.end_property()
                    self.end_node()
                    self.end_gametree()
                    state = 4
                elif ch == "(":
                    self.end_property()
                    self.end_node()
                    self.start_gametree()
                    state = 1
                else:
                    raise ParseException(ch, state, self.curLine)
            # Ignore everything in comments
            elif state == 8:
                # Until the end of the comment 
                if ch == "]":
                    if nestingLevel == 0:
                        # Go back to previous state
                        state = prevState
                    else:
                        nestingLevel -= 1
                elif ch == "[":
                    nestingLevel += 1
                elif whitespace(ch):
                    continue
                    #pass
                else:
                    #print(ch)
                    continue
                    #pass
                # Otherwise do nothing
            else:
                # only a programming error could get here
                raise Exception(state)  # pragma: no cover

        if state != 4:
            #print ("State not 4 on line "+str(self.curLine))
            raise ParseException(ch, state, self.curLine)


def parse(sgf_string):
    parser = Parser()
    collection = Collection(parser)
    parser.parse(sgf_string)
    return collection
