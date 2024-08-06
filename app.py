import streamlit as st
import main

# def get_response(question):
#     # For now, we'll use a simple placeholder response.
#     # In a real application, this function would generate or retrieve a response based on the question.
#     return f"You asked: {question}\nResponse: This is a placeholder response."

# Title of the web app
st.title("School Accreditation Search")

if 'question' not in st.session_state:
    st.session_state.question = ''
if 'response' not in st.session_state:
    st.session_state.response = ''

# Prompt user to type in a question
st.session_state.question = st.text_input("Type your search parameters here:")

# When the user presses the button, generate a response
if st.button("Get Response"):
    if st.session_state.question:
        response = main.call_crew(st.session_state.question)
        st.markdown(response)
    else:
        st.session_state.response = "Please type the school name or state you want to search for."

# Display the response if available
if st.session_state.response:
    with st.expander("See the response"):
        st.markdown(st.session_state.response)

# Button to clear the output and ask another question
if st.button("Clear"):
    st.session_state.question = ''
    st.session_state.response = ''
    # restart session