import numpy as np
import pandas as pd
import nltk
from sklearn import feature_extraction
import mpld3
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from random import choice
from string import ascii_uppercase
import glob


curr_year = str(datetime.date.today().year)
path = "data/*.csv"

seed = 0

colnames = ['title', 'content', 'date', 'link']

title = []
content = []
date = []
link = []

for fname in glob.glob(path):
    data = pd.read_csv(fname, names=colnames, encoding='latin-1', header=1)
    title += data.title.tolist()
    content += data.content.tolist()
    date += data.date.tolist()
    link += data.link.tolist()


    
df = pd.DataFrame({'title':title, 'content': content, 'date': date, 'link':link})

if len(df) == 0:
    title = ("None")
    content = ("The quick brown fox jumps over the lazy dog","The quick brown fox jumps over the lazy dog")
    date = ("None")
    link = ("None")
    df = pd.DataFrame({'title':title, 'content': content, 'date': date, 'link':link})

with open('custom_stopwords.txt', 'r') as myfile:
    data=myfile.readlines()#.replace('\n', '')
cus_stop = [i.replace('\n','') for i in data]
cus_stop.append(str(curr_year))

punc = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
stop_words = feature_extraction.text.ENGLISH_STOP_WORDS.union(punc)
stop_words = stop_words.union(cus_stop) #Join English + Custom Stop Words

stopwords = nltk.corpus.stopwords.words('english')

vectorizer = TfidfVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(df['content'].values.astype('U'))

word_features = vectorizer.get_feature_names()

stemmer = SnowballStemmer('english')
tokenizer = RegexpTokenizer(r'[a-zA-Z\']+')

def tokenize(text):
    return [stemmer.stem(word) for word in tokenizer.tokenize(text.lower())]

vectorizer2 = TfidfVectorizer(stop_words = stop_words, tokenizer = tokenize)
X2 = vectorizer2.fit_transform(df['content'].values.astype('U'))
word_features2 = vectorizer2.get_feature_names()

vectorizer3 = TfidfVectorizer(stop_words = stop_words, tokenizer = tokenize, max_features = 1000)
X3 = vectorizer3.fit_transform(df['content'].values.astype('U'))
words = vectorizer3.get_feature_names()

'''
# The Elbow Method #
wb = []
n = 11

for i in range(1, n):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X3)
    wb.append(kmeans.inertia_)

plt.plot(range(1, n),wb)
plt.title("The Elbow Method")
plt.xlabel("Number of Clusters K")
plt.ylabel("Average Within-Cluster distance to centroid")
plt.savefig('elbow.png')
plt.show()
'''
#while (True):
'''
print("5 Clusters")
kmeans = KMeans(n_clusters = 5, n_init = 20, n_jobs = 1) # n_init(number of iterations for clsutering) n_jobs(number of cpu cores to use)
kmeans.fit(X3)
# We look at 5 the clusters generated by k-means.
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))


print("8 Clusters")
kmeans = KMeans(n_clusters = 8, n_init = 20, n_jobs = 1) # n_init(number of iterations for clsutering) n_jobs(number of cpu cores to use)
kmeans.fit(X3)
# We look at 8 the clusters generated by k-means.
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))

'''
'''
print("9 Clusters")
k = 9
kmeans = KMeans(n_clusters = k, n_init = 20, n_jobs = 1)
kmeans.fit(X3)
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))
'''
with open('selected_model.txt', 'r') as myfile:
    model_name=myfile.read().replace('\n', '')
#print(model_name)
kmeans = joblib.load(model_name) #model-OVODN

def show_model_data():
    mo_data = []
    common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
    for num, centroid in enumerate(common_words):
        #print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))
        mo_data.append('Cluster ' + str(num) + ' : ' + ', '.join(words[word] for word in centroid))

    return mo_data

def load_model_check_contents(s):
    kmeans = joblib.load('models/'+str(s)+'.pkl')
    common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
    for num, centroid in enumerate(common_words):
        print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))


def gen_model(k):
    kmeans = KMeans(n_clusters = k, n_init = 20, n_jobs = 1) #n_jobs is num of cpu used
    kmeans.fit(X3)
    common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]

    model_name = ''.join(choice(ascii_uppercase) for i in range(5))
    model_name = 'models/model-'+model_name
    #model = joblib.load(model_name+'.pkl')
    joblib.dump(kmeans,  model_name+'.pkl')
    return model_name+".pkl"

clusters = kmeans.labels_.tolist()

to_predict = pd.read_csv('main.csv', names=colnames, encoding='latin-1', header=0)
to_predict_content = []
to_predict_title = []
to_predict_date = []
to_predict_link = []
to_predict_content += to_predict.content.tolist()
to_predict_title += to_predict.title.tolist()
to_predict_date += to_predict.date.tolist()
to_predict_link += to_predict.link.tolist()

#to_predict = pd.read_csv('rappler-'+curr_year+'.csv', names=colnames, encoding='latin-1', header=0)
#to_predict_content += to_predict.content.tolist()
#to_predict_title += to_predict.title.tolist()
#to_predict_date += to_predict.date.tolist()
#to_predict_link += to_predict.link.tolist()

def pred_which_clus(data):
    Y = vectorizer3.transform([data])
    return int(kmeans.predict(Y))



def main_with_clusters():
    predicted_clusters = []
    for x in to_predict_content:
        predicted_clusters.append(str(int(pred_which_clus(x))))
    
    df_predicted = pd.DataFrame({'title':to_predict_title, 'content': to_predict_content, 'date': to_predict_date, 'link':to_predict_link, 'cluster': predicted_clusters})
    df_predicted.sort_values(by=['date'], inplace=True, ascending=False)

    df_predicted.to_csv("main_with_clusters.csv",index=False)    

# Select the data with cluster == 2:
# df_predicted.loc[df_predicted['cluster'] == '2']['title'] #

def show_predicted_clusters():
    for n in range(0,kmeans.n_clusters):
        print("Cluster ",n," titles: ", df_predicted.loc[df_predicted['cluster'] == str(n)]['title'].tolist())
        print()





