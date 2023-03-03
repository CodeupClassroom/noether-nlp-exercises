from requests import get
from bs4 import BeautifulSoup
import pandas as pd

import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

################################ BASIC CLEAN ################################
def basic_clean(string):
    '''
    This function takes in the original text.
    The text is all lowercased and any characters that are not ascii are ignored
    additionally, special characters are all removed.
    A clean article is then returned
    '''
    #lowercase
    string = string.lower()
    
    #normalize
    string = unicodedata.normalize('NFKD', string)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    #remove special characters and replaces it with blank
    string = re.sub(r"[^a-z0-9'\s]", '', string)
    
    return string

################################ TOKENIZE ################################

def tokenize(string):
    '''
    This function takes in a string
    and returns the string as individual tokens put back into the string
    '''
    #create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()

    #use the tokenizer
    string = tokenizer.tokenize(string, return_str = True)

    return string

################################ STEM ################################

def stem(text):
    '''
    This function takes in text
    and returns the stem word joined back into the text
    '''
    #create porter stemmer
    ps = nltk.porter.PorterStemmer()
    
    #use the stem
    stems = [ps.stem(word) for word in text.split()]
    
    #join stem word to string
    text_stemmed = ' '.join(stems)

    return text_stemmed

################################ LEMMATIZE ################################

def lemmatize(text):
    '''
    This function takes in text
    and returns the lemmatized word joined back into the text
    '''
    #create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    
    #look at the article 
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    
    #join lemmatized words into article
    text_lemmatized= ' '.join(lemmas)

    return text_lemmatized

################################ REMOVE STOPWORDS ################################

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in text, extra words and exclude words
    and returns a list of text with stopword removed
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(exclude_words)
    
    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))
    
    # Split words in string.
    words = string.split()
    
    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords

################################ PREP ARTICLES ################################

#take dataframe, specify the column, extra and exclude words
def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    #original text from content column
    df['original'] = df['content']
    
    #chain together clean, tokenize, remove stopwords
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    #chain clean, tokenize, stem, remove stopwords
    df['stemmed'] = df['clean'].apply(stem)
    
    #clean clean, tokenize, lemmatize, remove stopwords
    df['lemmatized'] = df['clean'].apply(lemmatize)
    
    return df[['title', 'original', 'clean', 'stemmed', 'lemmatized']]