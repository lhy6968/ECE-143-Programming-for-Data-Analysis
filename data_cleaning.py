"""
Helper functions to Preprocessing Data
"""

import pandas as pd
import string
from string import digits
import spacy
from collections import defaultdict
import gensim
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

def comments_to_words(sentences, deacc=True):
    '''
    takes comments from data file and prepares them to be cleaned by 
    removing punctuation and splitting sentences into single words
    '''
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence)))
       
     
def remove_stopwords(data, custom_words):
    '''
    removes stop words

    '''
    stop_words = stopwords.words('english') + custom_words + list(string.punctuation)
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in data]

def lemmatization(data, allowed_word_types = ['NOUN', 'ADJ', 'VERB', 'ADV']):
    output = []
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    for i in data:
        doc = nlp(" ".join(i))
        output.append([token.lemma_ for token in doc if token.pos_ in allowed_word_types])
    return output

def department_star(x):
    
    departments = x['department_name'].values.tolist()
    star = x['student_star'].values.tolist()
    d = defaultdict(list)
    
    for key, value in zip(departments, star):
        d[key].append(value)
    return dict(d)


def dataframe(x):
    '''
    
    dataframe with school, professor, department, state and avg rating

    '''
    
    schools = x['school_name'].values.tolist()
    professors = x['professor_name'].values.tolist()
    departments = x['department_name'].values.tolist()
    state = x['state_name'].values.tolist()
    star = x['star_rating'].values.tolist()
    data_tuple = list(zip(schools, professors, departments, state, star))
    df = pd.DataFrame(data_tuple, columns = ['School', 'Professor', 'Department', 'State', 'Star'])
    df = df.drop_duplicates()
    df = df.sort_values('School')
    return df


def professor_tags(x):
    '''
    dataframe containing professor and tags

    '''
    professors = x['professor_name'].values.tolist()
    tags = x['tag_professor'].values.tolist()
    
  
    for i in range(len(tags)):
        tags[i] = str(tags[i])
        tags[i] = tags[i].replace("(","").replace(")", "")
        remove_digits = str.maketrans('','', digits)
        tags[i] = tags[i].translate(remove_digits)
        tags[i] = tags[i].replace("\\", "")
    
        
    data_tuple = list(zip(professors, tags))
    df = pd.DataFrame(data_tuple, columns = ['Professor', 'Tags'])
    df = df.drop_duplicates()
    return df


def professor_tags_dict(x):
    '''
    dictionary of the form
    
    [prof : [(tag1, freq1), (tag2, freq2) ... ]

    '''
    professors = df['professor_name'].values.tolist()
    df.tag_professor = df.tag_professor.fillna('')
    tags = df['tag_professor'].values.tolist()
    prof_tags_dict = collections.defaultdict(list)
    for i in range(len(tags)):  
        tgs = re.sub('\(\d\)',':', tags[i])
        clean_tags = [x.strip() for x in tgs.split(':') if x!='']
        freqs = re.findall('(\d)', tags[i])
        tag_freqs = list(zip(clean_tags, freqs))
        prof_tags_dict[professors[i]] = tag_freqs
        
    with open('prof_tags_dict.pickle', 'wb') as handle:
        pickle.dump(prof_tags_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)



def professor_diff(x):
    '''
    dataframe containing professor and student difficulty

    '''
    
    professors = x['professor_name'].values.tolist()
    difficulty = x['student_difficult'].values.tolist()
    
    data_tuple = list(zip(professors, difficulty))
    df = pd.DataFrame(data_tuple, columns = ['Professor', 'Difficulty'])
    return df

def date_star(x):
    '''
    df with professor, star rating and date

    '''
    
    professors = x['professor_name'].values.tolist()
    star = x['star_rating'].values.tolist()
    date = x['post_date'].values.tolist()
    
    data_tuple = list(zip(professors, star, date))
    df = pd.DataFrame(data_tuple, columns = ['Professor', 'Star', 'Post Date'])
    return df


def diff_star(x):
    '''
    df with professor difficulty and star rating

    '''
    professors = x['professor_name'].values.tolist()
    star = x['star_rating'].values.tolist()
    difficulty = x['student_difficult'].values.tolist()

    data_tuple = list(zip(professors, difficulty, star))
    df = pd.DataFrame(data_tuple, columns = ['Professor', 'Difficulty', 'Star'])
    return df