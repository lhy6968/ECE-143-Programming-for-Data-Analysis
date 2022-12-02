import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.interpolate import griddata
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Blues8
from bokeh.embed import components
import seaborn as sns
from bokeh.plotting import figure, output_file, show
import plotly.express as px
import plotly.graph_objects as go




# data = pd.read_csv('RateMyProfessor_Sample data.csv')

def heat_map_plot_rating(data):
    '''
    Plots the Heat map of Star Rating & Various Review Tags 
    '''

    df = data
    df = df[df['tag_professor'].notna()]
    df.dropna(subset='tag_professor')

    df_new1 = df['star_rating']
    df_new2 = df.iloc[:, 30:51]

    res = pd.concat([df_new1, df_new2], axis = 1)
    plt.figure(figsize=[15,15])
    sns.heatmap(res.corr(), annot=True)
    plt.show()

def heat_map_plot_diff(data):
    '''
    Plots the Heat map of Difficulty Rating & Various Review Tags 
    '''
    df = data
    df = df[df['tag_professor'].notna()]
    df.dropna(subset='tag_professor')

    df_new1 = df['diff_index']
    df_new2 = df.iloc[:, 30:51]

    res = pd.concat([df_new1, df_new2], axis = 1)
    plt.figure(figsize=[15,15])
    sns.heatmap(res.corr(), annot=True)
    plt.show()

def diff_rating_scatter_plot(data):
    '''
    Scatter Plot of Difficulty Index vs Star Rating 
    '''
    df = data
    p = figure(width = 400, height = 400)
    p.circle(df['diff_index'], df['star_rating'],size = 5, alpha = 0.5)
    p.xaxis.axis_label = 'diff_index'
    p.yaxis.axis_label = 'star_rating'
    show(p)

def diff_rating_regression_line_plot(data):
    '''
    Scatter Plot of Difficulty Index vs Star Rating  - "Regression Plot to see patterns"
    '''
    df = data
    aggregation_functions = {'star_rating':'mean'}
    df_new = df.groupby(df['diff_index']).aggregate(aggregation_functions)
    df_new.reset_index(inplace = True)
    sns.regplot(x = df_new['diff_index'], y = df_new['star_rating'])
    plt.show()
    

def prof_rating_based_on_department(df):
    '''
    Dataframe showing Per Department Rating"
    '''
    df_agg = df.groupby(['department_name', 'professor_name']).agg({'star_rating':'mean'})
    df_new = df_agg['star_rating'].groupby('department_name', group_keys = False).nlargest(5)
    res = df_new.reset_index()
    res.to_csv('prof_based_on_department.csv',index=False)
    print(df_new)


def state_rating_heatmap(data):
    '''
    Heat Map of US States & Rating spread across all states
    '''
    aggregation_functions = {'star_rating':'mean'}
    df_new = data.groupby(data['state_name']).aggregate(aggregation_functions)
    df_new.reset_index(inplace = True)
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
    df_new.rename(columns = {"state_name":"code", 'star_rating' : 'star_rating'}, inplace = True)
    df_new['code'] = df_new['code'].str.strip()
    res = pd.merge(df,df_new, on = 'code', how = 'outer')
    res_new = pd.read_csv('data/download_states.csv')

    fig = px.choropleth(res_new,
                    locations='code', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='star_rating',
                    color_continuous_scale="Viridis_r", 
                    
                    )

    fig.update_layout(
        title_text = 'Star Rating by States',
        geo_scope='usa', # limite map scope to USA
    )

    fig.show()

# state_rating_heatmap(data)


