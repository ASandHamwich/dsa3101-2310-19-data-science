# things i pip installed: spacy (google how to pip install it properly), scikit-learn, wordcloud, matplotlib, --upgrade pip and --upgrade Pillow (if wordcloud isn't generating)
import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
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

# loading data
nus_dsa_df = pd.read_csv("NusDsaMods.csv")
nus_dse_df = pd.read_csv("NusDseMods.csv")
ntu_df = pd.read_csv("ntu_db_sentiment.csv")
smu_df = pd.read_csv("smu.csv")

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
print(glossary_list)

tokenised = []
for index, row in smu_df.iterrows():
    lemma = lemmatize(row['Module Description'])
    tokenized_description = tokenize(lemma, ngram_range=(1, 2))
    print(tokenized_description)
    tokenised.append(tokenized_description)


# extracting keywords associated to each module
keywords = []
for i in range(len(tokenised)):
    words = []
    for j in range(len(tokenised[i])):
        if tokenised[i][j] in glossary_list and tokenised[i][j] not in words:
            words.append(tokenised[i][j])
    keywords.append(words)
keywords = [', '.join(inner_list) for inner_list in keywords]

keywords_df = pd.DataFrame(keywords, columns=['Key Concepts'])
smu_df = smu_df.reset_index(drop=True)
keywords_df = keywords_df.reset_index(drop=True)
combined_df = pd.concat([smu_df, keywords_df], ignore_index=True)
combined_df.to_csv('smu_with_concepts_reviews.csv', index=False)

# ############################ SMU ############################
# smu_df['lemmatized_text'] = smu_df['Module Description'].apply(lemmatize)
# ngram_smu= smu_df['tokenized_text'] = smu_df['lemmatized_text'].apply(lambda x: tokenize(x, ngram_range=(1, 2)))  # This includes both unigrams and bigrams
# # print(ngram_smu) #just for me to check if my bigrams r present
# word_frequencies = count_frequency(ngram_smu.tolist())

# # Filter word frequencies that appear more than 0 times
# ##word_frequencies_filtered = {word: freq for word, freq in word_frequencies.items() if freq > 0}
# sorted_word_frequencies = dict(sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True))
# # Filter words in the sorted_word_frequencies dictionary based on the glossary_terms
# # pk changed the if clause in this line
# essential_words = {term: count for term, count in sorted_word_frequencies.items() if term in glossary_list}
# print(essential_words)

# # SMU wordcloud
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(essential_words)
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.title("SMU Wordcloud")
# plt.show()








# for desc in ntu_df['Course Description']:
#     if type(desc) is str: 
#         ntu_df['lemmatized_text'] = ntu_df['Course Description'].apply(lemmatize)
#     else: continue
# ngram_ntu = ntu_df['tokenized_text'] = ntu_df['lemmatized_text'].apply(lambda x: tokenize(x, ngram_range=(1, 2)))  # This includes both unigrams and bigrams
# print(ngram_ntu) #just for me to check if my bigrams r present
# word_frequencies = count_frequency(ngram_ntu.tolist())

# # NLP NTU
# tokenized_desc_ntu = []
# for desc in ntu_df['Course Description']:
#     if type(desc) is str:
#         lemmatize_desc = lemmatize(desc)
#         tokenized_desc_ntu.append(lemmatize_desc)
#     else: continue
# ngram_ntu = ntu_df['tokenized_text'] = tokenized_desc_ntu.apply(lambda x: tokenize(x, ngram_range=(1, 2)))
# word_frequencies = count_frequency(tokenized_desc_ntu)

# # Filter word frequencies that appear more than 10 times
# word_frequencies_filtered = {word: freq for word, freq in word_frequencies.items() if freq > 0}
# sorted_word_frequencies = dict(sorted(word_frequencies_filtered.items(), key=lambda item: item[1], reverse=True))
# print(sorted_word_frequencies)

# # extracting the keywords that appear more than 15 times in module descriptions of a particular university
# # NLP NUS
# tokenized_desc_nus = []
# for desc in nus_df['NUS Module Description']:
#     lemmatize_desc = lemmatize(desc)
#     tokenized_list = tokenize(lemmatize_desc)
#     tokenized_desc_nus.append(tokenized_list)

# nus_word_occurrences = count_frequency(tokenized_desc_nus)
# nus_relevant_words = {key:value for key,value in nus_word_occurrences.items() if value > 15}
# nus_relevant_words_sorted = {k: v for k, v in sorted(nus_relevant_words.items(), key=lambda item: item[1], reverse=True)}
# print(nus_relevant_words_sorted)

# # NLP NTU
# tokenized_desc_ntu = []
# for desc in ntu_df['Course Description']:
#     if type(desc) is str:
#         lemmatize_desc = lemmatize(desc)
#         tokenized_list = tokenize(lemmatize_desc)
#         tokenized_desc_ntu.append(tokenized_list)
#     else: continue

# ntu_word_occurrences = count_frequency(tokenized_desc_ntu)
# ntu_relevant_words = {key:value for key,value in ntu_word_occurrences.items() if value > 15}
# ntu_relevant_words_sorted = {k: v for k, v in sorted(ntu_relevant_words.items(), key=lambda item: item[1], reverse=True)}
# print(ntu_relevant_words_sorted)

# # NLP SMU
# tokenized_desc_smu = []
# for desc in smu_df['Module Description']:
#     lemmatize_desc = lemmatize(desc)
#     tokenized_list = tokenize(lemmatize_desc)
#     tokenized_desc_smu.append(tokenized_list)

# smu_word_occurrences = count_frequency(tokenized_desc_smu)
# smu_relevant_words = {key:value for key,value in smu_word_occurrences.items() if value > 15}
# smu_relevant_words_sorted = {k: v for k, v in sorted(smu_relevant_words.items(), key=lambda item: item[1], reverse=True)}
# print(smu_relevant_words_sorted)

# # NUS wordcloud
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(nus_relevant_words_sorted)

# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.title("NUS Wordcloud")
# plt.show()

## NTU wordcloud
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(ntu_relevant_words_sorted)

# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.title("NTU Wordcloud")
# plt.show()

# # SMU wordcloud
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(smu_relevant_words_sorted)

# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.title("SMU Wordcloud")
# plt.show()