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



#Recommendation System Function
def recommendation_system(user_input):
    #Check is user input is empty
    if user_input =='':
        user_input = None

    user_input_list = user_input.split()   

    #Get course id
    if user_input is not None:

        user_input = user_input.lower()
        try:
            id = course_id[user_input]

            #create similarity index for each course and sorting from highest to lowest
            sim_index = list(enumerate(cossim_matrix[id]))
            sorted_sindex = sorted(sim_index, key=lambda x:x[1],reverse = True)
            sorted_sindex[1:]

            #Picking Final courses to be displayed:
            final_courses = [i[0] for i in sorted_sindex[1:]]
            final_course_index = [i[1] for i in sorted_sindex[1:]]
            
            #final result
            result = dataframe['course_title'].iloc[final_courses]
            result_dataframe = pandas.DataFrame(result)
            print(result_dataframe)
        except:
            
            result_dataframe = dataframe[dataframe['Simplified_Title'].str.contains(user_input, build)]
            result_dataframe_series = pandas.Series(result_dataframe.index, index=result_dataframe['course_title_l']).drop_duplicates()
            try:
                id = result_dataframe_series.iloc[0]
                #create similarity index for each course and sorting from highest to lowest
                sim_index = list(enumerate(cossim_matrix[id]))
                sorted_sindex = sorted(sim_index, key=lambda x:x[1],reverse = True)
                sorted_sindex[1:]

                #Picking Final courses to be displayed:
                final_courses = [i[0] for i in sorted_sindex[1:]]
                final_course_index = [i[1] for i in sorted_sindex[1:]]
            
                #final result
                result = dataframe['course_title'].iloc[final_courses]
                result_dataframe = pandas.DataFrame(result)
                print(result_dataframe)

            except:
                print("Not found")
    if user_input is None:
        print("Not found")    


            



user_input = input("Enter what you want to learn?")
recommendation_system(user_input)
