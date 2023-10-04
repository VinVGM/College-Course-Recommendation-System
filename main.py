#Import all required modules
import streamlit as sweb
import streamlit.components.v1 as sweb_items



#Website
sweb.title("College Course Recommendation System")
user_input = sweb.text_area("What do you want to learn?")
clicked = sweb.button("Search")

import pandas
import neattext.functions as nt_func
from keybert import KeyBERT

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
    user_input = user_input.lower()

    kw_model = keybert_loader()
    keywords_user = kw_model.extract_keywords(user_input, keyphrase_ngram_range=(1,3), stop_words="english", highlight =False, top_n=10)
    user_input_list = list(dict(keywords_user).keys())
            

    matched_keywords= {"Course Title":[],"matched_values" :[],"URL":[],"Price":[]}            

    for skeywords in dataframe['keywords']:
    
        keywords_list = eval(skeywords)
    
        matched_values = 0
    



                
        for keyword in user_input_list:
            if keyword in keywords_list:
                matched_values+=1
                title_index = dataframe.index[dataframe["keywords"] == str(keywords_list)].tolist()
            
                title_index = title_index[0]
                title = dataframe.loc[title_index,"course_title"]
                link = dataframe.loc[title_index, "url"]
                price = dataframe.loc[title_index, "price"]
            
           
                matched_keywords["Course Title"].append(title)
                matched_keywords["matched_values"].append(matched_values)
                matched_keywords["URL"].append(link)
                matched_keywords["Price"].append(price)
                                 



                


    #result_dataframe = (pandas.DataFrame(matched_keywords)).sort_values(by=["matched_values"], ascending=False)
    result_dataframe = (pandas.DataFrame(matched_keywords)).sort_values(by=["matched_values"], ascending=False)
    i = 1
    for row in result_dataframe.iterrows():
        
        Title = row[1][0]
        sweb.write(i,". ",Title)
        Url = row[1][2]
        sweb.write("Url:",Url)
        Price = row[1][3]
        sweb.write("Price: ",Price,"$")
        sweb.write("")
        i+=1
    




 



csv = "courses_with_keywords_test.csv"
dataframe = csv_reader(csv)








if clicked == True:
    dataframe = keyword_recc_system(user_input,dataframe,csv)
    dataframe











