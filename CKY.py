import sys
import math
from collections import defaultdict
from nltk.tree import Tree


class Pointer:
    def __init__(self, label, prob, lbp, rbp, word):
        self.label = label
        self.prob = prob
        self.lbp = lbp
        self.rbp = rbp
        self.word = word

    def __str__(self):
        # + " lbp: " + str(self.lbp) + " rbp: " + str(self.rbp)
        return self.label + " " + str(self.prob)

    # def __get_left__(lbp):
    #     return lbp[0]
    __repr__ = __str__


# grammar file
file1 = sys.argv[1]
# sentences to be parsed
file2 = sys.argv[2]


def readGrammarFile(fn):

    f = open(fn, "r")
    rules = defaultdict(lambda: [])

    for line in f:
        line = line.split('#')[0].strip()  # strip out comments and whitespace
        if line == '':
            continue
        fields = line.split()
        # takes the counts in the grammar into account
        neg_log_prob = float(fields[0])
        lhs = fields[1]
        rhs = fields[2:]            # a list of RHS symbols
        # adds a list of the list of RHS symbols
        rules[lhs].extend([rhs, neg_log_prob])

    return rules


def readSentFile(fn):
    f = open(fn, "r")
    # list of sentences, each element contains a list of tokens (terminal contituents)
    sentences = []

    for line in f:
        sentences.append(line.split())

    return sentences


grammar = readGrammarFile(file1)
sentences = readSentFile(file2)
# print(grammar)
# print(sentences)

# print(grammar["Vsuff"])
# search_age = "Grandma"
# for name in grammar.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
#     if name.contains(search_age):
#         print(name)

# returns a list of all the possible POS of constintuent


def find_key(input_dict, value):
    lister = []
    for k, v in input_dict.items():
        for i in range(len(v)):
            if v[i] == value:
                lister.append(k)
                lister.append(v[i+1])
    return lister


# print(find_key(grammar, ["Grandma"]))


def PCKY(sentences):
    # will change later to encompass all the sentences, or maybe a certain few, leave at the first one for testing
    sent = sentences
    print(sent, len(sent))
    CKY_list = []
    liste = []
    lister = []

    for i in range(len(sent)):
        CKY_list.append(liste)
        liste = liste[:]
        for j in range(len(sent)+1):
            CKY_list[i].append(lister)
            lister = lister[:]

    for j in range(1, len(sent)+1):
        found_key = find_key(grammar, [sent[j-1]])
        temp = []
        for i in range(0, len(found_key), 2):
            temp.append([Pointer(found_key[i],
                                 found_key[i+1], "", "", sent[j-1])])
        # print(temp, "yooo")
        CKY_list[j-1][j] = temp
        if(j == 1):
            continue
        for i in range(j-1, -1, -1):  # the pointer for the next diagonal POS/word
            for m in range(i+1, j):
                temp_list = []
                # holds each combination of list, used for multiple phrase structures in one element
                phrase_struct = Pointer
                for k in range(0, len(CKY_list[i][m])):
                    for l in range(0, len(CKY_list[m][j])):
                        # left Phrase Structure (left back pointer)
                        lbp = CKY_list[i][m][k][0]
                        # print(lbp, "lbp")
                        # right Phrase Structure (right back pointer)
                        rbp = CKY_list[m][j][l][0]
                        # print(rbp, "rbp")
                        # adds the prob of backpointers, does not add the actual prob until find_key is called below
                        probabil = lbp.prob + rbp.prob
                        phrase_struct = Pointer(
                            "None", probabil, lbp, rbp, "")
                        temp_list.append([phrase_struct])

                # print(temp_list, "temp list")
                for tags in temp_list:
                    tag_list = []
                    tagger = [tags[0].lbp.label, tags[0].rbp.label]
                    # print(tagger, "tagger")
                    if(find_key(grammar, tagger)):
                        tags[0].label = find_key(grammar, tagger)[0]
                        tags[0].prob += find_key(grammar, tagger)[1]
                        tag_list.append(tags)
                        CKY_list[i][j].append(tags)
                # print(CKY_list[i-1][j], "CKY list")

    return CKY_list


def recur_table(partOS):
    if partOS.lbp == "" and partOS.rbp == "":
        return" ( " + partOS.label + " " + partOS.word + ")"
    else:
        return "(" + partOS.label + " " + recur_table(partOS.lbp) + recur_table(partOS.rbp) + ")"


# example format
# ( ROOT is it true that (S (NP (Det a )(Noun pickle ))(VP (Verb pickled )(NP (Det every )(Noun sandwich ))))?  )


for sent in sentences:
    # print(PCKY(sent), "\n")
    table = PCKY(sent)
    # print(table, "\n")
    parse = []  # add parse to the list, print out in the end
    for i in table[0][-1]:
        parse = ""
        if i != [] and i[0].label == "ROOT":
            # print(j[0][0].label, j[0][0].lbp, j[0][0].rbp)
            t = Tree.fromstring(recur_table(i[0]))
            t.draw()
            print(recur_table(i[0]))
            print(i[0].prob, "\n")
    break


# print(grammar)

# print(PCKY(sentences))
