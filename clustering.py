import numpy as np
import pandas as pd
import datetime as dt
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import stop_words
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

df_notenr = pd.read_csv('original_files/NotEnrolled.csv', encoding = "ISO-8859-1" )
df_enroll = pd.read_csv('original_files/EnrolledAllTIme.csv', encoding = "ISO-8859-1")
df_notenr['Enrolled'] = 0
df_enroll['Enrolled'] = 1

df_allapp = pd.concat([df_notenr,df_enroll])

df_essays = df_allapp.iloc[:,[1,2,3,4]]
df_essays = df_essays.fillna('')
col = ['Reason applying to this program?', 'Goals after Immersive Program',
       'Failure Or Challenge / Technical Problem',
       'About your professional and educational']
temp = pd.DataFrame()
# temp = pd.DataFrame(df_essays[col].apply(lambda x: ' '.join(x), axis=1))

temp['essays'] = df_essays[col[0]] + ' ' + df_essays[col[1]]+ ' ' + df_essays[col[2]]+ ' ' + df_essays[col[3]]

tfidf = TfidfVectorizer(stop_words=stop_words.ENGLISH_STOP_WORDS)
X = tfidf.fit_transform(temp.values.ravel())

kmeans = KMeans(n_clusters=5,random_state=0)
kmeans.fit(X)

order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
terms = tfidf.get_feature_names()
for i in range(5):
    print("Cluster {}:".format(i))
    for ind in order_centroids[i, :20]:
        print(terms[ind])

if __name__ == '__main__':
    pass
