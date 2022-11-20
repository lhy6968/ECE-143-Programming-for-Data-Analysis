'''
File to clean csv file
'''
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
       
     
def remove_stopwords(data):
    '''
    removes stop words

    '''
    stop_words = stopwords.words('english') + list(string.punctuation)
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
    df.to_csv("rmp.csv")
    return df


def professor_tags(x):
    '''
    dataframe containing proffessor and tags

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
    df.to_csv("professor_tags.csv")
    return df

def professor_diff(x):
    '''
    dataframe containing professor and student difficulty

    '''
    
    professors = x['professor_name'].values.tolist()
    difficulty = x['student_difficult'].values.tolist()
    
    data_tuple = list(zip(professors, difficulty))
    df = pd.DataFrame(data_tuple, columns = ['Professor', 'Difficulty'])
    df.to_csv("professor_tags.csv")
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
    df.to_csv("professor_tags.csv")
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
    df.to_csv("professor_tags.csv")
    return df
    
a = "RateMyProfessor_Sample_data.csv"
x = pd.read_csv(a)
#sentences = x['comments'].values.tolist()
#data_words = list(comments_to_words(sentences))
#data_nostop_words = remove_stopwords(data_words)
#lemmatized_data = lemmatization(data_nostop_words, allowed_word_types = ['NOUN', 'ADJ', 'VERB', 'ADV'])
#print(data_nostop_words[5])
#print(lemmatized_data[5])

#print(department_star(x))
dataframe(x)
#professor_tags(x)