from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet

def evolutionary_augmented_CNF_word_pool(CNF_word_pool):
    augmented_synonym_in_pos_dict_0 = generate_candidate_list(CNF_word_pool)
    augmented_synonym_in_pos_dict_1 = generate_candidate_list(augmented_synonym_in_pos_dict_0)
    augmented_synonym_in_pos_dict_2 = generate_candidate_list(augmented_synonym_in_pos_dict_1)
#     augmented_synonym_in_pos_dict_3 = generate_candidate_list(augmented_synonym_in_pos_dict_2)
    total_word_pool = {}
    keys = []
    for key in augmented_synonym_in_pos_dict_0.keys():
        keys.append(key)
    for key in augmented_synonym_in_pos_dict_1.keys():
        keys.append(key)
    for key in augmented_synonym_in_pos_dict_2.keys():
        keys.append(key)
#     for key in augmented_synonym_in_pos_dict_3.keys():
#         keys.append(key)
    keys = list(set(keys))
    for key in keys:
        total_word_pool[key] = []
    for key in augmented_synonym_in_pos_dict_0.keys():
        for word in augmented_synonym_in_pos_dict_0[key]:
            total_word_pool[key].append(word)
    for key in augmented_synonym_in_pos_dict_1.keys():
        for word in augmented_synonym_in_pos_dict_1[key]:
            total_word_pool[key].append(word)
    for key in augmented_synonym_in_pos_dict_2.keys():
        for word in augmented_synonym_in_pos_dict_2[key]:
            total_word_pool[key].append(word)
#     for key in augmented_synonym_in_pos_dict_3.keys():
#         for word in augmented_synonym_in_pos_dict_3[key]:
#             total_word_pool[key].append(word)
    return total_word_pool

def generate_candidate_list(CNF_word_pool):
    augmented_list = augment_pos_syn_dict(CNF_word_pool)
    orig_list = CNF_word_pool
    for key in orig_list.keys():
        if key in augmented_list.keys():
            orig_list[key] = augmented_list[key]
        else:
            orig_list[key] = orig_list[key]
    return orig_list

def augment_pos_syn_dict(CNF_word_pool):
    pos_word_nested_dict = get_pos_word_nested_dict(CNF_word_pool)
    synonym_in_pos_dict = {}
    for poss in pos_word_nested_dict.keys():
        pos_word_dict = pos_word_nested_dict[poss]
        for pos in pos_word_dict.keys():
            synonyms = []
            for token in pos_word_dict[pos]:
                for syn in augment_synonyms_w_pos(token, poss):
                    synonyms.append(syn)
            synonym_in_pos_dict[pos] = synonyms
    return synonym_in_pos_dict

def get_POS_elements(POS_list):
    POS_elements = []
    for values in list(POS_list.values()):
        for value in values:
            POS_elements.append(value)
    return POS_elements

def get_pos_syn_dict(CNF_word_pool):
    
    pos_word_list = get_pos_word_list(CNF_word_pool)
    synonym_in_pos_dict = {}
    for pos in pos_word_list.keys():
        synonym_in_pos = []
        for token in pos_word_list[pos]:
            for syn in get_post_syn_set(token, pos):
                synonym_in_pos.append(syn)
        synonym_in_pos_dict[pos] = synonym_in_pos
    return synonym_in_pos_dict


def augment_synonyms_w_pos(token, pos):
    synonyms = list()
    for syn in wn.synsets(token):
        if syn.pos() == pos:
            terms = syn.lemma_names()
            synonyms.append(terms)
    synonym_set =[]
    for synonym in synonyms:
        for s in synonym:
            s = s.replace("_", " ").replace("-", " ").lower()
            s = "".join([char for char in s if char in ' qwertyuiopasdfghjklzxcvbnm'])
            synonym_set.append(s)
    return set(synonym_set)

def get_pos_word_nested_dict(CNF_word_pool):
    wn_pos_word_list = {}
    POS_list = get_POS_list(CNF_word_pool)
    POS_elements = get_POS_elements(POS_list)
    for key in POS_list.keys():
        #print(POS_list[key])
        wn_pos_word_list[key] = []
        pos_word_list = {}
        for poss in POS_list[key]:
            #print(poss)
            pos_word_list[poss] = []
            #print(CNF_word_pool[poss])
            for pos_word in CNF_word_pool[poss]: 
                pos_word_list[poss].append(pos_word)
        wn_pos_word_list[key] = pos_word_list
    return wn_pos_word_list


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


def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''