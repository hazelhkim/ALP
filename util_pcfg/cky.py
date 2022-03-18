"""
Manipulated the code for PCFGs by nausheenfatma.
"""
class CKY :
    def __init__(self, dataset):
        self.production_rules={}
        self.input_file_path="output/{}/CNFrules.txt".format(dataset)
        self.output_file_path="output/{}/final_output.txt".format(dataset)
        self.N=[]           # set of non terminals
        self.N_file="output/{}/non_terminals.txt".format(dataset)
        self.rule_file="output/{}/CNFrules.txt".format(dataset)
        self.R={}           # dict of rules and its probability
        self.test_file="output/{}/test_input.txt".format(dataset)
        self.pi={}
        self.n=0
        self.bp_map={}
        self.W=[]
        self.output=[]
        #self.output_file=open(self.output_file_path,"a")
    
    def base_case(self):
        testfile=open(self.test_file,"r")
        rules_file=open(self.rule_file,"r")  
        
        for line in rules_file:
            line=line.rstrip()
            rule_txt=line.split("#")
            rule_full=rule_txt[0]
            lhs_rhs=rule_full.split("->")
            probability=rule_txt[1]
            lhs=lhs_rhs[0]
            
            if(lhs not in self.N):
                self.N.append(lhs)
            rhs=lhs_rhs[1]
            self.R[(lhs,rhs)]=float(probability)
        
        #base case pi initialisation for terminals of the sentence
        for sentence in testfile:
            self.W=sentence.split()
            i=0
            self.pi={}
            for w in self.W:
                i=i+1
                #base case initialisation
                for X in self.N:
                    key=str(i)+","+str(i)+","+X
                    lhs=X
                    rhs=w
                    rule=(lhs,rhs)
                    if rule in self.R.keys(): # if rule exists assign its probability
                        q=self.R[rule]
                        self.pi[key]=q 
                    else :                    # else assign zero probability
                        q=0
                        self.pi[key]=q
                #base case ends
            self.CKYdynamic()            
    
    def CKYdynamic(self):
        n=len(self.W)
        val=self.pi_fxn(1,n,'S')
        self.preorder_traversal(1,n,'S')
        self.output.append("\n")
                                                    
    def pi_fxn(self,i,j,X):
        
        key1=str(i)+","+str(j)+","+X
       
        if not i==j : #not base case
            max_pi=0
            for key, value in self.R.items() :
                if key[0]==X:  #key[0]is lhs of rule
                    q=self.R[key]
                    rhs=key[1] #key[1]is rhs of rule
                    rhs_tokens=rhs.split()
                    if len(rhs_tokens)==2:   
                        rhs_1=rhs_tokens[0]
                        rhs_2=rhs_tokens[1]
                        for s in range(i,j):
                            temp_pi=q*self.pi_fxn(i,s,rhs_1)*self.pi_fxn(s+1,j,rhs_2)
                            if temp_pi>max_pi:
                                max_pi=temp_pi
                                lhs_address=str(i)+","+str(s)+","+rhs_1
                                rhs_address=str(s+1)+","+str(j)+","+rhs_2
                                bp_value=[str(max_pi),lhs_address,rhs_address]
                                self.bp_map[key1]=bp_value
            self.pi[key1]=max_pi                             
        else:
            bp_value=[str(self.pi[key1])]
            self.bp_map[key1]=bp_value 
        return self.pi[key1]                   
    

    def preorder_traversal(self,i,j,NODE) : 
        key=str(i)+","+str(j)+","+NODE
        self.output.append("(")
        self.output.append(NODE)
        if(len(self.bp_map[key])==3): #left and right exists
            left_txt=self.bp_map[key][1]
            left_txt_tokens=left_txt.split(",")
            self.preorder_traversal(left_txt_tokens[0],left_txt_tokens[1],left_txt_tokens[2])
            
            right_txt=self.bp_map[key][2]
            right_txt_tokens=right_txt.split(",")
            self.preorder_traversal(right_txt_tokens[0],right_txt_tokens[1],right_txt_tokens[2])
        
        elif i==j  :
            index=int(i)-1
            self.output.append(" "+ self.W[index]) 
        self.output.append(")")

