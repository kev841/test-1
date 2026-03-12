import streamlit as st

st.title("diabetes App")

name = st.text_input("Enter you name")

if st.button("Submit"):
    st.write("Hello", name)


