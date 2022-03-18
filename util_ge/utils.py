import re


def extract_micro_rules(phrase_rules, candidate_sents):
    '''rule corresponding to each word''' 
    phrase_list = {}
    sets = []
    for key in phrase_rules.keys():
        if phrase_rules[key][0]!='':
            phrase_list[key] = phrase_rules[key]
            for acr in phrase_rules[key]:
                sets.append([a for a in acr.split()][0])
    #phrase_list
    candidates = set(sets)
    micro_rules = {}
    for candidate in candidates:
        micro_rules[candidate] = candidate_sents[candidate]
    return micro_rules 

# def extract_final_ruleset(candidate_rule_pool):
#     rule_set = {}
#     exist = []
#     for key in candidate_rule_pool.keys():
#         for elem in candidate_rule_pool[key]:
#             if len(elem) > 20:
#                 if key not in exist:
#                     exist.append(key)
#                     rule_set[key] = []
#                 else:
#                     rule_set[key].append(elem)
#     return rule_set
    

def extrac_phrase_rules(phrase_rules):
    phrase_list = {}
    for key in phrase_rules.keys():
        if phrase_rules[key][0]!='':
            phrase_list[key] = phrase_rules[key]
    return phrase_list


def extract_candidate_phrase(constituency_trees):
    nt_list, t_list, _ = make_nt_t_dict(constituency_trees)
    
    extract_subtree = []
    for constituency_tree in constituency_trees:
        extract_subtree.append(list(parenthetic_contents(constituency_tree)))
    total_subtrees = {}
    for nt in nt_list:
        total_subtrees[nt] = []

    for subtree_list in extract_subtree:
        for subtree in subtree_list:
            total_subtrees[subtree[1].split()[0]] = []

    for subtree_list in extract_subtree:
        for subtree in subtree_list:
            total_subtrees[subtree[1].split()[0]].append(' '.join(subtree[1].split()[1:]))
    
    candidate_sents = {}
    phrase_rules = {}
    for key in total_subtrees.keys():
        total_subtrees[key] = set(total_subtrees[key])
        candidate_sents[key] = []
        phrase_rules[key] = []
#         sentences = []
#         rules = []
        for words_list in total_subtrees[key]:
            sentence = []
            rule = []    
            for word in words_list.split():
                word = word.replace('(', '')
                word = word.replace(')', '')
                if word in t_list:
                    sentence.append(word)
                elif word in nt_list:
                    rule.append(word)
            
            candidate_sents[key].append(' '.join(sentence))
            phrase_rules[key].append(' '.join(rule))
#         candidate_sents[key].append(sentences)
#         phrase_rules[key].append(rules)
        phrase_rules[key] = list(set(phrase_rules[key]))
        total_subtrees[key] = total_subtrees[key]
        
    return total_subtrees, candidate_sents, phrase_rules

def rules_words_list(CFGrules, nt_list):
    rules = {}
    words = {}
    for key in CFGrules.keys():
        if key in nt_list:
            words[key] = CFGrules[key]
        else:
            rules[key] = CFGrules[key]

    return rules, words

########################################
def rules_list(CFGrules, t_list):
    result = {}
    for key in CFGrules.keys():
        res = []
        for elem in CFGrules[key]:
            elem = elem[0]
            elem = elem.replace('.<br', '')
            elem = elem.replace('/><br', '')
            if elem not in t_list:
                res.append(elem)
        result[key] = res

    return result

def make_plausible_rules(rule_list):
    plausible_rule_list = []
    plausible_rule_list.append('S')
    plausible_rule_list.append('SQ')
    plausible_rule_list.append('SBAR')
    plausible_rule_list.append('ADJP')
    plausible_rule_list.append('ADVP')
        
    for i in rule_list['S']:
        plausible_rule_list.append(i)
    return plausible_rule_list

def CFGrule_dict(data):
    rules = open('output/{}/CFGrules.txt'.format(data)).read().split('\n')
    lhs_list = [rule.split('->')[0] for rule in rules]
    lhs_set = set(lhs_list)
    lhs_dict = {}
    for lhs in lhs_set:
        lhs_dict[lhs] = []
    count = 0
    for rule in rules:
#         print(rule)
#         print(rule.split('->')[0])
#         print(rule.split('->')[1])
        lhs_rhs = rule.split('->')
        lhs = lhs_rhs[0]
        rhs = lhs_rhs[1]
        lhs_dict[lhs].append(rhs)
    for lhs in lhs_dict.keys():  
        lhs_dict[lhs] = list(set(lhs_dict[lhs]))
    return lhs_dict

def PCFGrule_dict(data):
    rules = open('output/{}/PCFGrules.txt'.format(data)).read().split('\n')
    lhs_list = [rule.split('->')[0] for rule in rules]
    lhs_set = set(lhs_list)
    lhs_dict = {}
    for lhs in lhs_set:
        lhs_dict[lhs] = []
    for rule in rules:
    #     print(rule.split('->')[0])
    #     print(rule.split('->')[1])
        lhs_rhs = rule.split('->')
        #print(lhs_rhs)
        lhs = lhs_rhs[0]
       
        rhs = lhs_rhs[1].split('#')[0]
        prob = lhs_rhs[1].split('#')[1]
        lhs_dict[lhs].append((rhs, prob))
    return lhs_dict

def CNFrule_dict_(CNFrules):
    lhs_list = [rule.split('->')[0] for rule in CNFrules]
    lhs_set = set(lhs_list)
    lhs_dict = {}
    for lhs in lhs_set:
        lhs_dict[lhs] = []
    for rule in CNFrules:
#         print(rule.split('->')[0])
#         print(rule.split('->')[1])
        lhs_rhs = rule.split('->')
        if len(lhs_rhs) == 1:
            continue
        lhs = lhs_rhs[0]
        if len(lhs_rhs[1].split('#')) != 2:
            continue
        rhs = lhs_rhs[1].split('#')[0]
        prob = lhs_rhs[1].split('#')[1]
        lhs_dict[lhs].append((rhs, prob))
    return lhs_dict


def CNFrule_dict(dataset, file):
    rules = open('output/{}/preprocessing/{}'.format(dataset, file)).read().split('\n')
    lhs_list = [rule.split('->')[0] for rule in rules]
    lhs_set = set(lhs_list)
    lhs_dict = {}
    for lhs in lhs_set:
        lhs_dict[lhs] = []
    for rule in rules:
#         print(rule.split('->')[0])
#         print(rule.split('->')[1])
        lhs_rhs = rule.split('->')
        if len(lhs_rhs) == 1:
            continue
        lhs = lhs_rhs[0]
        if len(lhs_rhs[1].split('#')) != 2:
            continue
        rhs = lhs_rhs[1].split('#')[0]
        prob = lhs_rhs[1].split('#')[1]
        lhs_dict[lhs].append((rhs, prob))
    return lhs_dict


def dependency_head_list(constituency_tree, dephead):
    nt_t_list = match_nt_t(constituency_tree)
    head_indices = dependency_head_index(dephead)
    #print("head_indices",head_indices)
    head_nt_t_list = []
    for idx in head_indices:
        #print("idx",idx)
        #print(nt_t_list[int(idx)])
        head_nt_t_list.append(nt_t_list[int(idx)])
#     head_nt_t_list.append(head_nt_t)
    return head_nt_t_list

def dependency_head_index(dephead):
    #dephead = dephead_0.read().split('\n')
    #dependency_heads_indices = []
    #for dephead in depheads:
    if len(dephead) == 0:
        return []
        
    dependency_heads = []
    for dep in dephead.split():
        dep = dep.replace('[', '')
        dep = dep.replace(']', '')
        dep = dep.replace(',', '')
        dependency_heads.append(int(dep))
#         if len(dependency_heads) != 0:
#             dependency_heads.append(set(dependency_heads))
    return list(set(dependency_heads))


def make_nt_t_dict(constituency_trees): 
    total_dict = {}
    nt_list = []
    nt_t_container = []
    for constituency_tree in constituency_trees:
        nt_t_list = match_nt_t(constituency_tree)
        nt_t_list = list(set(nt_t_list))
        for nt_t in nt_t_list:
            nt_list.append(nt_t.split()[0])
            nt_t_container.append(nt_t)
    nt_list = list(set(nt_list)) 
    for nt in nt_list:
        total_dict[nt] = []    
    
    exist = []
    t_list = []
    for nt_t in nt_t_container:
        if len(nt_t.split()) > 1:
            t = nt_t.split()[1]
            t_list.append(t)
            if t not in exist:
                total_dict[nt_t.split()[0]].append(t)
                exist.append(t)
    
    return nt_list, list(set(t_list)), total_dict


def match_nt_t(constituency_tree): 
    #constituency_tree = constituency_tree_0.read().split('\n')
    #nt_t_list = []
#     for ex in constituency_tree:
    res = re.findall(r'\(.*?\)', constituency_tree)
    #print("res", res)
    res_list = [extract_reverse_string(r) for r in res]
    #print("res_list",res_list)
#     nt_t_list.append(res_list)
    return res_list

def extract_reverse_string(string): 
    stack = 0
    startIndex = None
    results = []
    string = string[::-1]
    #print(string)
    for i, c in enumerate(string):
        if c == ')':
            if stack == 0:
                startIndex = i + 1 # string to extract starts one index later
            # push to stack
            stack += 1
        elif c == '(':
            # pop stack
            stack -= 1
            if stack == 0:
                return string[startIndex:i][::-1]
            
def extract_strings(string):
    stack = 0
    startIndex = None
    results = []

    for i, c in enumerate(string):
        if c == '(':
            if stack == 0:
                startIndex = i + 1 # string to extract starts one index later

            # push to stack
            stack += 1
        elif c == ')':
            # pop stack
            stack -= 1

            if stack == 0:
                results.append(string[startIndex:i]) 

    return results


def extract_string(string):
    stack = 0
    startIndex = None
    results = []

    for i, c in enumerate(string):
        if c == '(':
            if stack == 0:
                startIndex = i + 1 # string to extract starts one index later

            # push to stack
            stack += 1
        elif c == ')':
            # pop stack
            stack -= 1

            if stack == 0:
                return string[startIndex:i]
            
def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])




