import pickle
import numpy as np 
import streamlit as st
import pandas as pd 


pickled_model = pickle.load(open('bodyfat_prediction.pkl', 'rb'))


def calculateBodyfat(umur,tinggi_badan,berat_badan,gender):
    bodyfat = ""
    if(gender == 'Laki-laki'):
        h_squared = tinggi_badan/ 100
        bmi = berat_badan/(h_squared*h_squared)
        desnity = 49500/(43380 + 120* bmi + 23 * umur)
        bodyfat = pickled_model.predict(np.array([(umur, berat_badan,	tinggi_badan ,desnity,bmi)]).reshape(1,-1))
        bodyfat = bodyfat[0]
        
    elif(gender ==  'Perempuan'):
        bmi = berat_badan/((tinggi_badan/ 100)*(tinggi_badan/ 100))
        bodyfat = (1.2*bmi)+(0.23*umur)-5.4
    
    return bodyfat

c_tinggi =""
c_berat = ""
kkb = ""
st.set_page_config(page_title="Fidealify", page_icon="images\Fi.png", layout="wide")

# Header Section 
with st.container():
    st.title('Fidealify')
    st.write(
        "The Body Fat Calculator can be used to estimate your total body fat based on specific measurements."
    )
    st.write('---')
    hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    '''
st.markdown(hide_img_fs, unsafe_allow_html=True)
hasil = ""
with st.container():
    st.header(' Calculate')
    st.text('\n')
    st.text('\n')
    st.text('\n')
    col_upper,ccol = st.columns([4,6])
    with col_upper :
        gender = col_upper.selectbox(
        'Gender anda',
        ('Laki-laki', 'Perempuan', ))
        umur = st.number_input(
            "Umur anda"
            )

    col1, col2,col3, = st.columns([3, 1, 6])
    with col1 :
        tinggi_badan = st.number_input(
        "Tinggi badan anda"
        )

    with col2 :
        tinggi_badan_option = st.selectbox(
        '',
        ('cm', 'ft', ),label_visibility='hidden')
    col1, col2,col3, = st.columns([3, 1, 6])
    with col1 :
        berat_badan = st.number_input(
        "Berat badan anda"
        )
    with col2 :
        beart_badan_option = st.selectbox(
        '',
        ('kg', 'lb', ),label_visibility='hidden')
    st.text('\n')
    st.text('\n')
    
    
    col_upper,ccol = st.columns([4,6])
    if col_upper.button('Calculate body fat'):
        if (umur != 0.00 and tinggi_badan !=0.00 and berat_badan != 0.00 ):
            c_tinggi = tinggi_badan if tinggi_badan_option == "cm" else tinggi_badan*30.48;
            c_berat = berat_badan if beart_badan_option =="kg" else berat_badan*0.453592;
            hasil = calculateBodyfat(umur,c_tinggi,c_berat,gender)
            bbi = (c_tinggi-100)-((c_tinggi-100)/10) 
            kkb = 30*bbi if gender == "Laki-laki" else 25*bbi
        elif(umur == 0.00 or tinggi_badan ==0.00 or berat_badan == 0.00 ):
            col_upper.error('inputan belum di input sepenuhnya', icon="🚨")
        else :
            col_upper.error('inputan belum di input sepenuhnya', icon="🚨")

    col_upper.text('\n')
    col_upper.text('\n')
    col_upper.subheader(f'Body fat kamu : {hasil}') 
    col_upper.write('---')
    col_upper.subheader(f'Kebutuhan kalori basal perhari: {kkb}') 
    # dataset = {
    #     'Green' : 1, 
    #     'Yellow' : 2, 
    #     'Red' :3 , 
    #     'Blue' :4
    # }
    df = pd.read_csv('datasetkalori.csv')
    makananDanKalori = dict(df.values)
    # st.write(makananDanKalori)
    options = col_upper.multiselect(
        'What are your favorite colors',

        [x for x in makananDanKalori ])

    kalori = []
    
    for x in options:
        if x in makananDanKalori:
            kalori.append(makananDanKalori[x])

    dataC = {
        'name' : [i for i in options],
        'kalori' : [i for i in kalori]
    }

    col_upper.table(dataC)  # Same as st.write(df)
    st.write(f'total kalori makanan yang di makan sehari : '+ str(sum(kalori)) if sum(kalori)!= 0 else '')