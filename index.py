# Import libraries
from fastapi import FastAPI, status, HTTPException
import pandas as pd
import uvicorn
from keras import models
from schema import data_to_be_used_for_prediction, prediction
from fastapi.middleware.cors import CORSMiddleware

# Load Model
model = models.load_model('please.h5')

# Initialize fastapi class
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prediction route
@app.post("/predict", response_model=prediction)
def predict_price(transaction_data: data_to_be_used_for_prediction):
    try:
        # Convert data to dictionary
        data = transaction_data.__dict__
        # Convert dictionary to dataframe
        data_df = pd.DataFrame(data)
        data_df['Date'] = pd.to_datetime(data_df['Date'])
        data_df.set_index('Date', inplace=True)
        # Make Prediction
        predictions = model.predict(data_df)
        # Save prediction to return
        prediction_dict = {'Prediction': []}
        data_list = predictions.tolist()
        for prediction in data_list[0]:
            prediction_dict['Prediction'].append(prediction[0])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
    # Return prediction
    return prediction_dict

@app.get("/")
def index():
    return {'Details': 'Working'}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
