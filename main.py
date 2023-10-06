#Import all required modules
import streamlit as st
import streamlit.components.v1 as st_items








#Website
st.set_page_config(page_title="Course Recommendation System")
st.title("College Course Recommendation System")
col1, col2, col3 = st.columns(3)
with col1:
    option = st.selectbox(
        'Choose a Course Provider',
        ('Udemy', 'Coursera', 'edX'))






import pandas
import neattext.functions as nt_func


#Loads keybert model for extraction of keywords
def keybert_loader():
    from keybert import KeyBERT
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    return kw_model


#Create a dataframe reading the csv file dataset
def csv_reader(csv):
    dataframe = pandas.read_csv(csv)
    return dataframe

clg_course = pandas.read_csv("dataset/ecm_curriculum.csv")
clg_course_codes = clg_course["course_code"]

clg_option = st.selectbox(
        "Choose the college course for which you want a third - party course",
        clg_course_codes
        
    )








#Simplifies the course title in the dataframe
def data_simlifier(dataframe):
    dataframe["Simplified_Title"] = dataframe["course_title"].apply(nt_func.remove_stopwords)
    dataframe["Simplified_Title"] = dataframe["Simplified_Title"].apply(nt_func.remove_special_characters)
    dataframe["Simplified_Title"] = dataframe['Simplified_Title'].str.lower()
    dataframe["course_title_l"] = dataframe["course_title"].str.lower()
    return dataframe 



#Recommendation system based on keyword extraction
def keyword_recc_system(user_input, dataframe,csv, dataset):
    dataframe = data_simlifier(dataframe)
   
    user_input = user_input.lower()

    kw_model = keybert_loader()
    keywords_user = kw_model.extract_keywords(user_input, keyphrase_ngram_range=(1,3), stop_words="english", highlight =False, top_n=10)
    user_input_list = list(dict(keywords_user).keys())
    print(user_input_list)
            
    if dataset == 0 or dataset == 2:
        matched_keywords= {"Course Title":[],"matched_values" :[],"URL":[],"Price":[], "matched_keywords" : []}
    if dataset == 1:
        matched_keywords= {"Course Title":[],"matched_values" :[], "matched_keywords" : []}              

    for skeywords in dataframe['keywords']:
    
        keywords_list = eval(skeywords)
        
    
        matched_values = 0
    


        global title
        title = ""
        global link
        link = ""
        global price
        price = ""
        
        mkeyword = []
                
        for keyword in user_input_list:
            for skeyword in keywords_list:
                if skeyword == keyword:
                    
                    matched_values+=1
                    title_index = dataframe.index[dataframe["keywords"] == str(keywords_list)].tolist()
                
                    title_index = title_index[0]
                    title = dataframe.loc[title_index,"course_title"]
                    if dataset == 0 or dataset == 2:
                        link = dataframe.loc[title_index, "url"]
                        price = dataframe.loc[title_index, "price"]
                    mkeyword.append(keyword)
        
        if title != "":
            matched_keywords["Course Title"].append(title)
            matched_keywords["matched_values"].append(matched_values)

            if dataset == 0 or dataset == 2:
                matched_keywords["URL"].append(link)
                matched_keywords["Price"].append(price)
                            
            matched_keywords["matched_keywords"].append(mkeyword)           
                                 



                


    #result_dataframe = (pandas.DataFrame(matched_keywords)).sort_values(by=["matched_values"], ascending=False)
    result_dataframe = (pandas.DataFrame(matched_keywords)).sort_values(by=["matched_values"], ascending=False)
    i = 1
    for row in result_dataframe.iterrows():
        
        Title = row[1][0]
        st.write(i,". ",Title)

        if dataset == 0 or dataset == 2:

            Url = row[1][2]
            st.write("Url:",Url)
            Price = row[1][3]
            st.write("Price: ",Price,"$")
            st.write("")
            i+=1
    
    print(result_dataframe)
    




 
clicked = st.button("Search")








if option == "Udemy":
    csv = "dataset/udemy_courses.csv"
    dataframe = csv_reader(csv)
    dataset = 0
if option == "Coursera":
    csv = "dataset/coursea_data.csv"
    dataframe = csv_reader(csv)
    dataset = 1
if option == "edX":
    csv = "dataset/edx_courses.csv"
    dataframe = csv_reader(csv)
    dataset = 2




if clicked == True:
    c_index = clg_course.index[clg_course["course_code"] == clg_option].tolist()
    c_index = c_index[0]
    
    user_input = clg_course._get_value(c_index,"course_title")
    print(user_input)
    dataframe = keyword_recc_system(user_input,dataframe,csv,dataset)
    dataframe











