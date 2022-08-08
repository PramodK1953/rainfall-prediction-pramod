import streamlit as st
import numpy as np
import pandas as pd
import time
from tensorflow import keras

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.pixabay.com/photo/2019/10/18/13/08/rain-4559068__480.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
add_bg_from_url()
img,title=st.columns([1,2])
title.title("Rainfall Prediction")
img.image("small img2.jpg",width=200)

st.subheader("Select the City in which you want to predict rainfall")
st.write("Select 1 for New Delhi, 2 for Jodhpur, 3 for Kolkata, 4 for Mumbai, 5 for Chennai, 6 for Bangalore, 7 for Nagpur, 8 for Varanasi")
INcity=st.number_input("City",1,8,step=1)

st.subheader("Select the Date on which you want the prediction")
INday,INmonth=st.columns(2)
Day=INday.number_input("Day(1 to 31)",1,31,step=1)
Month=INmonth.number_input("Month(1 to 12)",1,12,step=1)

st.subheader("Please provide values of the following parameters required for Prediction")    
INsh,INrh,INsp=st.columns(3) 
SHa=INsh.number_input("Specific Humidity  (g/kg)",0.00,100.00,step=0.01)
RHa=INrh.number_input("Relative Humidity  %",0.00,100.00,step=0.01)
SPa=INsp.number_input("Surface Pressure  (kPa)",0.00,150.00,step=0.01)
INws,INwsmax,INwsmin=st.columns(3)
WSa=INws.number_input("Wind Speed  (m/s)",0.00,100.00,step=0.01)
WSmax=INwsmax.number_input("Maximum Wind Speed  (m/s)",0.00,100.00,step=0.01)
WSmin=INwsmin.number_input("Minimum Wind Speed  (m/s)",0.00,100.00,step=0.01)
INwd,INdf,INwb=st.columns(3)
WDa=INwd.number_input("Wind Direction  (Degrees)",0.00,360.00,step=0.01)
DFa=INdf.number_input("Dew/Frost Point  (C)",-100.00,100.00,step=0.01)
WBa=INwb.number_input("Wet Bulb Temperature (C)",-100.00,100.00,step=0.01)
INt,INtmax,INtmin=st.columns(3)
Temp=INt.number_input("Average Temperature (C)",-100.00,100.00,step=0.01)
Tempmax=INtmax.number_input("Maximum Temperature (C)",-100.00,100.00,step=0.01)
Tempmin=INtmin.number_input("Minimum Temperature (C)",-100.00,100.00,step=0.01)

if st.button("Predict"):
    progress=st.progress(0)
    for i in range(100):
        time.sleep(.02)
        progress.progress(i+1)    
    dataset = pd.read_csv('8 Cities Previous Rainfall Data.csv')
    from sklearn.preprocessing import OneHotEncoder
    ohe=OneHotEncoder()
    one_h=ohe.fit_transform(dataset[["City"]]).toarray()
    one_hd=pd.DataFrame(one_h)
    dataset=dataset.drop("City",axis=1)
    X = dataset.drop("PRECIPITATION",axis=1)
    from sklearn.preprocessing import StandardScaler
    sc=StandardScaler()
    sc.fit(X)
    arr=np.array([ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11., 12., 13., 14., 15.])
    arr[0]=Month
    arr[1]=Day
    arr[2]=SHa
    arr[3]=RHa
    arr[4]=SPa
    arr[5]=WSa
    arr[6]=WSmax
    arr[7]=WSmin
    arr[8]=WSmax-WSmin
    arr[9]=WDa
    arr[10]=DFa
    arr[11]=WBa
    arr[12]=Temp
    arr[13]=Tempmax
    arr[14]=Tempmin
    arr[15]=Tempmax-Tempmin
    arr=pd.DataFrame(arr)
    transformed=sc.transform(arr.T)
    transformed= pd.DataFrame(transformed)
    loc=INcity-1
    incoding = one_h[loc]
    incoding_d = pd.DataFrame(incoding).T
    input = pd.concat([transformed,incoding_d],axis=1,ignore_index=True)
    input=input.drop(1,axis=1)
    final_model = keras.models.load_model('model.h5')
    arrp=final_model.predict(input)
    max=np.argmax(arrp[0])
    if max<3:
        if (arrp[0][max]-arrp[0][max+1])<=0.05:
            max=max+1
    if max==0:
        if (arrp[0][0]-arrp[0][1]>0.05) and (arrp[0][0]-arrp[0][1]<=0.1):
            st.header("Very Light Rain (0.5-5 mm/day)")
        else:
            st.header("No Rain (0-1 mm/day)")    
    if max==1:
        if ((arrp[0][1]-arrp[0][0]>0.05) and (arrp[0][1]-arrp[0][0]<=0.1)):
            st.header("Very Light Rain (0.5-5 mm/day)")
        elif ((arrp[0][1]-arrp[0][2]>0.05) and (arrp[0][1]-arrp[0][2]<=0.1)):
             st.header("Slightly Heavy Rain (10-25 mm/day)")
        else:
            st.header("Light Rain (1-15 mm/day)") 
    if max==2:
        if ((arrp[0][2]-arrp[0][1]>0.05) and (arrp[0][2]-arrp[0][1]<=0.1)):
            st.header("Slightly Heavy Rain (10-25 mm/day)")
        elif ((arrp[0][2]-arrp[0][3]>0.05) and (arrp[0][2]-arrp[0][3]<=0.1)):
             st.header("Heavier Rain (25-35 mm/day)")
        else:
            st.header("Heavy Rain (15-30 mm/day)")   
    if max==3:
        if (arrp[0][3]-arrp[0][2]>0.05) and (arrp[0][3]-arrp[0][2]<=0.1):
            st.header("Heavier Rain (25-35 mm/day)")
        else:
            st.header("Very Heavy Rain (>30 mm/day)")           
    st.header(" ")
    st.header(" ")
    st.text("Rainfall Intensity probabilities:")
    st.write(arrp)
    st.markdown("""
    ###### Made with :heart: by PRAMOD
    """,True)