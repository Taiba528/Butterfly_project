import streamlit as st
import pandas as pd


header=st.container()
with header:
    st.title('Butterfly App')
    st.markdown("Objective:To get the most Relevant publications with respect to some pre-defined Keywords and Business conditions")

from PIL import Image

image = Image.open('Indegene_Logo.png')
st.sidebar.image(image, width=200, clamp=False, channels="RGB", output_format="auto")

   

#adding a file uploader

st.header('Publication list')
file1 = st.file_uploader("Please upload your publication list here",type=["xlsx"])

if file1 is not None:
    df1= pd.read_excel(file1)
    df=df1[['PMID','Title','Abstractt_Text']]
    st.write(df1.head())
else:
    st.stop()    

#st.header('Title')
Title=df1["Title"]
with st.expander("Title"):
    st.write(Title)

#st.header('Abstract')
Abstract=df1["Abstractt_Text"]
with st.expander("Abstract"):
    st.write(Abstract)

def check_relevancy(crt):
    words_crt=[]
    for i in range(len(crt)):
        if len(crt[i])<7:
                    words_crt.append(str(' '+crt[i]+' '))
                    words_crt.append(str(' '+crt[i]+'.'))
                    words_crt.append(str(' '+crt[i]+';'))
                    words_crt.append(str(' '+crt[i]+':'))
                    words_crt.append(str(' '+crt[i]+'-'))
                    words_crt.append(str('('+crt[i]+')'))
                    words_crt.append(str(' '+crt[i]+'?')) 
                    words_crt.append(str(' '+crt[i]+'/')) 
        else:
                    words_crt.append(crt[i])
        
    #First Check whether keyword crt1 available in Title or not.
    l1a_crt_flag = []
    l1a_crt_word = []
    for i in range(len(Title)):
        try:
            l1b_crt_count=0
            l1b_crt_word=[]
            for j in range(len(words_crt)):
                if words_crt[j].lower() in Title[i].lower():
                    l1b_crt_count= l1b_crt_count+1
                    l1b_crt_word.append((words_crt[j]))
                    break


            l1a_crt_word.append(l1b_crt_word)
            l1a_crt_flag.append(l1b_crt_count)

        except:
            l1a_crt_word.append(('Title not available', 'NA'))
            l1a_crt_flag.append(0)

    

        


    #Second Check whether keyword available in Abstract or not.
    l2a_crt_flag = []
    l2a_crt_word = []
    for i in range(len(Abstract)):
        try:
            l2b_crt_count=0
            l2b_crt_word=[]
            for j in range(len(words_crt)):
                if words_crt[j].lower() in Abstract[i].lower():
                    l2b_crt_count= l2b_crt_count+1
                    l2b_crt_word.append((words_crt[j]))
                    continue


            l2a_crt_word.append(l2b_crt_word)
            l2a_crt_flag.append(l2b_crt_count)

        except:
            l2a_crt_word.append(('Abstract not available', 'NA'))
            l2a_crt_flag.append(0)

       
    
    return (l1a_crt_word,l1a_crt_flag, l2a_crt_word, l2a_crt_flag)    
       
    

files= st.file_uploader("Please upload Keywords_Criteria_lists here",accept_multiple_files=True,type=["xlsx"])
for i in range((len(files))):
    if files[i] is not None:
        data= pd.read_excel(files[i])
        crt=list(data.iloc[:,0])
        #st.write('crt_keywords_',i+1)
        a=check_relevancy(crt)
        with st.expander('crt_keywords_'+str(i+1)):
            st.write(crt)
                
    df['crt_words_T_'+str(i+1)]=a[0]
    df['crt_count_T_'+str(i+1)]=a[1]
    df['crt_words_A_'+str(i+1)]=a[2]
    df['crt_count_A_'+str(i+1)]=a[3]  

#st.header("Preprocessed Dataset")   
#with st.expander("Preprocessed Dataset"):
    #st.write(df)   


st.header("Define your Business Rule")

with st.expander("Business Condition"):
    st.markdown("Criteria 2,3 and 4 if present only once in Title - High relevancy")
    st.markdown("Criteria 2,3 and 4 if present more than once in abstract- High relevancy")
    st.markdown("Criteria 2,3 and 4 if present only once in abstract- Medium relevancy")
    st.markdown("Criteria 2,3 and 4 - Presence of keywords- irrespective once or more than once- Medium relevancy")
    st.markdown("Criteria 2,3 and 5 if present more than once or once in abstract or title- medium relevancy") 
    st.write("Criteria 5 Keywords to check : Point-Of-Care Ultrasonography","POCUS","Pocket ultrasound",
                                              "Point of care ultrasound","Point-of-care ultrasound",
                                              "Point Of Care Ultrasonography")
    st.write("Lung Keywords : Focused lung ultrasonography in dyspnea","Lung & Cardiac Ultrasound",
                                              "Lung and Cardiac Ultrasound","Lung and Cardiac Ultrasound (LuCUS)",
                                              "Lung ultrasonograph","Lung ultrasonography","Lung ultrasound",
                                              "Lung-cardiac-inferior vena cava (LCI) integrated ultrasound","LUS")
   
with st.form(key='my_form'):

    v5=st.multiselect('Select your criteria to consider',df.columns)  
    v1=st.number_input('Define a number for crt_word_count in title',min_value=1,step=1)

    v2=st.number_input('Define a number for crt_word_count in abstract',min_value=1,step=1)
    l3= pd.read_excel(files[3])
    l4= pd.read_excel(files[4])

#crt=list(data.iloc[:,0])
        
#l3=(("Point-Of-Care Ultrasonography","POCUS","Pocket ultrasound",
                                              #"Point of care ultrasound","Point-of-care ultrasound","Point Of Care Ultrasonography"))
#l4=(("Lung Keywords : Focused lung ultrasonography in dyspnea","Lung & Cardiac Ultrasound",
                                              #"Lung and Cardiac Ultrasound","Lung and Cardiac Ultrasound (LuCUS)",
                                              #"Lung ultrasonograph","Lung ultrasonography","Lung ultrasound",
                                              #"Lung-cardiac-inferior vena cava (LCI) integrated ultrasound","LUS"))

    l5=['crt_count_T_1','crt_count_T_2','crt_count_T_3',"crt_count_T_4",'crt_count_T_5','crt_count_A_1',"crt_count_A_2","crt_count_A_3","crt_count_A_4","crt_count_A_5","crt_words_A_5"]

    v3=st.multiselect('Define Criteria 5 keywords to check',l4)  
    v4=st.multiselect('Define the specific word to check',l3) 
    submit_button = st.form_submit_button(label='Submit')  
#v5=st.multiselect('Select your first criteria',df.columns)  
#v5=st.multiselect('Select your seccond criteria',l5)                                        
Relevancy=[]
for i in range(len(df["PMID"])):
    if df[v5[0]][i]==v1 and df[v5[1]][i]==v1 and df[v5[2]][i]==v1:
        Relevancy.append("High")
    elif df[v5[3]][i]>=v2 and df[v5[4]][i]>=v2 and df[v5[5]][i]>=v2:
        Relevancy.append("High")
         
    elif df[v5[3]][i]==v1 and df[v5[4]][i]==v1 and df[v5[5]][i]==v1:
        Relevancy.append("Medium")
    elif df[v5[3]][i]==v1 and df[v5[4]][i]>=v1 and df[v5[5]][i]>=v1:
        Relevancy.append("Medium")
    elif df[v5[3]][i]>=v1 and df[v5[4]][i]==v1 and df[v5[5]][i]>=v1:
        Relevancy.append("Medium")
    elif df[v5[3]][i]>=v1 and df[v5[4]][i]>=v1 and df[v5[5]][i]==v1:
        Relevancy.append("Medium")  
    elif df[v5[3]][i]>=v1 and df[v5[4]][i]>=v1 and (df[v5[6]][i] in v3 or df[v5[7]][i] in v3) and df[v5[7]][i] in v4:
        Relevancy.append("Medium")    
    else:
        Relevancy.append("Low")


df['Relevancy']=Relevancy 



Indication=[]
for i in range(len(df["PMID"])):
    if df["crt_words_T_1"][i] !='NA':
        Indication.append(df["crt_words_T_1"][i])
    elif df["crt_count_A_1"][i]==1:
         Indication.append(dataset["crt_words_A_1"][i])
        
    else:
        Indication.append("NA")

df['Indication']=Indication   

st.write(df)

col1, col2 = st.columns(2)


@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

with col1:
    #st.markdown((Total publications,len(df)), unsafe_allow_html=True)
    st.write('Total publications',len(df))   

with col2:   

    csv = convert_df(df)
    st.download_button(
       "Download Total Publication list",
       csv,
       "Total Publication list.csv",
       "text/csv",
       key='download-csv'
    )
            
with col1:
    df_High=df.loc[df['Relevancy']=="High"]
    #st.write(df_High)
    st.write('High relevancy publications',len(df_High))

with col2:     

    csv = convert_df(df_High)
    st.download_button(
       "Download High RelevancyPublication list",
       csv,
       "High Relevancy Publication list.csv",
       "text/csv",
       key='download-csv-High'
    )


with col1:
    df_Medium=df.loc[df['Relevancy']=="Medium"]
    #st.write(df_Medium)
    st.write('Medium relevancy publications',len(df_Medium))
    csv = convert_df(df_Medium)
    
   

with col2:


    st.download_button(
       "Download Medium Relevancy Publication list",
       csv,
       "Medium Relevancy Publication list.csv",
       "text/csv",
       key='download-csv-Medium'
    )
