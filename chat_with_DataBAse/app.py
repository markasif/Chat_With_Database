import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="Langchain: Chat With Sql DB",page_icon="🦜🧠")
st.title("🦜🧠Langchain:Chat with Sql DB")

LOCALDB="USE_LOCALDB"
MYSQL= "USE_MYSQL"

radio_opt=["Use Sqllite 3 Database- Student.db","Connect to your SQL Database"]
selected_opt=st.sidebar.radio(label="Choose your DB",options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    my_sql_host=st.sidebar.text_input("Provide MySQL HOSt")
    my_sql_user=st.sidebar.text_input("MYSQL USer")
    my_sql_password=st.sidebar.text_input("Enter your password",type="password")
    mysql_db=st.sidebar.text_input("mySQL database")

else:
    db_uri=LOCALDB


api_key=st.sidebar.text_input(label="Groq Api_key",type="password")

if not db_uri:
    st.info("Please Select your Database")

if not api_key:
    st.info("Please enter your api_key")


llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)

@st.cache_resource(ttl="2h")

def configure_db(db_uri,mysql_user=None,mysql_host=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator=lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine(f"sqlite:///{dbfilepath}"))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please Provide all mySQL connection details")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    
if db_uri==MYSQL:
    db=configure_db(db_uri,my_sql_user,my_sql_host,my_sql_password,mysql_db)
else:
    db=configure_db(db_uri)

toolkit=SQLDatabaseToolkit(db=db,llm=llm)
agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("Clear message History"):
    st.session_state["messages"]=[{"role":"assistant","content":"How can i help you bitch"}]


for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg["content"])

user_query=st.chat_input(placeholder="ask anything about in database")

if user_query:
    st.session_state.messages.append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        Streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[Streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)