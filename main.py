#Import all required modules
import streamlit as st
import streamlit.components.v1 as st_items
import base64








#Website

st.set_page_config(page_title="Course Recommendation System", layout="wide")

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  
    background-image: url("https://images.pexels.com/photos/5905709/pexels-photo-5905709.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
    background-size: cover;  
}



</style>
"""

st.markdown(page_element, unsafe_allow_html=True)

st.markdown("""
<style>
	[data-testid="stDecoration"] {
		display: none;
	}




</style>""",
unsafe_allow_html=True)

st.title("College Course Recommendation System")
st.markdown("#")
col1,colmid, col2 = st.columns([0.4,0.1,0.5]) 

with col1:
    option = st.selectbox(
        'Choose a Course Provider',
        ('edX', 'Coursera', 'Udemy'))
    

    







import pandas
import neattext.functions as nt_func

#Create a dataframe reading the csv file dataset
def csv_reader(csv):
    dataframe = pandas.read_csv(csv)
    return dataframe


if option == "Udemy":
    csv = "dataset/udemy_courses.csv"
    dataframe = csv_reader(csv)
    dataset = 0
    with col2:
        st.image("images/udemy.png", width= 200)
if option == "Coursera":
    csv = "dataset/coursea_data.csv"
    dataframe = csv_reader(csv)
    dataset = 1
    with col1:
        st.markdown("#")
        st.write("Please Note: Price list is not available for courses offered by Coursera. please visit the website to know more about it")
        st.markdown("#")
    with col2:
        st.image("images/coursera.png", width = 200)

if option == "edX":
    csv = "dataset/edx_courses.csv"
    dataframe = csv_reader(csv)
    dataset = 2
    with col2:
        st.image("images/edx.png", width = 100)


#Loads keybert model for extraction of keywords
def keybert_loader():
    from keybert import KeyBERT
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    return kw_model




clg_course = pandas.read_csv("dataset/ecm_curriculum.csv")
clg_course_codes = clg_course["course_code"]
with col1:
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
    user_input_unmod = user_input
    user_input = user_input.lower()
    
    kw_model = keybert_loader()
    keywords_user = kw_model.extract_keywords(user_input, keyphrase_ngram_range=(1,3), stop_words="english", highlight =False, top_n=10)
    user_input_list = list(dict(keywords_user).keys())
    print(user_input_list)
            
    if dataset == 0 or dataset == 2:
        matched_keywords= {"Course Title":[],"matched_values" :[],"URL":[],"Price":[], "matched_keywords" : []}
    if dataset == 1:
        matched_keywords= {"Course Title":[],"matched_values" :[], "URL": [] , "matched_keywords" : [], }              

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
            if dataset == 1:
                slink = "https://www.coursera.org/search?query="
                link = slink + title.replace(" ", "%20")
                matched_keywords["URL"].append(link)

            if dataset == 0 or dataset == 2:
                matched_keywords["URL"].append(link)
                matched_keywords["Price"].append(price)
                            
            matched_keywords["matched_keywords"].append(mkeyword)

                  
                                 



                


    #result_dataframe = (pandas.DataFrame(matched_keywords)).sort_values(by=["matched_values"], ascending=False)
    result_dataframe = (pandas.DataFrame(matched_keywords)).sort_values(by=["matched_values"], ascending=False)

    i = 1
    
    for row in result_dataframe.iterrows():
        
        with col2:
            
                if dataset == 1:
                    Title = row[1][0]
                    st.write(i,". ",Title)
                    
                    
                    Url = row[1][2]
                    st.write("Url: ", Url)
                    
                    i+=1
                if dataset == 0 or dataset == 2:
                    with col2:
                        Title = row[1][0]
                        st.write(i,". ",Title)
                        Url = row[1][2]
                        st.write("Url: ",Url)
                        Price = row[1][3]
                        st.write("Price: ",Price,"$")
                        st.write("")
                        i+=1
    if matched_values == 0:
        with col2:
            st.write("Courses not found. Please choose a different course provider")
    
    print(result_dataframe)

    
    
    
    




with col1: 
    clicked = st.button("Search")













if clicked == True:
    c_index = clg_course.index[clg_course["course_code"] == clg_option].tolist()
    c_index = c_index[0]
    
    user_input = clg_course._get_value(c_index,"course_title")
    print(user_input)
    keyword_recc_system(user_input,dataframe,csv,dataset)
    
    











