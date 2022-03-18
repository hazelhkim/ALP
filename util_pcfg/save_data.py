def save_labeled_data(content, save_path):
    # e.g. sst2
    labeled_text =[]
    for label in content.keys():
        for c in content[label]:
            labeled_text.append(str(c)  + '\t' + str(label)) 
    with open(save_path, 'w') as f:
        f.write('\n'.join(labeled_text))

def save_CFG_rules(content, dataset):
    # e.g. sst2
    with open("output/{}/preprocessing/CFGrules.txt".format(dataset),"w") as f:
        f.write('\n'.join(content.split('\t')))

def save_non_terminals(content, dataset):
    # e.g. sst2
    with open("output/{}/preprocessing/non_terminals.txt".format(dataset),"w") as f:
        f.write(content)
        
def save_parses(content, dataset):      
    with open("output/{}/preprocessing/parses.txt".format(dataset),"w") as f:
        f.write(str(content))
        
def save_PCFG_rules(content, dataset):
    with open("output/{}/preprocessing/PCFGrules.txt".format(dataset),"w") as f:
        f.write('\n'.join(content.split('\t')))
        