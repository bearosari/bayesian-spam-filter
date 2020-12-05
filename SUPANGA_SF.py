#EEE 111 WFXY2 PRE-SOFTWARE PROJECT
#BEA ROSARI B. SUPANGA ---> 2018-10282
#NAIVE BAYES SPAM FILTER

import collections
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math
import nltk
import email 

def contentEmail(email_one): 
    """Removes the header of the emails and gets only the content"""
    parse = email.message_from_string(email_one)
    if parse.is_multipart():
        for payload in parse.walk():
            email_three = payload.get_payload()
            try:
                email_three = email_three
            except AttributeError:
                continue
        return email_three    
    else:
        email_two = parse.get_payload()
        email_two = email_two
        return email_two

def processText(text): 
    """Cleans the words according to the specifications to be considered as a word"""

    no_punc = [word for word in text.split() if word.isalpha()] # and word not in stopwords.words('english')]
     #removes non-letter characters and only includes words not included in stopwords
    no_punc = " ".join(no_punc) 
    clean_words = nltk.word_tokenize(no_punc) #splits the punctuation marks from the real words
    return clean_words


def train():
    """Gets the data from the train set, counts how many spam and ham occurences and gets top 5000 words"""
    num_spam=0 
    num_ham=0
    spam_words=()
    ham_words=()
    pullData = open("labels", "r").read()
    dataArray= pullData.split('\n')
    #print(dataArray)
    dataArrayTrain=dataArray[0:21300] #opens training set from folder 000-070
    
    for eachLine in dataArrayTrain:
        kind,file = eachLine.split(' ')
        file=file.strip('../') 
        #print(kind)
        #print(file)
        
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filepath = os.path.join(fileDir,file)  
        print(filepath)
        email=""
        fh = open(filepath, encoding="ascii", errors="ignore")
        for line in fh:
            email += line
        fh.close()
        email= email.lower()
        #print(email)
        email_words = processText(contentEmail(email))
        #print(email_words)
        email_words = tuple(list(set(email_words))) #converted it into a set to avoid repetition of words in every email
        #print(email_words)
        if (kind == "spam"):
            num_spam+=1 #counts how many spam emails
            spam_words= spam_words + tuple(email_words) #adds every word to a spam tuple

        elif (kind=="ham"):
            num_ham+=1 #counts how many ham emails
            ham_words= ham_words + tuple(email_words) #adds every word to a ham tuple

        spam_words= tuple(spam_words)
        ham_words= tuple(ham_words)

    
    count_spam = collections.Counter(spam_words)   #counts how many times a words appears in all spam emails
    count_ham = collections.Counter(ham_words)     #counts how many times a words appears in all ham emails
    total_count = (count_spam + count_ham).most_common(5000)  #adds the total occurences of the words and gets top 5000
    #print(total_count)
    #print(num_ham, num_spam)

    top_words = []
    for everyword in total_count:
        top_words.append(everyword[0])
    for everyword in list(count_spam):
        if everyword not in top_words:
            del count_spam[everyword] #deletes words in spam emails not included in top 5000
    for everyword in list(count_ham):
        if everyword not in top_words:
            del count_ham[everyword]   #deletes words in ham emails not included in top 5000
    #print(words, count_ham, count_spam)

    file_encoder = open("top_word_count.txt", "w+", encoding = 'utf-8', errors = 'ignore')
    file_encoder.write("HERE ARE YOUR TOP 5000 WORDS: "+"\n"+str(total_count)+"\n"+"\n"+"SPAM WORDS: "+"\n"+str(count_spam)+"\n"+"\n"+"HAM WORDS: "+"\n"+str(count_ham))
    file_encoder.close()
    print("Counting and getting top 5000 words successful!")
    probabilityGet(num_spam, num_ham, count_spam, count_ham)


def probabilityGet(NS,NH,SList,HList):
    """Computes the probability of spam and ham (Laplacian/Lambda Smoothing)"""
    global PS
    global PH
    PS = NS/(NS+NH) #probability of Spam
    PH = NH/(NS+NH) #probability of Ham
    AllPSpam = {}          
    AllPHam = {}

    lambd = input("Choose a value for your lambda: \n(a) 0.05 \n(b) 0.5 \n(c) 1 \n(d) 2 \nEnter letter of your choice: ") #Changeable lambda
    if lambd == 'a':
        lam= 0.05
    elif lambd == 'b':
        lam = 0.5
    elif lambd == 'd':
        lam = 2
    else:
        lam = 1

    for every_word,count in SList.items(): #computes probability of words in spam 
        print(every_word, count)
        L_Spam = (count+lam)/(NS+(5000*lam))
        AllPSpam[every_word] = L_Spam #contains all the probability of everyword in Spam
    for every_word,count in HList.items(): #computes probability of words in ham
        L_Ham = (count+lam)/(NH+(5000*lam))
        AllPHam[every_word] = L_Ham #contains all the probability of everyword in Ham
    print("Testing of emails now begins!")
    testingPhase(AllPSpam, AllPHam)


def testingPhase(SP, HP):
    """Gets data/words from testing set and applies Bayes Theorem using the values from Laplacian/Lambda Smoothing"""
    classification= {}
    TP, TN, FP, FN = 0,0,0,0

    pullData = open("labels", "r").read()
    dataArray= pullData.split('\n')
    dataArrayTest=dataArray[21301:-1] #opens files from folder 070 onwards 
 
    for eachLine in dataArrayTest:
        kind,file = eachLine.split(' ')
        print(file,kind)
        if (kind == "spam"):
            SO = 1 #initially stating that it is a spam not a ham
            HO = 0
        elif (kind== "ham"):
            HO = 1
            SO = 0
        file=file.strip('../') 
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filepath = os.path.join(fileDir,file)  
        email=""
        fh = open(filepath, encoding="ascii", errors="ignore")
        for line in fh:
            email += line
        fh.close()
        email= email.lower()
        email_words = processText(contentEmail(email))
        email_words = tuple(email_words)
        spam_ba= math.log(PS,10) #initially contains value of Spam Probability
        ham_ba= math.log(PH, 10) #initially contains value of Ham Probability


        """BAYES THEOREM"""
        for word, value in SP.items(): 
            if word in email_words:
                x = math.log(value, 10)
                spam_ba += x
            else:
                x =  math.log(1-value, 10)
                #print(x)
                spam_ba += x 
            if ham_ba > spam_ba:
                label="ham"
            elif ham_ba < spam_ba:
                label="spam"

        for word,value in HP.items():    
            if word in email_words:
                x =  math.log(value, 10)
                #print(x)
                ham_ba += x 
            else:
                x =  math.log(1-value, 10)
                #print(x)
                ham_ba += x   
            if ham_ba > spam_ba:
                label="ham"
            elif ham_ba < spam_ba:
                label="spam"

        print("Spam Prob: " ,spam_ba, "Ham Prob: " ,ham_ba)

        #This part determines if the emails are ham or spam depending on the calculations
        if HO == 1 and label == "ham":
            TN +=1
        if HO == 1 and label == "spam":
            FP +=1
        if SO == 1 and label == "spam":
            TP +=1
        if SO == 1 and label == "ham":
            FN +=1
        #print(classification)
        print(TP, TN, FP, FN)
        print(spam_ba)
        print(ham_ba)
    """COMPUTES PRECISION AND RECALL"""
    Precision = TP/(TP+FP)
    Recall = TP/(TP+FN)

    print("Precision:   ", Precision, "     ", "Recall:   ", Recall)
train()
