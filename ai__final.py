# -*- coding: utf-8 -*-
"""ai__Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bFFlIU-MF56Bt6dX1edpg14OptUTmTSi

# SUBMITTED BY : 
 
  SUNIDHI SINGLA   101983052

In this notebook, I have made an attempt to get a simple text classification model up and running. In this, amazon fine food review data from Kaggle (Link for the dataset-https://www.kaggle.com/simonerossi/sentiment-analysis-on-fine-food-reviews)

#                                                  SENTIMENT ANALYSIS

### Importing all the Libraries
"""

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt 
import seaborn as sns
import sklearn
import nltk
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
nltk.download('wordnet')
nltk.download('stopwords')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from nltk.tokenize import TweetTokenizer
import string

"""#### Reading Dataset"""

df=pd.read_csv('Reviews.csv')
print(df.info())

df['sentiment'] = np.where(df.Score>3, 1,np.where(df.Score<3, -1,0))
df.rename(columns={'Text': 'review'}, inplace=True)
df=df[["review","sentiment"]]
print(df.sentiment.value_counts())
df

"""# Handling Missing Values"""

#Finding if there is any row with NULL value
print("Total Samples which do not have reviews: ",len(df[df["review"]==None]))
print("Total Samples which do not have sentiments: ",len(df[df["sentiment"]==None]))
#If there is any missing value then drop that row
df.dropna(inplace=True)
df

"""# Undersampling"""

shuffled_df = df.sample(frac=1,random_state=4)
df1 = shuffled_df.loc[shuffled_df['sentiment'] == 0]
df1_temp = shuffled_df.loc[shuffled_df['sentiment'] == 1].sample(n=42640,random_state=42)
df2_temp = shuffled_df.loc[shuffled_df['sentiment'] == -1].sample(n=42640,random_state=42)

normalized_df = pd.concat([df1_temp,df1,df2_temp])

plt.figure(figsize=(8, 8))
sns.countplot('sentiment', data=normalized_df)
plt.title('Count')
plt.show()
df=normalized_df
print(df.sentiment.value_counts())

#Mapping positive to 1 and negative to -1 and neutral to 0

df.loc[df['sentiment'] == 1, 'sentiment'] = "positive"
df.loc[df['sentiment'] == -1, 'sentiment'] = "negative"
df.loc[df['sentiment'] == 0, 'sentiment'] = "neutral"
df

"""### Data Cleaning """

#Data Cleaning
def process_string(text): 
   
    text = re.sub(r"https:\/\/.*[\r\n]*","",text) #remove any urls from the text
    text = re.sub(r"www\.\w*\.\w\w\w","",text)    #remove any urls starting from www. in the text
    text = re.sub(r"<[\w]*[\s]*/>","",text)       #remove any html elements from the text
    text = re.sub(r"[\.]*","",text)               #remove prediods  marks
    text= re.sub('[0-9\n]',' ',text)              # Remove numbers
    text = re.sub(r"[,.;@#?!&$_]+\ *", " ", text) #Remove special character
   
    tokenizer = TweetTokenizer(preserve_case=False,strip_handles=True,reduce_len=True)   #initilze tweet tokenizer    
    text_tokens = tokenizer.tokenize(text)          #tokenize text
    porter_stemmer = PorterStemmer()                #intizlize porter stemmer
    english_stopwords = stopwords.words("english")  #get english stopwords
    english_stopwords.remove('not')
    temp = ["br","href", 'http', 'just', 'amazon', 'product','time','year', 'tried','i\'ve']
    english_stopwords.extend(temp)
    cleaned_text_tokens = []                        # a list to hold cleaned text tokens
    
    for word in text_tokens:
        if((word not in english_stopwords) and #remove stopwords
            (word not in string.punctuation)): #remove punctuation marks
                
                stemmed_word = porter_stemmer.stem(word) #get stem of the current word
                cleaned_text_tokens.append(stemmed_word) #appened stemmed word to list of cleaned list
    
    #combine list into single string
    clean_text = " ".join(cleaned_text_tokens)
    
    return clean_text

df["review"] = df["review"].apply(process_string)
df

"""# Word Cloud after Data Cleaning"""

#After Cleaning and Preprocessing, lets make a Word Cloud
wordcloud = WordCloud( background_color="white",width=2000,height=2000, max_words=2000).generate(str(df))
plt.figure(1,figsize=(10, 10))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

"""### Tf-Idf"""

vectorizer = TfidfVectorizer()  #term frequency–inverse document frequency
X = vectorizer.fit_transform(df.review)
print(vectorizer.get_feature_names())
print(X)

"""# Training and testing data"""

#Splitting to training and testing
tfidf_train,tfidf_test,sentiment_values_train,sentiment_values_test=train_test_split(X,df.sentiment,test_size=0.20,random_state=0)

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score      
from sklearn.model_selection import StratifiedKFold             
from sklearn import metrics        
from sklearn.ensemble import RandomForestClassifier    
from sklearn.naive_bayes import BernoulliNB     
from sklearn.naive_bayes import GaussianNB     
from sklearn.naive_bayes import MultinomialNB   
from sklearn.tree import DecisionTreeClassifier 
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score                       
kfold = StratifiedKFold(n_splits=12) 
max_f1score=0
model_name=''

"""# Logistic Regression"""

lr = LogisticRegression(random_state=0, C=0.82286, max_iter=2000)                                
cv = cross_val_score(lr,tfidf_train,sentiment_values_train,cv=kfold)                                               
print("Cross Validation Scores                :",cv)
print("Mean of Cross Validation score         :",cv.mean()*100)
lr.fit(tfidf_train,sentiment_values_train)                                                                          
sentiment_values_pred_lr=lr.predict(tfidf_test)    
report=classification_report(sentiment_values_test, sentiment_values_pred_lr,target_names=['negative','positive','neutral'])    
print("Classification Report: \n",report)    
f1=metrics.f1_score(sentiment_values_pred_lr,sentiment_values_test,average='weighted')*100
cm=confusion_matrix(sentiment_values_test, sentiment_values_pred_lr)                                                         
print("Confusion Matrix                       :\n",cm)
print('The accuracy of the Logistic Regression:',metrics.accuracy_score(sentiment_values_pred_lr,sentiment_values_test)*100)    
print('The f1_score of the Logistic Regression:',f1)         
plot_confusion_matrix(lr,tfidf_test , sentiment_values_test) 
plt.show()
if(f1>max_f1score):
    max_f1score=f1
    model_name=LogisticRegression

"""# SVM"""

linear_svc = LinearSVC(C=0.5, random_state=42)
linear_svc.fit(tfidf_train, sentiment_values_train)
predict = linear_svc.predict(tfidf_test)
cv = cross_val_score(linear_svc,tfidf_train,sentiment_values_train,cv=kfold)                                                 #It takes the features df and target y , splits into k-folds (which is the cv parameter), fits on the (k-1) folds and evaluates on the last fold. It does this k times, which is why you get k values in your output array.Helps to determine hyperparameters for the model which will reult in lowest test errors.
print("Cross Validation Scores                :",cv)
print("Mean of Cross Validation score         :",cv.mean()*100)
report=classification_report(sentiment_values_test, predict,target_names=['negative','positive','neutral'])    
print("Classification Report: \n",report)         
matrix=confusion_matrix(sentiment_values_test, predict)
print("Confusion Matrix: \n",matrix)
accuracy=accuracy_score(sentiment_values_test, predict)*100    
print("Accuracy: \n", accuracy)
f1=f1_score(sentiment_values_test, predict,average='weighted')*100
print("F1 score: \n",f1)                           
if(f1>max_f1score):
    max_f1score=f1
    model_name=linear_svc
plot_confusion_matrix(linear_svc,tfidf_test , sentiment_values_test) 
plt.show()

"""## Bernoulli Naive Bayes"""

model_nb = BernoulliNB()
model_nb.fit(tfidf_train, sentiment_values_train)
predict=model_nb.predict(tfidf_test)
cv = cross_val_score(model_nb,tfidf_train,sentiment_values_train,cv=kfold)                                                 #It takes the features df and target y , splits into k-folds (which is the cv parameter), fits on the (k-1) folds and evaluates on the last fold. It does this k times, which is why you get k values in your output array.Helps to determine hyperparameters for the model which will reult in lowest test errors.
print("Cross Validation Scores                :",cv)
print("Mean of Cross Validation score         :",cv.mean()*100)
report=classification_report(sentiment_values_test, predict,target_names=['negative','positive','neutral'])
print("Classification Report: \n",report)      
matrix=confusion_matrix(sentiment_values_test, predict)
print("Confusion Matrix: \n",matrix)
accuracy=accuracy_score(sentiment_values_test, predict)*100    
print("Accuracy: \n", accuracy)

f1score=f1_score(sentiment_values_test, predict,average='weighted')*100
print ("F1 score: \n", f1score)                          
plot_confusion_matrix(model_nb,tfidf_test , sentiment_values_test)   
plt.show()                                                         
if(f1score>max_f1score):
    max_f1score=f1score
    model_name=BernoulliNB

"""# MultinomialNB"""

mnb = MultinomialNB(alpha=2)
cv = cross_val_score(mnb,tfidf_train,sentiment_values_train,cv=kfold)
print("Cross Validation Scores                :",cv)
print("Mean of Cross Validation score         :",cv.mean()*100)
mnb.fit(tfidf_train,sentiment_values_train)
y_pred_mnb=mnb.predict(tfidf_test)
cm=confusion_matrix(sentiment_values_test, y_pred_mnb)
f1score=metrics.f1_score(y_pred_mnb,sentiment_values_test,average='weighted')*100
print("Confusion Matrix                       :\n",cm)
print('The accuracy of the Naive Bayes        :', metrics.accuracy_score(y_pred_mnb,sentiment_values_test)*100)
print('The f1 score of the Naive Bayes        :', f1score)
print("\n",metrics.classification_report(y_pred_mnb,sentiment_values_test))
plot_confusion_matrix(mnb,tfidf_test , sentiment_values_test)   
plt.show()                                                         
if(f1score>max_f1score):
    max_f1score=f1score
    model_name=MultinomialNB

"""## Decision Tree Classifier"""

maximum_tree_depth= 15
model_dt = DecisionTreeClassifier(max_depth=maximum_tree_depth)
model_dt.fit(tfidf_train,sentiment_values_train)
predict = model_dt.predict(tfidf_test)
report=classification_report(sentiment_values_test, predict,target_names=['negative','positive','neutral'])
print("Classification Report: \n",report)                  
matrix=confusion_matrix(sentiment_values_test, predict)
print("Confusion Matrix: \n",matrix)
accuracy=accuracy_score(sentiment_values_test, predict)*100   
print("Accuracy: \n", accuracy)
f1=f1_score(sentiment_values_test,predict,average='micro')*100
print ("F1 score: \n", f1score)                          
plot_confusion_matrix(model_dt,tfidf_test , sentiment_values_test)    
plt.show() 
if(f1>max_f1score):
    max_f1score=f1
    model_name=DecisionTreeClassifier

"""#### Finding Best among above all Discussed Models """

print('Max F1_score is of following model')
print('F1-Score=',max_f1score,'\nModel name : ',model_name)

#MODEL TESTING
newreview = "Product arrived labeled as Jumbo Salted Peanuts...the peanuts were actually small sized unsalted. Not sure if this was an error or if the vendor intended to represent the product as Jumbo."

def prediction(text):   
        
    text = re.sub(r"https:\/\/.*[\r\n]*","",text)  
    text = re.sub(r"www\.\w*\.\w\w\w","",text)   
    text = re.sub(r"<[\w]*[\s]*/>","",text)
    text = re.sub(r"[\.]*","",text)
    text= re.sub('[0-9\n]',' ',text)
    text = re.sub(r"[,.;@#?!&$_]+\ *", " ", text)
   
    tokenizer = TweetTokenizer(preserve_case=False,strip_handles=True,reduce_len=True)
    text_tokens = tokenizer.tokenize(text)
    porter_stemmer = PorterStemmer()

    english_stopwords = stopwords.words("english")
    english_stopwords.remove('not')
    temp = ["br","href", 'http', 'just', 'amazon', 'product','time','year', 'tried','I\'ve']
    english_stopwords.extend(temp)
    cleaned_text_tokens = [] 
    
    for word in text_tokens:
        if((word not in english_stopwords) and 
            (word not in string.punctuation)): 
                
                stemmed_word = porter_stemmer.stem(word) 
                cleaned_text_tokens.append(stemmed_word)
    clean_text = " ".join(cleaned_text_tokens)
    clean_text =[clean_text]
    clean_text = vectorizer.transform(clean_text).toarray() 
    if linear_svc.predict(clean_text)[0] == 1:
            return "positive"   
    else:       
            return "negative"

feedback = prediction(newreview)

print("This review is: ", feedback)