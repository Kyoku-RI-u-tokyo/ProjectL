#coding:utf-8

from supporter import debug_tools
import conf
import MeCab as mc
#For more infomation about MeCab: http://taku910.github.io/mecab/

WORD_TYPES_TO_RETAIN = conf.word_types_to_retain
HASH_SIZE = conf.hash_size

def cal_hamming_weight(n):
    return bin(n).count("1")

def cal_hamming_distance(m, n):
    return cal_hamming_weight(m^n)

class Word():
    def __init__(self, word, weight, w_type, w_sub_type):
        self.word = word
        self.weight = weight
        self.w_type = w_type
        self.w_sub_type = w_sub_type

    def get_word(self):
        return self.word

    def get_weight(self):
        return self.weight

    def get_type(self):
        return self.w_type

    def get_sub_type(self):
        return self.w_sub_type

    def add_weight(self, to_add):
        self.weight += to_add

class MeCabResult():
    def __init__(self, sentence):
        self.words = {}
        for each_line in mc.Tagger("--node-format=%m\\t%H\\n").parse(sentence).split("\n"):
            a_line = each_line.split("\t")
            word = a_line[0]
            if len(a_line) >= 2:
                attributes = a_line[1].split(",")
                if attributes[0] in WORD_TYPES_TO_RETAIN:
                    weight_to_add = 1
                    if attributes[0]+attributes[1] in conf.weight_table:
                        weight_to_add = conf.weight_table[attributes[0]+attributes[1]]
                    if word in self.words:
                        self.words[word].add_weight(weight_to_add)
                    else:
                        self.words[word] = Word(word, weight_to_add, attributes[0], attributes[1])
                else:
                    pass
            else:
                pass #'eos' or '\n'

    def get_words(self):
        return self.words.keys()

    def get_weight(self, word):
        return self.words[word].get_weight()

    def __str__(self):
        result = ""
        for each_key in self.words.keys():
            a_word = self.words[each_key]
            result += "{word} \t weight:{weight}, type:{w_type}, sub_type:{w_sub_type}\n".format(word=a_word.get_word(),
                                                                                                 w_type=a_word.get_type(),
                                                                                                 w_sub_type=a_word.get_sub_type(),
                                                                                                 weight=a_word.get_weight())
        return result

def hasher(s):
    return hash(s)

def weighted_hash(word, weight=1, hash_func=hasher):
    bin_map_string = bin(abs(hash_func(word)))[2:][-HASH_SIZE:] #ex: '101101' <- String, NOT int.
    bin_map = [-1*weight for _ in xrange(HASH_SIZE)]
    diff = HASH_SIZE - len(bin_map_string)
    for i in xrange(diff, HASH_SIZE):
        to_write = int(bin_map_string[i-diff])
        if to_write == 0:
            to_write = -1
        bin_map[i] = weight*to_write
    return bin_map

def list_plus(left, right):
    assert(len(left) == len(right))
    for i in xrange(len(left)):
        left[i] += right[i]
    return left

def cal_simhash(s):
    sim_hash_value = [0 for _ in xrange(HASH_SIZE)]
    mecab_result = MeCabResult(s)
    words = mecab_result.get_words()
    for each_word in words:
        sim_hash_value = list_plus(sim_hash_value,
                                   weighted_hash(each_word, mecab_result.get_weight(each_word)))
    for i in xrange(HASH_SIZE):
        if sim_hash_value[i] > 0:
            sim_hash_value[i] = "1"
        else:
            sim_hash_value[i] = "0"
    return int("".join(sim_hash_value), 2)

