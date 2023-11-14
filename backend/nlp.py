# things i pip installed: spacy (google how to pip install it properly), scikit-learn, wordcloud, matplotlib, --upgrade pip and --upgrade Pillow (if wordcloud isn't generating)
import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
# from wordcloud import WordCloud
import matplotlib.pyplot as plt

# specific imports to generate the glossary list of keywords
import requests
from bs4 import BeautifulSoup

# generate keywords list first
url = "https://www.datascienceglossary.org/"
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    glossary_elements = soup.find_all("dt") #the headers are contained inside the dt tags , dt tags are used to define a term

    # Create a set to store unique glossary terms
    glossary_set = set()
    for element in glossary_elements:
        term = element.find("dfn").get_text().strip() #extract text within dfn tags, the headers are contained inside the dfn tags
        glossary_set.add(term)

    # Convert the set to a list
    glossary_list = list(glossary_set)

else:
    print("Failed to retrieve the web page. Status code:", response.status_code)

# process module descriptions and match them with previously generated keywords
nlp = spacy.load('en_core_web_sm')

# function to lemmatize text and remove stop words
def lemmatize(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    a_lemmas = [lemma for lemma in lemmas if lemma.isalpha() and lemma not in STOP_WORDS]
    return ' '.join(a_lemmas)

def tokenize(text, ngram_range=(1, 2)):
    vectorizer = CountVectorizer(analyzer= 'word', ngram_range = ngram_range)
    doc = nlp(text)
    tokens = vectorizer.build_analyzer()(doc.text)
    return tokens # returns a list of tokens

def count_frequency(tokenized_list):
    text = ' '.join([' '.join(inner_list) for inner_list in tokenized_list])
    vectorizer = CountVectorizer(ngram_range=(1,2)) #need to change our vectorizer such that it counts bigrams, else default is unigram
    X = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    counts = X.toarray()[0]
    frequency_dict = dict(zip(feature_names, counts))
    # Remove repeated words, e.g., 'learning learning' or 'vector vector'
    cleaned_frequency_dict = {key: value for key, value in frequency_dict.items() if len(key.split()) == len(set(key.split()))}
    return(cleaned_frequency_dict)

additional_words = ['optimisation', 'Python', 'Java', 'programming', 'calculus', 'probability', 'data structure', 'vision', 'cryptocurrencies', 'digital currencies', 'fintech']
for word in additional_words:
    lemma = lemmatize(word)
    tokenized_description = tokenize(lemma, ngram_range=(1, 2))
    glossary_list.extend(tokenized_description)
glossary_list.append('statistics')

def get_glossary_list():
    return glossary_list
