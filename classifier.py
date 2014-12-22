import math
import re

class Classifier:
    def __init__(self):
        
        self.priorProb = {}
        self.condProb = {}
        self.learn('train.data');
        return;

    # Add your code here.
    # Read training data and build your naive bayes classifier
    # Store the classifier in this class
    # This function runs only once when initializing
    # Please read and only read train_data: 'train.data'
    def learn(self, train_data):
        #total number of training examples
        numTrainEx=0
        #dictionary to save number of each democrats and republicans
        numParties= {}
        #dictionary to save the counts of each feature
        dictionary = {}
        with open('train.data', 'r') as inputFile:
             lines = inputFile.readlines()
        data = [re.split('\t|,',line) for line in lines]
        for x in data:
            x[16] = re.sub('\n', '', x[16])
        for x in data:
            index=0
            numTrainEx= numTrainEx+1
            instance = []
            for i in range(len(x)):
                #print x[i]
                if i==0:
                    party = x[i]
                else:
                    instance.append(x[i])
            
            dictionary.setdefault(party, {})
            
            for featureValue in instance:
                 index += 1
                 dictionary[party].setdefault(index,{})
                 #print dictionary
                 dictionary[party][index].setdefault(featureValue,0)
                 dictionary[party][index][featureValue] += 1
                 
            numParties.setdefault(party,0)
            numParties[party]= numParties[party]+ 1            
        #prior probabilities
        self.calPriorProb(numParties,numTrainEx)
            
        #print dictionary
        #for smoothing
        for index in range(1,16):    
            for featureValue in ['y','?','n']:    
                    dictionary['republican'][index].setdefault(featureValue,0)
                    dictionary['republican'][index][featureValue] += 0.0007
                    dictionary['democrat'][index].setdefault(featureValue,0)
                    dictionary['democrat'][index][featureValue] += 0.0007         
        #print dictionary      
         #conditional probabilities
        self.calCondProb(dictionary,numParties) 
        #print self.condProb
        return;

    # Add your code here.
    # Use the learned naive bayes classifier to predict
    # query example: 'n,y,n,y,y,y,n,n,n,y,?,y,y,y,n,y'
    # return 'republican' or 'republican'
    def solve(self, query):
         """Return class we think item Vector is in"""
         results = []
         data=query.split(',')
         for (party, prior) in self.priorProb.items():
             prob = prior
             index = 1
             for featureValue in data:
                 #this case not possible though since we did smoothing
                 if not featureValue in self.condProb[party][index]:
                     prob = 0
                 else:
                     prob = prob * self.condProb[party][index][featureValue]
                     index += 1
             results.append((prob, party))
         #return highest probability
         if results[0][0] > results[1][0]:
             return results[0][1]
         else:
             return results[1][1]

    def calPriorProb(self,x,y):
        for (party, count) in x.items():
             self.priorProb[party]=float(count) / y
         
    def calCondProb(self,dictionary,numParties):
        for (party, cols) in dictionary.items():
             self.condProb.setdefault(party, {})
             for (index, valueCounts) in cols.items():
                 self.condProb[party].setdefault(index, {})
                 for (attrValue, count) in valueCounts.items():
                     self.condProb[party][index][attrValue] = (float(count) / (numParties[party]+3*0.0007))

        
        
