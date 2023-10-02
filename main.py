#Import all required modules
import pandas
import neattext.functions as nt_func
import numpy
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from keybert import KeyBERT
import streamlit as sweb
import streamlit.components.v1 as sweb_items

#Loads keybert model for extraction of keywords
def keybert_loader():
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    return kw_model


#Create a dataframe reading the csv file dataset
def csv_reader(csv):
    dataframe = pandas.read_csv(csv)
    return dataframe







#Simplifies the course title in the dataframe
def data_simlifier(dataframe):
    dataframe["Simplified_Title"] = dataframe["course_title"].apply(nt_func.remove_stopwords)
    dataframe["Simplified_Title"] = dataframe["Simplified_Title"].apply(nt_func.remove_special_characters)
    dataframe["Simplified_Title"] = dataframe['Simplified_Title'].str.lower()
    dataframe["course_title_l"] = dataframe["course_title"].str.lower()
    return dataframe 



#Recommendation system based on keyword extraction
def keyword_recc_system(user_input, dataframe,csv):
    dataframe = data_simlifier(dataframe)


    kw_model = keybert_loader()
    keywords_user = kw_model.extract_keywords(user_input, keyphrase_ngram_range=(1,3), stop_words="english", highlight =False, top_n=10)
    user_input_list = list(dict(keywords_user).keys())
            

    matched_keywords= {"course_title":[],"matched_values" :[]}            

    for skeywords in dataframe['keywords']:
    
        keywords_list = eval(skeywords)
    
        matched_values = 0
    



                
        for keyword in user_input_list:
            if keyword in keywords_list:
                matched_values+=1
                title_index = dataframe.index[dataframe["keywords"] == str(keywords_list)].tolist()
            
                title_index = title_index[0]
                title = dataframe.loc[title_index,"course_title_l"]
            
           
                matched_keywords["course_title"].append(title)
                matched_keywords["matched_values"].append(matched_values)

    result_dataframe = (pandas.DataFrame(matched_keywords)).sort_values(by=["matched_values"], ascending=False)
    print(result_dataframe)
    return result_dataframe




#Recommendation system based on cosine similarity matrix

#def cos_mat_recc_sys(dataframe, user_input,csv):
    #Text Vectorization Process
    cvector = CountVectorizer()
    cvector_matrix = cvector.fit_transform(dataframe['Simplified_Title'])

    #building cosine similarity matrix
    cossim_matrix = cosine_similarity(cvector_matrix)
    #Getting course id
    course_id = pandas.Series(dataframe.index, index=dataframe['course_title']).drop_duplicates()

    #Check is user input is empty
    if user_input =='':
        user_input = None
    
    #Get course id
    if user_input is not None:
        try:

            user_input = user_input.lower()
            id = course_id[user_input]

            #create similarity index for each course and sorting from highest to lowest
            sim_index = list(enumerate(cossim_matrix[id]))
            sorted_sindex = sorted(sim_index, key=lambda x:x[1],reverse = True)
            sorted_sindex[1:]

            #Picking Final courses to be displayed:
            final_courses = [i[0] for i in sorted_sindex[1:]]
            
                
            #final result
            result = dataframe['course_title_l'].iloc[final_courses]
            result_dataframe = pandas.DataFrame(result)
            print(result_dataframe)
        except:
            result_dataframe = keyword_recc_system(user_input, dataframe, csv)
            
    return result_dataframe  


user_input = input("Type here:")
csv = "courses_with_keywords_test.csv"
dataframe = csv_reader(csv)

keyword_recc_system(user_input,dataframe,csv)











