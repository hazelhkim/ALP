"""
Manipulated the code for PCFGs by nausheenfatma.
"""
import sys
sys.path.append("..")
from util_pcfg.yk import *
from util_pcfg.Stack import Stack


def extract_CFGrules(parse_trees: dict):
    stack = Stack()
    CFGrules = ''
    non_terminals = []
    t=[]
    stack=Stack()
    parse_trees_label = {}
    for c in range(len(parse_trees)):
        for tokens in parse_trees[c]:
            parse_trees_info = []
            for token in tokens.split():
                if not token == ')':
                    stack.push(token) # push tokens in stack
                else:
                    rule_stack=Stack()
                    while stack.peek()!='(':  # while beginning bracket is not 
                        popped = stack.pop()
                        rule_stack.push(popped)
                    stack.pop()  # pop the left bracket (
                    lhs = rule_stack.pop()
                    CFGrules += lhs
                    CFGrules += "->"
                    if lhs not in t:
                        t.append(lhs)
                        non_terminals.append(lhs)
                        non_terminals.append(" ")
                    stack.push(lhs) # push back the lhs to the stack
                    while not rule_stack.isEmpty():
                        pop_item=rule_stack.pop()
                        CFGrules += pop_item
                        CFGrules += " "
                    CFGrules += "\t"
            parse_trees_info.append(CFGrules)
        parse_trees_label[c] = parse_trees_info
    non_terminals = ''.join(non_terminals)
    return CFGrules, non_terminals


def neat_parses(labeled_parses: dict):
    labeled_parses_clean = {}
    for c in range(len(labeled_parses)):
        parses_clean = []
        for parse in labeled_parses[c]:
            tokens = []
            for token in parse.split():

                count_f = 0
                count_b = 0

                while '(' in token:
                    count_f += 1
                    token = token[1:]

                while ')' in token:
                    count_b += 1
                    token = token[:-1]

                for i in range(count_f):
                    tokens.append('(')

                #token = token[count_f:-count_b]
                tokens.append(token)

                for j in range(count_b):
                    tokens.append(') ')
            if ' ' not in tokens:
                tokens = ' '.join(tokens)
            parses_clean.append(tokens)
        labeled_parses_clean[c] = parses_clean
    return labeled_parses_clean
            
def get_nonbinary_spans(actions, SHIFT=0, REDUCE=1):
    spans = []
    tags = []
    stack = []
    pointer = 0
    binary_actions = []
    nonbinary_actions = []
    num_shift = 0
    num_reduce = 0
    for action in actions:
        # print(action, stack)
        if action == "SHIFT":
            nonbinary_actions.append(SHIFT)
            stack.append((pointer, pointer))
            pointer += 1
            binary_actions.append(SHIFT)
            num_shift += 1
        elif action[:3] == 'NT(':
            # stack.append('(')
            stack.append(action[3:-1].split('-')[0])
        elif action == "REDUCE":
            nonbinary_actions.append(REDUCE)
            right = stack.pop()
            left = right
            n = 1
            # while stack[-1] is not '(':
            while type(stack[-1]) is tuple:
                left = stack.pop()
                n += 1
            span = (left[0], right[1])
            tag = stack.pop()
            if left[0] != right[1]:
                spans.append(span)
                tags.append(tag)
            stack.append(span)
            while n > 1:
                n -= 1
                binary_actions.append(REDUCE)
                num_reduce += 1
        else:
            assert False
    assert (len(stack) == 1)
    assert (num_shift == num_reduce + 1)
    return spans, tags, binary_actions, nonbinary_actions

def get_terms_from_dict(input_dict: dict):
    final_output = {}
    for label in input_dict.keys():
        output = []
        content = input_dict[label]
        for line in content:
            output.append(get_terms(line))
        final_output[label] = output
    return final_output
        
def get_terms(line):
    NTs = []
    Ts = []
    term_dict = {}
    output_actions = []
    line_strip = line.rstrip()
    i = 0
    max_idx = (len(line_strip) - 1)
    while i <= max_idx:
        assert line_strip[i] == '(' or line_strip[i] == ')'
        if line_strip[i] == '(':
            if is_next_open_bracket(line_strip, i):  # open non-terminal
                curr_NT = get_nonterminal(line_strip, i)
                NTs.append(curr_NT)
                output_actions.append('NT(' + curr_NT + ')')
                i += 1
                # get the next open bracket,
                # which may be a terminal or another non-terminal
                while line_strip[i] == ' ':
                    i+=1
                if line_strip[i] != ' ':
                    currr_T = get_terminal(line_strip, i)
                    curr_T_info = currr_T.split(' ')
                    term_dict[curr_T_info[-1]] = curr_T_info[-2]
                Ts.append(currr_T)
                while line_strip[i] != '(':
                    i += 1
            else:  # it's a terminal symbol
                output_actions.append('SHIFT')
                while line_strip[i] != ')':
                    i += 1
                i += 1
                while line_strip[i] != ')' and line_strip[i] != '(':
                    i += 1
        else:
            output_actions.append('REDUCE')
            if i == max_idx:
                break
            i += 1
            while line_strip[i] != ')' and line_strip[i] != '(':
                i += 1
    assert i == max_idx

    return NTs

def get_terminal(line, start_idx):
    #assert line[start_idx] == ' '  # make sure it's an emtpy bracket
    output = []
    terminal =[]
    #for char in line[(start_idx + 1):]:
    for i in range(start_idx + 1, len(line)):  
        char = line[i]
        if char == ')':
            break
        if char == '(':
            continue
        #assert not (char == '(') and not (char == ')')
        output.append(char)
    return ''.join(output)

def get_nonterminal(line, start_idx):
    assert line[start_idx] == '('  # make sure it's an open bracket
    output = []
    for char in line[(start_idx + 1):]:
        if char == ' ':
            break
        assert not (char == '(') and not (char == ')')
        output.append(char)
    return ''.join(output)

def get_clean(string):
    ans = string
    for c in string:
        if c ==')':
            ans = ans[:-1]
    return ans

def extract_PCFGrules(CNFrules):
    lhs_dict={}
    rule_dict={}
    PCFGrules=''
    for line in CNFrules.split('\t'):
        line=line.rstrip()
        if line in rule_dict.keys():
            rule_dict[line]=rule_dict[line]+1
        else:
            rule_dict[line]=1
        lhs=line.split("->")[0]
        if lhs in lhs_dict.keys():
            lhs_dict[lhs]=lhs_dict[lhs]+1
        else:
            lhs_dict[lhs]=1
    for rule in rule_dict.keys():
        count_rule=rule_dict[rule]
        lhs=rule.split("->")[0]
        count_lhs=lhs_dict[lhs]
        rule_probability=count_rule/float(count_lhs)
        if(rule=='.->.'):
            PCFGrules += '.->dot'
        elif (rule==',->,'):
            PCFGrules += ',->comma'
        else:
            PCFGrules += rule
        PCFGrules += '#'
        PCFGrules += str(rule_probability)
        PCFGrules += "\t"
    PCFGrules = ''.join(PCFGrules)
    return PCFGrules


def find_CNFrules(PCFGrules, nt_list):
        lhs_dict={}         #dictionary to hold count of LHS
        rule_dict={}
        #nt_file=open(self.non_terminal_file_path,"r")
        V=[]                #list of non terminals
        final_rules=[]
        intermediate_rules={}
        change_rules={}
        rules=[]
        for line in nt_list:
            V=line.split()  
        #STEP 1 : keep only terminal rules & replace single value rhs non-terminals
        for line in PCFGrules :
            #examine rhs
            if line[0] == '#' or line[0] == '':
                continue
            #print('#'*100)
            rule=line.rstrip()
            split_txt=line.split("->")
            lhs=split_txt[0]
            if '->' not in line:
                continue
            rhs=split_txt[1].split("#")[0]
            rhs_tokens=rhs.split()
            if len(rhs_tokens)==1:            #check if terminal rule add the rule to CNF
                if(rhs_tokens[0] not in V) :  #the only element
                    final_rules.append(rule)
                    intermediate_rules[rule]=lhs
                else :
                    change_rules[rule]=lhs
            else :
                    intermediate_rules[rule]=lhs

        new_intermediate_rules={}
        i=1
        for rule in change_rules :
            i=i+1         
            line=rule
            rule_txt=rule.split("->")
            lhs=rule_txt[0]
            rhs_txt=rule_txt[1].split("#")
            if len(rhs_txt) == 1:
                continue
            rhs=rhs_txt[0]
            prob=float(rhs_txt[1])
            
            all_rhs=[]
            
            if rhs in change_rules.values(): #if RHS is in the set of single non terminal rules
                rhs_chain=rhs
                list_of_chain=[]
                
                for rule_read in change_rules:
                    if(rhs_chain==change_rules[rule_read]):
                        list_of_chain.append(rule_read.split("#")[0].split("->")[1])
                
                for rhs_chain1 in list_of_chain :
                        new_prob=prob
                        while rhs_chain1 in change_rules.values() :
                            for rhs_rule in change_rules :
                                    if(rhs_chain1==change_rules[rhs_rule]):
                                        int_rule_txt=rhs_rule.split("->")[1]
                                        int_rule_rhs_tokens=int_rule_txt.split("#")
                                        probability=float(int_rule_rhs_tokens[1])
                                        int_rule_rhs=int_rule_rhs_tokens[0]
                                        new_prob=new_prob*probability
                                        rhs_chain1=int_rule_rhs
                        all_rhs.append(rhs_chain1)    
            if rhs in intermediate_rules.values():
                all_rhs.append(rhs)

            for rhs_token in all_rhs:    
                if rhs_token in intermediate_rules.values():
                    for int_rule in intermediate_rules :
                        if(rhs_token==intermediate_rules[int_rule]):
                            int_rule_txt=int_rule.split("->")[1]
                            int_rule_rhs_tokens=int_rule_txt.split("#")
                            probability=float(int_rule_rhs_tokens[-1])
                            if int_rule_rhs_tokens[0] == '':
                                continue
                            int_rule_rhs=int_rule_rhs_tokens[0]
                            new_prob=prob*probability
                            new_rule=lhs+"->"+int_rule_rhs+"#"+str(new_prob)
                            new_intermediate_rules[new_rule]=lhs
                            final_rules.append(new_rule)
        
        for key in new_intermediate_rules.keys():
            intermediate_rules[key]=new_intermediate_rules[key]

        #STEP 2 : keep only terminal rules & replace single value rhs non-terminals
        for key in intermediate_rules.keys():
            rule_prob_txt=key.split("#")
            if len(rule_prob_txt) != 2:
                break
            rule=rule_prob_txt[0]
            prob=rule_prob_txt[1]
            rule_txt=rule.split("->")
            lhs=rule_txt[0]
            rhs=rule_txt[1]
            rhs_tokens=rhs.split()
            #print rhs_tokens
            if(len(rhs_tokens)==1):
               # print "len 1"
                if(rhs_tokens[0]  in V):
                    print("oops this should not be in rule1",rhs_tokens[0])
            elif(len(rhs_tokens))==2:
                for rhs_token in rhs_tokens :
                    if(rhs_token not in V):
                        print("oops this should not be in rule2")
                        break # break
                final_rules.append(key)
            elif(len(rhs_tokens))>2:
                joinees=rhs_tokens[:-1]
                no_of_joinees=len(rhs_tokens)-1
                joint="-".join(joinees)
                rule1=lhs+"->"+joint+" "+rhs_tokens[len(rhs_tokens)-1]+"#"+prob
                if not rule1 in final_rules:
                    final_rules.append(rule1)
                while (no_of_joinees >=2):
                    lhs=joint
                    rhs_joinee_tokens=joint.split("-")
                    new_joinees=rhs_joinee_tokens[:-1]
                    new_joint="-".join(new_joinees)
                    last_token=rhs_joinee_tokens[no_of_joinees-1]
                    joinee_rule=lhs+"->"+new_joint+" "+last_token+"#1"
                    no_of_joinees=no_of_joinees-1
                    joint=new_joint
                    if not joinee_rule in final_rules:
                        final_rules.append(joinee_rule)      

        return intermediate_rules, final_rules


