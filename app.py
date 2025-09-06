from dotenv import load_dotenv
load_dotenv() ## Load environment variables from a .env file

import streamlit as st
import os
import sqlite3

## Install the Google GenAI SDK so that we can call the Gemini models
from google import genai

## The client gets the API key from the environment variable `GEMINI_API_KEY`
client = genai.Client()

# Function to load Google Gemini model and provide sql query as response
def get_gemini_response(question, prompt):
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents = [prompt[0], question]
        # config={
        #     "max_output_tokens": 256,
        #     "temperature": 0.2,
        # }
    )
    return response.text

## Function to retrieve query results from the sql database
def read_sql_query(sql, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    data = cursor.execute(sql)
    rows = data.fetchall()
    connection.commit()
    connection.close()
    for row in rows:
        print(row)
    return rows


## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION and MARKS.\n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """

]


## Streamlit App
#st.title("Text to SQL App using Google Gemini")
st.header("Gemini App to Retrieve SQL Data")

question = st.text_input("Input: ", key = "input")

submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    data = read_sql_query(response, "student.db")
    st.subheader("The Response is")
    for row in data:
        print(row)
        st.header(row)