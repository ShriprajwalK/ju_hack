import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import confusion_matrix
import re

data = pd.read_csv("spam.csv", encoding = "latin-1")
data = data[['v1', 'v2']]
data = data.rename(columns = {'v1': 'label', 'v2': 'text'})

lemmatizer = WordNetLemmatizer()
stopwords = set(stopwords.words('english'))

def review_messages(msg):
    # converting messages to lowercase
    msg = msg.lower()
    return msg

def alternative_review_messages(msg):
    # converting messages to lowercase
    msg = msg.lower()

    # uses a lemmatizer (wnpos is the parts of speech tag)
    # unfortunately wordnet and nltk uses a different set of terminology for pos tags
    # first, we must translate the nltk pos to wordnet
    nltk_pos = [tag[1] for tag in pos_tag(word_tokenize(msg))]
    msg = [tag[0] for tag in pos_tag(word_tokenize(msg))]
    wnpos = ['a' if tag[0] == 'J' else tag[0].lower() if tag[0] in ['N', 'R', 'V'] else 'n' for tag in nltk_pos]
    msg = " ".join([lemmatizer.lemmatize(word, wnpos[i]) for i, word in enumerate(msg)])

    # removing stopwords 
    msg = [word for word in msg.split() if word not in stopwords]

    return msg

# Processing text messages
data['text'] = data['text'].apply(review_messages)

# train test split 
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size = 0.2, random_state = 1)

# training vectorizer
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)

# training the classifier 
svm = svm.SVC(C=1000)
svm.fit(X_train, y_train)

# testing against testing set 
X_test = vectorizer.transform(X_test)
y_pred = svm.predict(X_test) 
#print(confusion_matrix(y_test, y_pred))

# test against new messages 
def pred(msg):
    msg = vectorizer.transform([msg])
    prediction = svm.predict(msg)
    return prediction[0]
def check_eng(word_to_test):
    if len(wordnet.synsets(word_to_test)) == 0:
        return 0
    else:
        return 1

def get_probability_of_eng_words(string):
    list_of_words = (string.lower().split())
    #re.sub('[^0-9a-zA-Z]+', '*', s)
    list_of_words_new = []
    for i in list_of_words:
        list_of_words_new.extend(re.sub('[^a-z]+',' ', i).split()) 
    sum = 0
    for i in ((list_of_words_new)):
        #print(i,check_eng(i) )
        if check_eng(i) == 1:
            sum+=1
    #print(sum/len(list_of_words_new))
    dict_count = {}
    for i in list_of_words_new:
        if i not in dict_count:
            dict_count[i] = 1
        else:
            dict_count[i]+=1
    #print(dict_count)
    sum_set = 0
    for i in dict_count.keys():
        if check_eng(i) == 1:
            sum_set+=1
    #print(sum_set/len(dict_count))
    #print(len(dict_count)/len(list_of_words_new))
    return (sum*sum_set*(len(dict_count)/len(list_of_words_new))/(len(dict_count)*len(list_of_words_new)))
 
def get_pos_tag_probability(string):
    tokens = word_tokenize(string)
    pos_tagged_tuple = pos_tag(tokens)
    #print(pos_tagged_tuple)
    dict_pos = {}
    for i in pos_tagged_tuple:
        if i[1] not in dict_pos:
            dict_pos[i[1]] = [i[0]]
        else:
            dict_pos[i[1]].append(i[0])
    #print(dict_pos)
    return len(dict_pos)*len(pos_tagged_tuple)   

def end(string):
    f1 = pred(string)
    f2 = get_probability_of_eng_words(string)
    f3 = get_pos_tag_probability(string)
    #print(f1,f2,f3)
    if f1=="ham" and f2 > 0.35 and f3 > 150:
        return 1
    else:
        return 0

#"sxdfcvgbhj dcfvgbhnjm fghjk"
#"jain unversity laptop swimming pool"
#"The Office of Principal Scientific Adviser (PSA) has identified - Waste to Wealth mission to address waste mining at Ghazipur landfill. Innovators/startups who can solve this problem, apply for RFP (link: http://psa.gov.in/rfp/) psa.gov.in/rfp/ India @PrinSciAdvGoI Headstart Network Foundation"  
#"the @narendramodi  this is main cause of electricity problem in our colony.   Many illegal connections on a single pole.  Is this your new india? Ballia, 277001"


