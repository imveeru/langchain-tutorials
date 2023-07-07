import streamlit as st
import urllib.parse
from fpdf import FPDF
from langchain_helper import generate_name_and_menu

st.set_page_config(
    page_title="CulinaryCrafter",
    page_icon="🥣",
    initial_sidebar_state="expanded",
)

st.title("🥣CulinaryCrafter")

cuisine=st.sidebar.selectbox('Pick a cuisine',('Indian (South Indian and North Indian)','South Indian', 'North Indian', 'Italian', 'French', 'Chinese', 'Japanese', 'Spanish', 'Lebanese', 'Mexican', 'Arabic', 'American','Thain','Turkey'))
res_type=st.sidebar.radio('Choose a diet',("Vegetarian","Non-Vegetarian","Vegan"))
location=st.sidebar.text_input('Type the name of the city')

def get_response(cuisine,res_type,location):
    return generate_name_and_menu(cuisine,res_type,location)
    #return {'cuisine': 'South India', 'type': 'Vegetarian', 'place': 'Coimbatore', 'menu': 'South India', 'location': 'Coimbatore', 'von': 'Vegetarian', 'restaurant_name': "Veggie's Delight, Coimbatore", 'menu_items': ' Cuisine\n\nIdli, Dosa, Vada, Upma, Pongal, Uttapam, Sambar Rice, Curd Rice, Masala Dosa, Rava Idli, Onion Rava Dosa, Onion Uttapam, Tomato Uttapam, Onion Pakoda, Veg Biryani, Veg Fried Rice, Veg Pulao, Veg Manchurian, Veg Kurma, Veg Korma, Aloo Gobi, Aloo Mutter, Aloo Jeera, Veg Kolhapuri, Veg Chettinadu, Veg Biryani, Veg Jalfrezi, Veg Kofta Curry, Veg Cutlet, Veg Fried Rice, Veg Sweet Corn Soup, Veg Manchow Soup, Veg Clear Soup, Veg Noodles, Veg Fried Noodles, Veg Chowmein, Veg Hakka Noodles.', 'price': '\nIdli - 25, Dosa - 40, Vada - 20, Upma - 30, Pongal - 35, Uttapam - 35, Sambar Rice - 30, Curd Rice - 35, Masala Dosa - 50, Rava Idli - 40, Onion Rava Dosa - 50, Onion Uttapam - 40, Tomato Uttapam - 40, Onion Pakoda - 25, Veg Biryani - 90, Veg Fried Rice - 70, Veg Pulao - 80, Veg Manchurian - 80, Veg Kurma - 70, Veg Korma - 70, Aloo Gobi - 70, Aloo Mutter - 70, Aloo Jeera - 70, Veg Kolhapuri - 80, Veg Chettinadu - 80, Veg Biryani - 90, Veg Jalfrezi - 80, Veg Kofta Curry - 80, Veg Cutlet - 40, Veg Fried Rice - 70, Veg Sweet Corn Soup - 50, Veg Manchow Soup - 50, Veg Clear Soup - 40, Veg Noodles - 60, Veg Fried Noodles - 60, Veg Chowmein - 60, Veg Hakka Noodles - 60.'}

if cuisine and res_type and location:
        res=get_response(cuisine,res_type,location)
        st.divider()
        st.header(res["restaurant_name"])
        cuisine=urllib.parse.quote(res["cuisine"])
        type=urllib.parse.quote(res["type"])
        place=urllib.parse.quote(res["place"])
        
        st.markdown(f'''
                    | ![{cuisine}](https://img.shields.io/badge/{cuisine}-0d327a) | ![{type}](https://img.shields.io/badge/{type}-0d327a) | ![{place}](https://img.shields.io/badge/{place}-0d327a) |
                    |:-----:|:------:|:-----------:|
                    ''')
        
        st.subheader("Menu")
        menu_items=res["price"].split(',')
        menu_text=""
        i=1
        for item in menu_items:
            st.write("-",item.strip())
            menu_text+=f"\n{i}) "+item.strip()
            i+=1

        export_as_pdf = st.button("Export Menu")
        if export_as_pdf:
            
            pdf = FPDF()  # pdf object
            pdf = FPDF(orientation="P", unit="mm", format="A4")
            pdf.add_page()
            pdf.set_font("Arial", "B", 18)
            pdf.set_xy(10.0, 20)
            pdf.cell(w=75.0, h=5.0, align="L", txt="Menu of "+str(res["restaurant_name"]))
            pdf.set_font("Arial", size=12)
            pdf.set_xy(10.0, 30)
            pdf.cell(w=75.0, h=5.0, align="L", txt=f"A "+res["cuisine"]+f" - {type} restaurant running in {place}.")
            pdf.set_xy(10.0, 35)
            pdf.write(h=7.0,txt=menu_text)
            

            st.download_button(
                "Download Menu",
                data=pdf.output(dest='S').encode('latin1'),
                file_name=res["restaurant_name"]+" - Menu.pdf",
            )
        
        st.divider()
        st.caption("The above given list and prices are AI Generated. Please do a cost analysis and customer analysis before considering the above response.")
else:
    st.divider()
    st.write("Choose the options to generate name and menu for the restaurant!")
    