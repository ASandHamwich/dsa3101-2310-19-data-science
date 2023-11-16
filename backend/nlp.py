# things i pip installed: spacy (google how to pip install it properly), scikit-learn, wordcloud, matplotlib, --upgrade pip and --upgrade Pillow (if wordcloud isn't generating)
import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
# from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys

# specific imports to generate the glossary list of keywords
import requests
from bs4 import BeautifulSoup

# generate keywords list first
url = "https://www.datascienceglossary.org/"
response = requests.get(url)
response.encoding = 'utf-8'  # Set encoding to UTF-8

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    glossary_elements = soup.find_all("di") #the headers are contained inside the dt tags , dt tags are used to define a term

    # Create a set to store unique glossary terms
    glossary_dic = dict()
    for element in glossary_elements:
        term = element.find("dfn").get_text().strip() #extract text within dfn tags, the headers are contained inside the dfn tags
        glossary_dic[term] = element.find("dd").find("p").get_text().strip()

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

additional_words = {'optimisation': 'Process of making something as effective or functional as possible. It involves improving and fine-tuning systems, processes, or objects to achieve the best possible performance, efficiency, or outcome. Optimization is a common concept in various fields, including mathematics, engineering, computer science, business, and more.', 
                    'Python': 'Python is a high-level, general-purpose programming language known for its readability, simplicity, and versatility. It was created by Guido van Rossum and first released in 1991. Python has become one of the most popular programming languages due to its ease of learning, extensive standard libraries, and a vibrant community of developers.', 
                    'Java': 'Java is a high-level, object-oriented, and versatile programming language that was first released by Sun Microsystems in 1995. It has since become one of the most popular and widely used programming languages due to its platform independence, strong community support, and extensive ecosystem.', 
                    'programming': 'Programming refers to the process of creating computer programs or scripts that instruct a computer to perform specific tasks or solve problems. It involves writing instructions in a programming language that a computer can understand and execute. Programming is a key component of software development and plays a crucial role in creating a wide range of applications, from simple scripts to complex software systems.', 
                    'calculus': 'Calculus is a branch of mathematics that studies continuous change and motion. It has two main branches: differential calculus and integral calculus.', 
                    'probability': 'Probability is a branch of mathematics that deals with the likelihood or chance of events occurring. It provides a quantitative measure of uncertainty and is used to model and analyze random phenomena.',
                    'data structure': 'A data structure is a way of organizing and storing data to perform operations efficiently. It defines the relationship between the data, the operations that can be performed on the data, and the constraints on these operations. Choosing the right data structure is essential for optimizing the performance of algorithms and solving computational problems efficiently.',
                    'vision': 'Vision refers to the application of computer vision, a subfield of artificial intelligence and computer science. Computer vision involves teaching machines to interpret and understand visual information from the world, such as images and videos.', 
                    'cryptocurrencies': 'Cryptocurrency is a form of digital or virtual currency that uses cryptography for security and operates on decentralized networks based on blockchain technology. Unlike traditional currencies issued by governments and central banks, cryptocurrencies operate on a peer-to-peer network, allowing for secure, transparent, and borderless transactions.', 
                    'digital currencies': 'Digital currencies encompass a broad category of currencies that exist in electronic or digital form, and they include both cryptocurrencies and traditional digital representations of fiat currencies.', 
                    'fintech': 'Fintech is a term that refers to the intersection of finance and technology. It encompasses a wide range of technological innovations and applications that aim to improve and automate the delivery and use of financial services. Fintech companies leverage cutting-edge technologies to enhance traditional financial activities, create new business models, and enhance overall efficiency in the financial industry.'}

for word, desc in additional_words.items():
    lemma = lemmatize(word)
    tokenized_description = tokenize(lemma, ngram_range=(1, 2))
    for t in tokenized_description:
        glossary_dic[t] = desc
glossary_dic['statistics'] = 'Statistics is a branch of mathematics that involves collecting, analyzing, interpreting, presenting, and organizing data. It provides methods and techniques for making inferences and drawing conclusions about populations based on sample'

# returns {key_concept: description}
def get_glossary_dic():
    return glossary_dic

# returns the list of all the key_concepts
def get_glossary_list():
    glossary_list = []
    for name, desc in glossary_dic.items():
        glossary_list.append(name)
    return glossary_list