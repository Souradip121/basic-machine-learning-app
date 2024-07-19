import streamlit as st  
import requests  

st.title("Placement Prediction")  

cgpa = st.number_input("Enter your CGPA:", min_value=0.0, max_value=10.0, step=0.1)  
iq = st.number_input("Enter your IQ:", min_value=0, max_value=200, step=1)  

if st.button("Predict"):  
    # Prepare the data to send to FastAPI  
    data = {  
        "cgpa": cgpa,  
        "iq": iq  
    }  

    # Call the FastAPI endpoint  
    response = requests.post("http://localhost:8000/predict", json=data)  

    if response.status_code == 200:  
        result = response.json()  
        placement = result["placement"]  
        if placement == 1:  
            st.success("You are likely to be placed!")  
        else:  
            st.warning("You are unlikely to be placed.")  
    else:  
        st.error("Error in prediction. Please try again.")  
