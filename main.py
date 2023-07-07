import streamlit as st

st.title("Hello World")

cuisine=st.sidebar.selectbox('Pick a cuisine',('Indian (South Indian and North Indian)','South Indian', 'North Indian', 'Italian', 'French', 'Chinese', 'Japanese', 'Spanish', 'Lebanese', 'Mexican', 'Arabic', 'American','Thain','Turkey'))
res_type=st.sidebar.radio('Choose a diet',("Vegetarian","Non-Vegetarian","Vegan"))
location=st.sidebar.text_input('Type the name of the city')

