from secret_key import openai_api_key
import os
os.environ["OPENAI_API_KEY"]=openai_api_key

from langchain.llms import OpenAI

llm=OpenAI(temperature=0.5)

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

name_template=PromptTemplate(
    input_variables=['cuisine', 'type', 'place'],
    template='''
    I am planning to open a restaurant. I'll provide you with the details below, Suggest a fancy and catchy name for it. (Give the name with a relevant emoji)

    Type: {type}
    Cuisine: {cuisine}
    Location: {place}
    '''
)
name_chain=LLMChain(llm=llm,prompt=name_template,output_key="restaurant_name")

menu_template=PromptTemplate(
    input_variables=['restaurant_name','von','menu'],
    template="Give me a comma separated values of menu items (minimum 20, maximum 50) for the {von} restaurant named {restaurant_name} which serves {menu}"
)
menu_chain=LLMChain(llm=llm,prompt=menu_template,output_key="menu_items")

price_template=PromptTemplate(
    input_variables=['menu_items','location'],
    template='''
    Give me a comma separated price list for the below mentioned menu items.
    
    {menu_items}
    
    The restaurant is located in {location}. Assign the price accordingly. Assume the currency according to the give location. Format the output as a comma separated values.
    '''
)
price_chain=LLMChain(llm=llm,prompt=price_template,output_key="price")

from langchain.chains import SequentialChain
from langchain.memory import SimpleMemory

def generate_name_and_menu(res_type,cuisine,place):
    overall_chain = SequentialChain(
        memory=SimpleMemory(memories={"menu": cuisine, "location":place, "von":res_type}),
        chains=[name_chain, menu_chain, price_chain],
        input_variables=["cuisine", "type","place"],
        output_variables=["restaurant_name","menu_items","price"]
    )

    return overall_chain({"cuisine":cuisine,"type":res_type,"place":place})