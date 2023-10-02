import pandas
from keybert import KeyBERT





#Generates keywords in empty cells if the keyword_gen misses to fill empty cells
def keyword_fixer(dataframe, csv):
    kw_model = keybert_loader()
    i=0
    for keyword_list in dataframe['keywords']:
        try:
            x = eval(keyword_list)
        
        
        except:
            keywords = kw_model.extract_keywords(dataframe._get_value(i,"course_title_l"), keyphrase_ngram_range=(1,3), stop_words="english", highlight =False, top_n=10)
            keywords_list = list(dict(keywords).keys())
            dataframe.at[i,"keywords"] = keywords_list
            i+=1
    dataframe.to_csv(csv)



#Generates keywords
def keyword_gen(dataframe,csv):
    kw_model = keybert_loader()
    dataframe['keywords'] = ""
    allkey_list = []
    for title in dataframe["course_title_l"]:
        keywords = kw_model.extract_keywords(title, keyphrase_ngram_range=(1,3), stop_words="english", highlight =False, top_n=10)
        keywords_list = list(dict(keywords).keys())
        #print(keywords_list)
    
        title_index = dataframe.index[dataframe["course_title_l"] == title].tolist()
        title_index = title_index[0]
        print(title_index)
        dataframe.at[title_index, "keywords"] = keywords_list

    dataframe.to_csv(csv) 


csv = input("Enter database file")

dataframe = pandas.read_csv(csv)

keyword_gen(dataframe,csv)
keyword_fixer(dataframe,csv)