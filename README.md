# ECE 143 (Fall '22)  - 'Rate My Professor' Reviews Analysis

The purporse of the project is to analyze Student Reviews on RateMyProfessor site to gain insight into the course difficulty level, Professor’s style of teaching and overall student sentiment at a Professor / Department level.

## Dataset

We are using the Big Data Set sourced from RateMyProfessor.com for Professors' Teaching Evaluation.

The dataset has fields like professor's name, school name, number of students, student comments, student star rating, student difficulty rating etc. The dataset contains 9,543,998 rows of comment records with valid information for 919,750 professors.

https://data.mendeley.com/datasets/fvtfjyvw7d/2


## Getting Started

### Dependencies

* Python 3.9.13 version was used
* 3rd Party Python Modules (can be found in requirements.txt) :
    1. NLTK (For sentiment analysis)
    2. Spacy (For text preprocessing)
    2. Seaborn (For visualization)
    3. Matplotlib (For visualization)
    4. Pandas
    5. Numpy
    6. Bokeh (For visualization)
    7. Plotly

### Installation & Setup

1. Clone repository
2. Install python dependencies
```sh
   pip install -r requirements.txt
```

3. Install VADER library from NLTK
```sh
    import nltk
>>> nltk.download('vader_lexicon')
```
3. Run the jupyter notebook to render visualizations & statistics


## Acknowledgments

Inspiration, code snippets, etc.
* [sentiment-analysis-hotel-reviews](https://www.kaggle.com/code/jonathanoheix/sentiment-analysis-with-hotel-reviews)
* [amazon-reviews-topic-modelling](https://www.kaggle.com/code/yasserh/amazon-product-reviews-topic-modelling)
