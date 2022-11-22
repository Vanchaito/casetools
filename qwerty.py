import re
import requests
from collections import OrderedDict
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import matplotlib.pyplot as plt 
   
rawtext1 = requests.get('https://raw.githubusercontent.com/nevmenandr/word2vec-russian-novels/master/books_before/CrimeAndPunishment.txt').text
rawtext2 = requests.get('https://raw.githubusercontent.com/nevmenandr/word2vec-russian-novels/master/books_before/EugeneOnegin.txt').text
rawtext3 = requests.get('https://raw.githubusercontent.com/nevmenandr/word2vec-russian-novels/master/books_before/FathersAndSons.txt').text
rawtext4 = requests.get('https://raw.githubusercontent.com/nevmenandr/word2vec-russian-novels/master/books_before/MasterAndMargarita.txt').text
rawtext5 = requests.get('https://raw.githubusercontent.com/nevmenandr/word2vec-russian-novels/master/books_before/WarAndPeace.txt').text

textlines = rawtext1
textlines += rawtext2
textlines += rawtext3
textlines += rawtext4
textlines += rawtext5

dict_word = dict()

reg = re.sub(r'-\n','', textlines)
reg1 = re.sub(r'[^\w\s^]','', reg)
r = re.compile("[а-я]+")
word = word_tokenize(reg1.lower(),"russian")

for items in word:
    if r.findall(items):
        if items in dict_word:
            dict_word[items] += 1
        else:
            dict_word[items] = 1 


# Стеммер
stemmer=SnowballStemmer("russian")
rankdict=dict()

for item in dict_word:
    word_stem=stemmer.stem(item)  
    
    if word_stem in rankdict:
        rankdict[word_stem] += dict_word.get(item)
    else:
        rankdict[word_stem] = dict_word.get(item)
    

sortDict = OrderedDict(sorted(rankdict.items(), key = lambda item: item[1], reverse=True))
popular_word = []
frequency=[]
rank=[]
wordCount=0
k = 0
c = 0.00

# Количество слов
for item in sortDict:
    wordCount+=sortDict.get(item)

# Ранг и частота слов
for item in sortDict:
    if (k==0):
        k = k + 1
        popular_word.append(item)
        frequency.append(sortDict.get(item))
        rank.append(k)
        continue
    
    if (frequency[-1]!=sortDict.get(item)):
        k = k + 1
        rank.append(k)
    else:
        rank.append(k)
        
    popular_word.append(item)
    frequency.append(sortDict.get(item))

    c=frequency[-1]*rank[-1]/wordCount
    print(c)
    if (k == 20):
        break

# График    
plt.title('Закон Зипфа') # заголовок
plt.xlabel('Ранг') # ось абсцисс
plt.ylabel('Частота') # ось ординат
plt.plot(rank, frequency)

plt.show()

# Постоянная Зипфа
c=frequency[-1]*rank[-1]/wordCount
print('Постоянная Зипфа = ' + str(c))

