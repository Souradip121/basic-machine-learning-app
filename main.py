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
