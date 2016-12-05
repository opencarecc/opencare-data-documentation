from nltk.corpus import stopwords
from nltk.stem.porter import *
import re
import operator
import Levenshtein

fpath = "../data/mon5.bcp"
with open(fpath) as f:
	text = f.read()

#text = "http://www.abc.com it is a good example in www.ben.com but like </s> and there is < abc its=123> aTextWithoutSpace"

#remove web links
text = re.sub("http[^\s]+", ' ', text)
text = re.sub("www[^\s]+", ' ', text)
#remove marking language
text = re.sub("<.*>", ' ', text)

#correct capital letters issues
text = re.sub(r"(\w)([A-Z])", r"\1 \2", text)

#remove non letters
text = re.sub('[^a-zA-Z]+', ' ', text)

#remove (English) stop words and small words
stop = set(stopwords.words('english'))
word_list = [i for i in text.lower().split() if i not in stop and len(i)>3]


stem_list = []
stem2form = {}
stemmer = PorterStemmer()

#stem the words to avoid plural, conjugated, and multiple forms etc.
for w in word_list:
	stem = stemmer.stem(w)
	if stem not in stem2form:
		stem2form[stem] = {}

	if w not in stem2form[stem]:
		stem2form[stem][w] = 0
	stem2form[stem][w] += 1

	stem_list.append(stem)


# choose the most occurrent plain form as the representent
stem2rep = {}
for s in stem2form:
	candidate = max(stem2form[s].iteritems(), key=operator.itemgetter(1))[0]
	stem2rep[s] = candidate

#corrects some mispelling (but also may introduce some confusion across pairs of words such as lease/please)
word_set = [w for w in stem2rep.values()]
for i in range(len(word_set)-1):
	w1 = word_set[i]
	for j in range(i+1, len(word_set)):
		w2 = word_set[j]
		if Levenshtein.ratio(w1, w2) > 0.91:
			print w1, w2

# use normalized text
word_list = [stem2rep[w] for w in stem_list]

text = " ".join(word_list)
text += " "


outpath = "../data/mon5.cln"

#oversample (because limited data)
with open(outpath, "w") as f:
	for i in range(100):
		f.write(text)
