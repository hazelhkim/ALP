from util_ge.utils import *
import random

def generate_sentence(plausible_rule_list, rule_word_dict):
    potential_res = []
    for key in rule_word_dict.keys():
        if key in plausible_rule_list:
            for sent in rule_word_dict[key]:
                for s in sent.split(','):
                    #print(s)
                    potential_res.append(s)
    return potential_res

def generate_sst_sentence(plausible_rule_list, rule_word_dict):
    potential_res = []
    for key in rule_word_dict.keys():
        for sent in rule_word_dict[key]:
            for s in sent.split(','):
                #print(s)
                potential_res.append(s)
    return potential_res

def generate_random_sent(candidate_sents): 
    
    keys = list(candidate_sents.keys())
    data = []
    for i in range(10):
        a_key = keys[random.randint(0,len(candidate_sents.keys())-1)]
#     b_key = keys[random.randint(0,len(candidate_sents.keys())-1)]
#     c_key = keys[random.randint(0,len(candidate_sents.keys())-1)]
#     d_key = keys[random.randint(0,len(candidate_sents.keys())-1)]
        if len(candidate_sents[a_key]) > 1:
            a_phrase = random.randint(0, len(candidate_sents[a_key])-1)
        else: 
            a_phrase = 0
        data.append(candidate_sents[a_key][a_phrase])
    
    return ' '.join(data)

def generate_sent_agnews(candidate_sents):
    nope = random.randint(0,2)
    np = random.randint(0, len(candidate_sents['S'])-1)
    vp = random.randint(0, len(candidate_sents['VP'])-1)
    pp = random.randint(0, len(candidate_sents['PP'])-1)
    if nope == 0:
        data = candidate_sents['PP'][pp] + ' ' + candidate_sents['VP'][vp]
        if len(data.split()) < 8:
            data = candidate_sents['PP'][pp] + ' ' + candidate_sents['VP'][vp] + ' ' + candidate_sents['PP'][pp]
    elif nope == 1:
        data = candidate_sents['S'][np] + ' ' + candidate_sents['PP'][pp]
        if len(data.split()) < 8:
            data = str(candidate_sents['S'][np]) + ' ' + candidate_sents['VP'][vp] + ' ' + candidate_sents['PP'][pp]
    else:
        data = candidate_sents['S'][np]  + ' ' + candidate_sents['VP'][vp]
        if len(data.split()) < 8:
            data = candidate_sents['S'][np] + ' ' + candidate_sents['VP'][vp] + ' ' + candidate_sents['PP'][pp]
    return data

def generate_sent_yahoo(candidate_sents):
    nope = random.randint(0,2)
    np = random.randint(0, len(candidate_sents['S'])-1)
    vp = random.randint(0, len(candidate_sents['VP'])-1)
    pp = random.randint(0, len(candidate_sents['PP'])-1)
    if nope == 0:
        data = candidate_sents['PP'][pp] + ' ' + candidate_sents['VP'][vp]
        if len(data.split()) < 8:
            data = candidate_sents['S'][pp] + ' ' + candidate_sents['VP'][vp] + ' ' + candidate_sents['PP'][pp]
    elif nope == 1:
        data = candidate_sents['S'][np] + ' ' + candidate_sents['PP'][pp]
        if len(data.split()) < 8:
            data = candidate_sents['S'][pp] + ' ' + candidate_sents['VP'][vp] + ' ' + candidate_sents['PP'][pp]
    else:
        data = candidate_sents['S'][np]  + ' ' + candidate_sents['VP'][vp]
        if len(data.split()) < 8:
            data = candidate_sents['S'][pp] + ' ' + candidate_sents['VP'][vp] + ' ' + candidate_sents['PP'][pp]
    return data


def generate_sent(candidate_sents):
    nope = random.randint(0,2)
    np = random.randint(0, len(candidate_sents['NP'])-1)
    vp = random.randint(0, len(candidate_sents['VP'])-1)
    pp = random.randint(0, len(candidate_sents['PP'])-1)
    if nope == 0:
        data = candidate_sents['PP'][pp] + ' ' + candidate_sents['VP'][vp]
        if len(data.split()) < 8:
            data = candidate_sents['NP'][pp] + ' ' + candidate_sents['VP'][vp] + ' ' + candidate_sents['PP'][pp]
    elif nope == 1:
        data = candidate_sents['NP'][np] + ' ' + candidate_sents['PP'][pp]
        if len(data.split()) < 8:
            data = candidate_sents['NP'][pp] + ' ' + candidate_sents['VP'][vp] + ' ' + candidate_sents['PP'][pp]
    else:
        data = candidate_sents['NP'][np]  + ' ' + candidate_sents['VP'][vp]
        if len(data.split()) < 8:
            data = candidate_sents['NP'][pp] + ' ' + candidate_sents['VP'][vp] + ' ' + candidate_sents['PP'][pp]
    return data


def generate_sent_sst(candidate_sents):
    candidate_sents = extract_final_ruleset(candidate_sents)

    keys = list(candidate_sents.keys())
    min_length = 10
    for key in keys:
        temp_min_length = min(len(candidate_sents[key]))
        if min_length > temp_min_length:
            min_length = temp_min_length
    sent = ''
    while len(sent.split()) < 10 or len(sent.split()) < min_length:
        phrase = keys[random.randint(0,len(keys))]
        elem = 0
        print(len(candidate_sents[phrase]))
        if len(candidate_sents[phrase]) == 0:
            #print(phrase)
            #print('!!!')
            continue
        if len(candidate_sents[phrase]) > 1:
               elem = random.randint(0, len(candidate_sents[phrase])-1)
        sent += candidate_sents[phrase][elem]
    return sent


def get_pos_word_list(CNF_word_pool):
    POS_list = get_POS_list(CNF_word_pool)
    
    pos_word_list = {}
    for key in POS_list.keys():
        pos_word_list[key] = []
        for pos in POS_list[key]:
            for word in CNF_word_pool[pos]:
                pos_word_list[key].append(word)
    return pos_word_list



def get_POS_list(CNF_word_pool):
    POS_list = {}
    POS_list[wordnet.ADJ] = []
    POS_list[wordnet.VERB] = []
    POS_list[wordnet.NOUN] = []
    POS_list[wordnet.ADV] = []

    for key in CNF_word_pool.keys():
        if get_wordnet_pos(key) != '':
            POS_list[get_wordnet_pos(key)].append(key) 

    return POS_list

def CNF_word_pool_wo_prob(CNFword_list):
    candidate_word_pool_wo_prob = {}
    for key in CNFword_list.keys():
        words = []
        for word_prob in CNFword_list[key]:
            word = word_prob[0]
            #prob = word_prob[0]
            words.append(word)
        candidate_word_pool_wo_prob[key] = words
    return candidate_word_pool_wo_prob

# def word_dict_pool(candidate_rule_pool, CNFword_list):
#     rule_word_dict = {}
#     for rule_pool in candidate_rule_pool:
#         #print(rule_pool)
#         rule_word_dict[rule_pool] = []
#         for rule in candidate_rule_pool[rule_pool]:
#             candidate_phrase = []
#             for r in rule.split():
#                 #print(CNFword_list[r])

#                 word = select_random_from_cnf(CNFword_list[r])

#                 candidate_phrase.append(word)

#             candidate_phrase = ' '.join(candidate_phrase)
#             rule_word_dict[rule_pool].append(candidate_phrase)
#     return rule_word_dict


def word_dict_pool(candidate_rule_pool, CNF_word_pool):
    rule_word_dict = {}
    for rule_pool in candidate_rule_pool:
        rule_word_dict[rule_pool] = []
        for rule in candidate_rule_pool[rule_pool]:
            candidate_phrase = []
            for r in rule.split():
                if r in CNF_word_pool.keys():
                    if len(CNF_word_pool[r]) != 0:
                        word = select_random_from_cnf(CNF_word_pool[r])
                        candidate_phrase.append(word)
            rule_word_dict[rule_pool].append(' '.join(candidate_phrase))
        rule_word_dict[rule_pool] = list(set(rule_word_dict[rule_pool]))
    return rule_word_dict

def word_dict_pool_big(candidate_rule_pool, CNF_word_pool):
    rule_word_dict = {}
    for rule_pool in candidate_rule_pool:
        #print(rule_pool)
        rule_word_dict[rule_pool] = []
        for rule in candidate_rule_pool[rule_pool]:
            #candidate_phrase = []
            for r in rule.split():
                if r not in CNF_word_pool.keys():
                    continue
                #print(CNFword_list[r])
                else:
                    for word in CNF_word_pool[r]:
                        candidate_phrase = select_random_from_cnf(word)

            #print(candidate_phrase)
            #candidate_phrase = ' '.join(candidate_phrase)
            for phrase in candidate_phrase:
                rule_word_dict[rule_pool].append(phrase)
    return rule_word_dict


def select_random_from_cnf(rule_list):
    idx = random.randint(0, len(rule_list)-1)
    return rule_list[idx]


def select_candidate(candidate_pool: dict, key: str):
    candidates = candidate_pool[start]
    idx = random.randint(0, len(candidates))
    return candidates[idx]

def select_word(candidate_word_pool: dict, start:str):
    candidate_words = candidate_word_pool[start]
    idx = random.randint(0, len(candidate_words))
    return candidate_words[idx]
    
def select_rule_both(rule_dict, start:str):
    candidate_rules = select_rules_w_prob(rule_dict, start)
    selected_rule = select_random(candidate_rules)
    return selected_rule

def select_random(rule_list):
    idx = random.randint(0, len(rule_list))
    return rule_list[idx][0]

def select_most_prob(rule_list):
    import numpy as np
    max_prob = 0
    max_idx = np.inf
    for idx, rule in enumerate(rule_list):
        prob = rule[1]
        if max_prob < float(prob):
            max_prob = float(prob)
            max_idx = idx
    return rule_list[max_idx][0]


def select_rules_w_prob(rule_dict, start:str):
    #path = 'ouptut/{}.'.format(dataset)
    #rule_dict = CNFrule_dict(data)
    tot_val = 0.0
    for rule in rule_dict[start]:
        tot_val += float(rule[1])
    avg = tot_val/len(rule_dict[start])
    rule_list = []
    for rule in rule_dict[start]:
        if float(rule[1]) > avg:
            rule_list.append(rule[0])

    return rule_list
    
# class Chromosome():
#     def __init__(self, data, generation):
#         self.rule_dict = CNFrule_dict(data)
#         self.next_Generation = 

#     def chromomse_memory():

   

