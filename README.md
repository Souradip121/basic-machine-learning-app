# Placement Prediction Project  
  
This project consists of two main components: a FastAPI backend and a Streamlit frontend. The FastAPI backend serves as an API to predict placement based on CGPA and IQ, while the Streamlit frontend provides an interactive user interface for inputting data and viewing predictions.  
  
## Requirements  
  
- Python 3.6+  
- pip (Python package installer)  
  
## Installation  
  
1. **Clone the repository:**  
  
    ```sh  
    git clone https://github.com/your-repo/placement-prediction.git  
    cd placement-prediction  
    ```  
  
2. **Create and activate a virtual environment (optional but recommended):**  
  
    - On Windows:  
  
        ```sh  
        python -m venv myenv  
        myenv\Scripts\activate  
        ```  
  
    - On macOS and Linux:  
  
        ```sh  
        python -m venv myenv  
        source myenv/bin/activate  
        ```  
  
3. **Install the required packages:**  
  
    ```sh  
    pip install -r requirements.txt  
    ```  
  
## Running the FastAPI Backend  
  
1. **Ensure you have the FastAPI code in a file named `main.py`:**  
  
    ```python  
    from fastapi import FastAPI, HTTPException  
    from pydantic import BaseModel  
    import numpy as np  
    import pickle  
    import uvicorn  
  
    app = FastAPI()  
  
    # Load the model and scaler from the pickle file  
    with open('model.pkl', 'rb') as f:  
        data = pickle.load(f)  
        model = data['model']  
        scaler = data['scaler']  
  
    class PlacementPredictionRequest(BaseModel):  
        cgpa: float  
        iq: float  
  
    @app.get("/")  
    def read_root():  
        return {"message": "Welcome to the placement prediction API"}  
  
    @app.post("/predict")  
    def predict(data: PlacementPredictionRequest):  
        # Prepare input data  
        input_data = np.array([[data.cgpa, data.iq]])  
        input_data = scaler.transform(input_data)  
        # Make prediction  
        prediction = model.predict(input_data)  
        return {"placement": int(prediction[0])}  
  
    if __name__ == "__main__":  
        uvicorn.run(app, host="0.0.0.0", port=8000)  
    ```  
  
2. **Run the FastAPI application:**  
  
    ```sh  
    python -m uvicorn main:app --reload  
    ```  
  
   The FastAPI server will be available at `http://localhost:8000`.  
  
## Running the Streamlit Frontend  
  
1. **Ensure you have the Streamlit code in a file named `app.py`:**  
  
    ```python  
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
    ```  
  
2. **Run the Streamlit application:**  
  
    ```sh  
    streamlit run app.py  
    ```  
  
   The Streamlit application will be available at `http://localhost:8501`.  
  
## Summary  
  
1. Install the required packages:  
  
    ```sh  
    pip install -r requirements.txt  
    ```  
  
2. Run the FastAPI application:  
  
    ```sh  
    python -m uvicorn main:app --reload  
    ```  
  
3. Run the Streamlit application:  
  
    ```sh  
    streamlit run app.py  
    ```  
  
By following these steps, you will have both the FastAPI backend and Streamlit frontend up and running, allowing you to make placement predictions interactively.  
