import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
llm = AzureChatOpenAI(deployment_name="gpt-4o",temperature=0,max_tokens=400)
output_parser = StrOutputParser()

def finalOutputPrompt():
    prompt = [
        f"""
            You have the task of translating tech jargons so that you bridge the gap between IT and normal person.
            """,
    ]
    prompt.append("""Make the below statement as simple as possible so that any layman can understand without and difficulty. Answer in a very detailed way but in simple language for: {query}.\n
                  JUST NEED THE DETAILED TRANSLATION IN SIMPLE LANGUAGE IN BULLETS NOTHING ELSE!!!""")

    # Join prompt sections into a single string
    formattedPrompt = [''.join(prompt)]

    formattedPromptTemplate = ChatPromptTemplate.from_template(formattedPrompt[0])

    return formattedPromptTemplate



# Set the page configuration
st.set_page_config(page_title="JARGO", page_icon="🧊", layout="wide")

# Title of the chat application
st.title("JARGO: Tech Jargon Translation Demo💬🖥️")
st.text("This GenAI assistant is designed to make your life easier")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_question = st.chat_input("Enter your conversation below:")
if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    st.session_state.query=user_question
    with st.chat_message("user"):
        st.markdown(st.session_state.query)

if st.button('See Translation'):
    with st.spinner("Generating Response..."):
        prompt=finalOutputPrompt()
        print(prompt)
        print(st.session_state.query)
        chain = prompt | llm | output_parser
        user_response=chain.invoke({"query":st.session_state.query})

        st.session_state.messages.append({"role": "assistant", "content": user_response})

        with st.chat_message("assistant"):
            st.markdown(user_response)        

st.session_state.messages = st.session_state.messages[-100:]

# I understand you have issues accessing Chat GPT through google, this is because we have applied a firewall on this webpage. You can access all the OpenAI models through Motorola's techbot or front door UI.
# The issue you are facing is because you are not on VPN. Connect to VPN and set the network location to Chicago.

