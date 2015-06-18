#coding:utf-8

import conf
import MeCab as mc
#For more infomation about MeCab: http://taku910.github.io/mecab/

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


WORD_TYPES_TO_RETAIN = conf.word_types_to_retain
HASH_SIZE = conf.hash_size

HASH_SIZE = 64

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


if __name__ == "__main__":
    test_set = ["居酒屋で学生ら男女33人が食中毒",
    "歌舞伎町ぼったくり店 11人逮捕",
    "処方薬を無許可販売 130年分入手",
    "串カツ屋 橋下氏判断で強制撤去",
    "雅子さまを楽にした佳子さま人気",
    "妻が夫の車にひかれ死亡 横浜",
    "元少年Aは妻子持ち? 怪情報拡散",
    "とくダネで虚偽報道 BPO申し立て",
    "「元少年A」手記を擁護する人達",
    "高村副総裁の二枚舌に集中砲火",
    "衆院で混乱 携帯盗難で告発へ写真",
    "文科相が国歌要請 大学は困惑映像",
    "橋下氏の国政進出 首相エール写真",
    "多選自粛 相次ぐ心変わり写真",
    "避難先で差別 東電に賠償請求",
    "マタハラ CAがJALを提訴写真",
    "元少年手記 週間売り上げ1位写真",
    "元社会党書記長 馬場さん死去写真",
    "モルシ氏ら６被告に死刑判決「国の治安乱した」",
    "日航ＣＡ、「マタハラ」提訴…休職命じられ無給",
    "5月米住宅着工件数は11.1％減、許可件数8年ぶり高水準",
    "ぜんそく悪用、処方薬を大量転売の疑い 逮捕の男は否認",
    "ＳＴＡＰなど不正１２件「信頼揺らぐ」と危機感",
    "中東でＭＥＲＳ感染、ドイツ人死亡　欧州では今年初",
    "韓国ＭＥＲＳ、死者１４人に　ＷＨＯは警戒呼びかけ",
    "韓国ＭＥＲＳ感染拡大、隔離者も急増　日本でも警戒強化",
    "鳥取）ＭＥＲＳで新型インフルに準じ対応",
    "小規模噴火確認、浅間山　メカニズム解明目指す",
    "蔵王山で噴火警報解除　「噴火の可能性低下」"]

    test_result = []

    for each in test_set:
        test_result.append((each, cal_simhash(each)))

    for i in xrange(len(test_result)):
        print(test_result[i][0])
        to_set = ["", 2**64]
        for j in xrange(len(test_result)):
            if j != i:
                if cal_hamming_distance(test_result[i][1], test_result[j][1]) < to_set[1]: # <=也许更好
                    to_set[0] = test_result[j][0]
                    to_set[1] = cal_hamming_distance(test_result[i][1], test_result[j][1])
        print("-->"),
        print(to_set[0]),
        print("  "),
        print(to_set[1])

    print(MeCabResult("韓国ＭＥＲＳ、死者１４人に　ＷＨＯは警戒呼びかけ"))
    print(MeCabResult("中東でＭＥＲＳ感染、ドイツ人死亡　欧州では今年初"))
    print(MeCabResult("韓国ＭＥＲＳ感染拡大、隔離者も急増　日本でも警戒強化"))
    print(MeCabResult("鳥取）ＭＥＲＳで新型インフルに準じ対応"))
    print(MeCabResult("蔵王山で噴火警報解除　「噴火の可能性低下」"))
    print(MeCabResult("小規模噴火確認、浅間山　メカニズム解明目指す"))


    a = """気象庁は１６日午前、浅間山（群馬、長野県）が噴火したもようだと発表した。ごく小規模とみられ、火口から北側約４キロの鬼押出しで、微量の降灰を確認した。最後に噴火したのは２００９年５月２７日。気象庁は「これ以上、活発化する兆候はみられない」として、噴火警戒レベルは現状の２（火口周辺規制）を維持。火口から約２キロで大きな噴石への警戒を求めている。１１年の東日本大震災以降、国内の火山は御嶽山や口永良部島や箱根山などで噴火が相次ぎ、活動が活発化している。気象庁によると、１６日午前９時半ごろ、観光施設職員が降灰に気づいた。雲がかかり視界不良で噴煙の状況は不明。"""

    b = """仙台管区気象台は１６日、宮城県と山形県にまたがる蔵王山に４月に出した噴火警報（火口周辺危険）を解除した。火山性地震が減少するなどしており、６月１５日の火山噴火予知連絡会の見解も踏まえ「噴火が発生する可能性が低くなった」と判断した。引き続き、活火山であることに留意するよう求めている。気象台によると、蔵王山では４月、火口湖の「御釜」付近が震源とみられる火山性地震が増加し、４月１３日に噴火警報を発表した。気象台は、想定火口域から１・２キロの範囲で大きな噴石に警戒するよう呼び掛けていた。周辺温泉街で観光客が大幅に減り、地元から早期解除を求める声が出ていた。"""

    c = """結果だけでなく生きざまを見せるのがプロレスだと、日本を代表するプロレスラー三沢光晴さん（４６）が、かつて自著で語っていた。実際、戦績以上にその生きざまにファンは共感してきた。１９年前、選手の大量離脱で危機に瀕した全日本プロレスを救ったのは、彼のひたむきさだった。体格もパワーも違うジャンボ鶴田選手という巨大な壁に食らいつき、乗り越える姿に、ファンは勇気をもらった。受け身の名人と呼ばれるまでに練習を積み、どんな危険な技でも耐えてみせた。少々の骨折などものともせず年間１００試合以上に出場し、常に全力を尽くした。それが彼の考える「強さ」であり、プロレスラーとしての「誇り」だったのだろう。そんな彼にファンはしびれた。リングの外で見せた男気にほれ直したこともある。…（２００９年６月１６日付「一日一言」）"""

    print(cal_hamming_distance(cal_simhash(a), cal_simhash(b)))
    print(cal_hamming_distance(cal_simhash(a), cal_simhash(c)))