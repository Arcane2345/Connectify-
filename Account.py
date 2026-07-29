import streamlit as st
import json


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
with open("pages/data.json", "r") as file:
    data = json.load(file)
st.title("Connectify+")
st.subheader("Connect. Share. Belong.")
option = st.radio("Select an option", ("Login", "Create an account"))
if option == "Create an account":
    Name = st.text_input("Name")
    Email = st.text_input("Email")
    Password = st.text_input("Password", type="password")
    if Email in [user["email"] for user in data["users"]]:
        st.error("An account has already been created with this email. Please use a different email.")
    st.write("")
    if st.button("Create Account"):
        new_user = {
            "name": Name,
            "email": Email,
            "password": Password
        }
        data["users"].append(new_user)
        with open("pages/data.json", "w") as file:
            json.dump(data, file, indent=4)
        st.success("Account created successfully!") 
        st.session_state.logged_in = True
        st.session_state.name = Name
        st.switch_page("pages/Home.py")
elif option == "Login":
    Email = st.text_input("Email")
    Password = st.text_input("Password", type="password")
    st.write("")
    if st.button("Login"):
        login_successful = False
        for user in data["users"]:
            if user["email"] == Email and user["password"] == Password:
                login_successful = True
                st.session_state.logged_in = True
                st.session_state.name = user["name"]
                st.success("Logged in successfully!")
                st.switch_page("pages/Home.py")
                break
        if not login_successful:
            st.error("Invalid email or password.")
