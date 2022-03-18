from util_pcfg.methods import *
from util_pcfg.preprocess import *
from util_pcfg.yk import *
from util_pcfg.save_data import *
from util_ge.utils import *
from util_ge.generator import *
from util_ge.augment import *
import os
import random
import sys
import benepar
import spacy
import nltk
from pathlib import Path

def aug_alp(text, n_aug, max_seq_len):
    
    sampled_data = len(text)
    num_output = n_aug
    seq_len = max_seq_len*2
    
    benepar.download('benepar_en3')
    nlp = spacy.load('en_core_web_sm')
    if spacy.__version__.startswith('2'):
        nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
    else:    
        nlp.add_pipe("benepar", config={"model": "benepar_en3"})

    constituency_trees = []
    for idx in range(len(text)):
        doc_sents = str(text[idx])
        doc = nlp(doc_sents)
        sentences = list(doc.sents)
        for each_sentence in sentences:
            res = each_sentence._.parse_string
            res = res.replace(" (_SP  )", "")
            res = res.replace(" (-LRB- -LRB-)", "")
            res = res.replace(" (-RRB- -RRB-)", "")
            constituency_trees.append(res)

    parse_trees = {}
    parse_trees[0] = constituency_trees
    clean_parses = neat_parses(parse_trees)
    #print(clean_parses)

    CFGrules, non_terminals = extract_CFGrules(clean_parses)
    PCFGrules = extract_PCFGrules(CFGrules)
    PCFGrules = PCFGrules.split()[:-1]

    nt_list, t_list, total_dict = make_nt_t_dict(constituency_trees)
    total_subtrees, candidate_sents, phrase_rules = extract_candidate_phrase(constituency_trees)

    _, CNFrules = find_CNFrules(PCFGrules, nt_list)
    CNFrules = CNFrule_dict_(CNFrules) ##important!!!    
    #print(CNFrules)
    CNFrule_list, CNFword_list = rules_words_list(CNFrules, nt_list)
    CNF_word_pool = CNF_word_pool_wo_prob(CNFword_list)
    rule_list = rules_list(CNFrules, t_list) ## important!! -> test
    plausible_rule_list = make_plausible_rules(rule_list) 
    with open('plausible_rule_list.txt', 'w') as f:
        f.write(str(plausible_rule_list))

    candidate_rule_pool = extrac_phrase_rules(phrase_rules)
    augmented_word_pool = generate_candidate_list(CNF_word_pool)

    total_word_pool = evolutionary_augmented_CNF_word_pool(CNF_word_pool)

    rule_word_dict = word_dict_pool(candidate_rule_pool, CNF_word_pool)
    syn_rule_word_dict = word_dict_pool(candidate_rule_pool, augmented_word_pool)
    augmented_rule_word_dict = word_dict_pool(candidate_rule_pool, total_word_pool)
    list1 = []
    list2 = []
    list3 = []
    potential_res = []
    if len(text[0]) < 50:
        list1 = generate_sentence(plausible_rule_list, candidate_sents)
        list2 = generate_sentence(plausible_rule_list, syn_rule_word_dict)
        list3 = generate_sentence(plausible_rule_list, augmented_rule_word_dict) 
        print(len(list1))
        print(len(list2))
        print(len(list3))
        potential_res = list1+list2+list3
    else:    
        list1 = generate_sentence(plausible_rule_list, candidate_sents)
        list2 = generate_sentence(plausible_rule_list, syn_rule_word_dict)
        #list3 = generate_sentence(plausible_rule_list, augmented_rule_word_dict)
        print(len(list1))
        print(len(list2))
        potential_res = list1+list2

    print(len(potential_res))
    total_augmented_data = []
    for i in range(num_output - sampled_data):
        doc = ''
        while len(doc) < seq_len: 
            idx = random.randint(0, len(potential_res)-1)
            doc += str(potential_res[idx]) + ' ' 
        doc = doc.replace('\t', ' ')
        total_augmented_data.append(str(doc))
    
    return total_augmented_data
        

