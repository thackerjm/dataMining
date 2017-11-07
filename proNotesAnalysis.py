import pandas as pd
pd.options.display.width = 1000
pd.options.display.max_rows = 500
import pandas as pd
import nltk.data
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
from nltk.collocations import *
from nltk import word_tokenize
import string
import pymysql
# from secrets import mysqlPW, mysqlUser, myHost, myDB
import sys
sys.path.insert(0, '/Users/jxt3376/Desktop/Python/')
from secretsfile import mysqlPW, mysqlUser, myHost, myDB

conn = pymysql.connect(host=myHost, unix_socket='/tmp/mysql.sock', user=mysqlUser, passwd=mysqlPW, db=myDB, autocommit=False, cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()

cur.execute("Select * from PROF_CUST_NOTE limit 500")

notes_data = cur.fetchall()

cur.close()
conn.close()

CUST_ID = []
NOTE_SEQ_NBR = []
LAST_UPD_SYSUSR_ID = []
LAST_UPD_TS = []
NOTE_TXT = []
ASSOC_ID = []

for note in notes_data:
    if len(note) > 0:
        try:
            if note["CUST_ID"]:
                CUST_ID.append(note["CUST_ID"])
            else:
                CUST_ID.append("null")
            NOTE_SEQ_NBR.append(note["NOTE_SEQ_NBR"])
            LAST_UPD_SYSUSR_ID.append(note["LAST_UPD_SYSUSR_ID"])
            LAST_UPD_TS.append(note["LAST_UPD_TS"])
            NOTE_TXT.append(note["NOTE_TXT"])
            ASSOC_ID.append(note["ASSOC_ID"])
        except:
            continue

notes_df = pd.DataFrame({
    "CUST_ID": CUST_ID,
    "NOTE_SEQ_NBR": NOTE_SEQ_NBR,
    "LAST_UPD_SYSUSR_ID": LAST_UPD_SYSUSR_ID,
    "LAST_UPD_TS": LAST_UPD_TS,
    "NOTE_TXT": NOTE_TXT,
    "ASSOC_ID": ASSOC_ID
})

top_N = 20

notes_df = notes_df[notes_df.NOTE_TXT != 0]

df = notes_df

txt = df.NOTE_TXT.str.lower().str.replace(r'\|', ' ').str.cat(sep=' ')

txt = txt.translate(str.maketrans('','',string.punctuation))

words = txt

words = word_tokenize(words)

word_dist = nltk.FreqDist(words)

stoplist = nltk.corpus.stopwords.words('english')

more_stopwords = """: @ rt https # . , the a of her to in de la for ! and that be by el from 's out ? is //t.co/yidj0smfid que `` & ; ... '' //t.co/ygyo61kkkr  //t.co/qjt42sjbxd en ( ) n't 're //t.co/euqdcfoboh customer note added alert """

stoplist += more_stopwords.split()

words_except_stop_dist = nltk.FreqDist(w for w in words)

rslt = pd.DataFrame(words_except_stop_dist.most_common(top_N),
                    columns=['Word', 'Frequency']).set_index('Word')

print(rslt)
print('=' * 60)

bigram_measures = nltk.collocations.BigramAssocMeasures()

finder = BigramCollocationFinder.from_words(words)

bgs = nltk.trigrams(words)
fdist = nltk.FreqDist(bgs)
nGram = []
nGramF = []

print('Frequency of NGrams:')
for k,v in fdist.items():
        nGram.append(k)
        nGramF.append(v)

nGramDf = pd.DataFrame({
    "nGram": nGram,
    "nGramFreq": nGramF
})

print(nGramDf.sort_values('nGramFreq', ascending=False).head(100))