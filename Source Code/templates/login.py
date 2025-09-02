# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 20:05:39 2025

@author: user
"""

import streamlit as st
USER_CREDENTIALS={"admin","password123","user","test123"}
if "logged_in" not in st.session_state:st.session_state.logged_in = False
def login(username,password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username]==password:
        st.session_state.logged_in = True
        st.session_state.logged_in = username
        st.success(f"Welcome,{username}!")
    else:
        st.error("invalid username or password")
def logout():
    st.session_state.logged_in = False st.session_state.username=""
    st.title("Login Page")
if not st.session_state.logged_in:
    username = st.text_input("username")
    password = st.text_input("Password",type="password")
    if st.button("Login"):
        login(username, password)
    else:
        st.write(f"Logged in as:**{st.session_state.username}**")
        st.button("Logout",on_click=logout)