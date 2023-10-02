#Import all required modules
import pandas
import neattext.functions as nt_func
import numpy
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer


#Create a dataframe reading the csv file dataset
dataframe = pandas.read_csv("dataset/courses.csv")

#Simplified course names
dataframe["Simplified_Title"] = dataframe["course_title"].apply(nt_func.remove_stopwords)
dataframe["Simplified_Title"] = dataframe["Simplified_Title"].apply(nt_func.remove_special_characters)
dataframe["Simplified_Title"] = dataframe['Simplified_Title'].str.lower()
dataframe["course_title_l"] = dataframe["course_title"].str.lower()

#Text Vectorization Process
cvector = CountVectorizer()
cvector_matrix = cvector.fit_transform(dataframe['Simplified_Title'])

#building cosine similarity matrix
cossim_matrix = cosine_similarity(cvector_matrix)
#Getting course id
course_id = pandas.Series(dataframe.index, index=dataframe['course_title']).drop_duplicates()





            



user_input = input("Enter what you want to learn?")
recommendation_system(user_input)
