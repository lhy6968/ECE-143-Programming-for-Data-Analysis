import csv
from numpy import *
from data_cleaning import remove_stopwords, comments_to_words, lemmatization, professor_tags
import pandas as pd
from nltk.util import ngrams
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def best_worst_departments(f):
    '''
    Return the Best & Worst departments based on ratings
    '''
    csvreader = csv.reader(f)
    final_list = list(csvreader)
    res_dict = {}
    for i in range(len(final_list)):
        if i == 0:
            continue
        if final_list[i][2] not in res_dict:
            res_dict[final_list[i][2]] = [float(final_list[i][6])]
        else:
            res_dict[final_list[i][2]].append(float(final_list[i][6]))
            
    new_res_dict = {}
    for i in res_dict:
        if len(res_dict[i]) >= 100:
            new_res_dict[i] = mean(res_dict[i])
            
    res_list = []
    for i in new_res_dict:
        res_list.append(new_res_dict[i])
    res_list.sort()
    
    
    best_department = {}
    worst_department = {}
    for i in range(5):
        temp = [k for k,v in new_res_dict.items() if v == res_list[i]]
        worst_department[temp[0][:-11]] = res_list[i]

    for i in range(1,6):
        temp = [k for k,v in new_res_dict.items() if v == res_list[-i]]
        best_department[temp[0][:-11]] = res_list[-i]
    
    return best_department, worst_department


def prof_count(df):
    '''
    Return a dataframe of unique professors & a count of their reviews
    '''
    df_profs = df.groupby('professor_name')['professor_name'].count()
    return df_profs

def dept_count(df):
    '''
    Return a dataframe of unique departments & a count of their reviews
    '''
    df_depts = df.groupby('department_name')['department_name'].count()
    
    return df_depts


def add_clean_reviews(df):
    '''
    Clean the reviews text and add two new columns to DF ~ 
    
    1. Cleaned Text (including stop words)
    2. Deep Cleaned Text  
    '''
    custom_words = ['professor', 'class', 'teacher', 'question']

    sentences = df['comments'].values.tolist()
    data_words = list(comments_to_words(sentences))
    data_nostop_words = remove_stopwords(data_words, custom_words)
    lemmatized_data = lemmatization(data_nostop_words, allowed_word_types = ['NOUN', 'ADJ', 'VERB', 'ADV'])

    # Lower case + Tokenization only (for word clouds)
    clean_reviews = []
    for sen in data_words:
            clean_sen = ' '.join(word for word in sen)
            clean_reviews.append(clean_sen)

    df['clean_reviews'] = clean_reviews
    
    clean_reviews_nostop = [ ' '.join(word for word in sen) for sen in data_nostop_words]

    df['clean_reviews_nostop'] = clean_reviews_nostop

    return df


def concat_prof_reviews():
    '''
    Group the data by unique professors & concat all their reviews ~ Useful to create word cloud
    '''
    def f(x):
        d = {}
        d['star_rating'] = x['star_rating'].max()
        d['clean_reviews_concat'] = ' '.join(x['clean_reviews'])
        d['clean_reviews_nostop_concat'] = ' '.join(x['clean_reviews_nostop'])
        return pd.Series(d, index=['star_rating', 'clean_reviews_concat', 'clean_reviews_nostop_concat'])


    return dff.groupby('professor_name').apply(f)


def concat_prof_reviews(dff):
    '''
    Group the data by unique professors & concat all their reviews ~ Useful to create word cloud
    '''
    def f(x):
        d = {}
        d['star_rating'] = x['star_rating'].max()
        d['clean_reviews_concat'] = ' '.join(x['clean_reviews'])
        d['clean_reviews_nostop_concat'] = ' '.join(x['clean_reviews_nostop'])
        return pd.Series(d, index=['star_rating', 'clean_reviews_concat', 'clean_reviews_nostop_concat'])


    return dff.groupby('professor_name').apply(f)


def get_ngrams(text, n=2):
    '''
    For a given text review, get a list of ngrams
    '''
    text = str(text)
    n_grams = ngrams(text.split(), n)
    returnVal = []
    try:
        for grams in n_grams:
            returnVal.append('_'.join(grams))
            
    except(RuntimeError):
        pass
        
    return ' '.join(returnVal).strip()


def get_sentiment_scores(df):
    '''
    Add 4 sentiment scores to dataframe : pos, neg, neu & compound score
    '''
    sid = SentimentIntensityAnalyzer()
    df["sentiments"] = df["comments"].apply(lambda review: sid.polarity_scores(str(review)))
    df = pd.concat([df.drop(['sentiments'], axis=1), df['sentiments'].apply(pd.Series)], axis=1)
    
    return df
    

def get_department_sents(df):
    '''
    Group data by department, calculate Positive, Negative & Neutral % Sentiment of each department
    '''
    
    def func(x):
        d = {}
        pos = len(x[x['Sentiment']=='Positive'])
        neu = len(x[x['Sentiment']=='Neutral'])
        neg = len(x[x['Sentiment']=='Negative'])

        total = pos+neu+neg
        d['#Positive'] = pos/total * 100
        d['#Neutral'] = neu/total * 100
        d['#Negative'] = neg/total * 100

        return pd.Series(d, index=['#Positive', '#Neutral', '#Negative'])
    
    df_dept_sent = df.groupby('department_name').apply(func)
    df_depts = dept_count(df)
    df_dept_sent2 = df_dept_sent.join(df_depts.to_frame('count')).sort_values(by = 'count', ascending=False)
    
    return df_dept_sent2



