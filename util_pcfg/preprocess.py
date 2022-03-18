def select_data(data_path, sample_num):
    import random
    labels = []
    contents = []
    data = []
    with open(data_path) as f:
        for line in f.readlines():
            labels.append(int(line.split('\t')[-1]))
            contents.append(line.split('\t')[0]) 

    num_class = max(labels) + 1
    sample_num = sample_num #10
#     sampled_data = []
    stats = {label: 0 for label in range(num_class)}
#     print(stats)

#     idx = 0
#     while True:
#         idx += 1
#         if len(sampled_data) == num_class*sample_num:
#             break
#         for label in range(num_class):   
#             if stats[label] < sample_num:
#                 sampled_data.append((labels[idx], contents[idx]))
#             else:
#                 break
        
#     print(sampled_data)
    
#     print("Length of total sampled data: ",len(sampled_data))
    
    labeled_data = {}
    for l in range(num_class):
        #labeled_data[l] = []
        contents_per_label = []
        while len(contents_per_label) < sample_num:
            idx = random.randint(0, len(labels)-1)
            label = int(labels[idx])
            if label == l:
                contents_per_label.append(contents[idx])
            if len(contents_per_label) == sample_num:
                continue
        labeled_data[l] = contents_per_label
    return labeled_data, num_class

def select_agnews_data(data_path, sample_num):
    import random
    labels = []
    contents = []
    data = []
    with open(data_path) as f:
        for line in f.readlines():
            labels.append(int(line.split('\t')[-1]))
            contents.append(line.split('\t')[0]) 

    num_class = max(labels)
    sample_num = sample_num #10
#     sampled_data = []
    stats = {label: 0 for label in range(num_class)}
#     print(stats)

#     idx = 0
#     while True:
#         idx += 1
#         if len(sampled_data) == num_class*sample_num:
#             break
#         for label in range(num_class):   
#             if stats[label] < sample_num:
#                 sampled_data.append((labels[idx], contents[idx]))
#             else:
#                 break
        
#     print(sampled_data)
    
#     print("Length of total sampled data: ",len(sampled_data))
    
    labeled_data = {}
    for l in range(num_class):
        #labeled_data[l] = []
        contents_per_label = []
        while len(contents_per_label) < sample_num:
            idx = random.randint(0, len(labels)-1)
            label = int(labels[idx])
            #print(label)
            if label == l+1:
                contents_per_label.append(contents[idx])
            if len(contents_per_label) == sample_num:
                break
        labeled_data[l] = contents_per_label
    return labeled_data, num_class



# def select_data(data_path, sample_num):
#     labels = []
#     contents = []
#     data = []
#     with open(data_path) as f:
#         for line in f.readlines():
#             labels.append(int(line.split('\t')[1]))
#             contents.append(line.split('\t')[0]) 

#     num_class = max(labels) +1
#     print("Num of class: ",num_class)
#     sample_num = sample_num #10
#     print("Num of Sample: ", sample_num)
#     sampled_data = []
#     stats = {label: 0 for label in range(num_class)}
# #     print(stats)

#     idx = 0
#     while True:
#         if len(sampled_data) == num_class*sample_num:
#             break
#         for label in range(num_class):   
#             if stats[label] < sample_num:
#                 sampled_data.append((labels[idx], contents[idx]))
#                 idx += 1
#             else:
#                 break
        
# #     print(sampled_data)
#     print("Length of total sampled data: ",len(sampled_data))
    
#     labeled_data = {}
#     for l in labels:
#         #labeled_data[l] = []
#         contents_per_label = []
#         for data in sampled_data:
#             label = data[0]
#             if label == l:
#                 contents_per_label.append(data[1])
#         labeled_data[l] = contents_per_label
#     return labeled_data, num_class


def split_data_label(labeled_data ,num_class):
    import benepar
    benepar.download('benepar_en3')
    import spacy
    spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')
    if spacy.__version__.startswith('2'):
        nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
    else:
        nlp.add_pipe("benepar", config={"model": "benepar_en3"})
        
    ###################
    labeled_sentences = {}
    for label in range(num_class):
        sentences = []
        contents = labeled_data[label]
        for sentence in contents:
            sentence_info = []
            doc = nlp(sentence)
            sent = list(doc.sents)
            for s in sent:
                sent_content = s._.parse_string
                sentence_info.append(sent_content)
            sentences.append(sentence_info)
        labeled_sentences[label] = sentences
    return labeled_sentences
